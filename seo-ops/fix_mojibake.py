#!/usr/bin/env python3
"""
The Baking Kaur - repair double(+)-encoded UTF-8 ("mojibake") across the FULL catalogue
(active + draft, ~1,235 products) and fix seo.title/product-title mismatches.

WHY (CLAUDE.md "Live defects" #1)
  /products/motu-patlu-designer-birthday-cake-meerut has an H1 of "Motu Patlu Designer
  Birthday Cake" but a <title> naming a different cake ("Celestial Charm"), plus mojibake.
  Google shows the wrong product name today. 8 known mojibake drafts + 1 live mismatch
  surfaced incidentally in earlier phases - this sweeps the full catalogue for both
  defects across title / seo.title / seo.description / descriptionHtml.

  seo-ops/title_utils.py already carries mojibake DETECTION (MOJI, is_broken()) from an
  earlier pass but was never wired into a repair script ("kept as a utility for future
  imports" - this is that import). What was missing is REPAIR, not detection: for
  descriptionHtml (real body content) the instruction is "repair encoding, never strip" -
  is_broken() alone would only tell you to discard/rebuild, which is not an option for
  real content.

HOW REPAIR WORKS
  This store's corruption is UTF-8 bytes mis-decoded as a single-byte Western encoding
  (Latin-1/Windows-1252 family), one or more times in a row (double- or triple-encoded),
  matching the shape of the corrupted forms already found and hand-mapped in
  assets/custom.js's client-side cleanup script. Latin-1 (not cp1252) is used for the
  byte<->char step deliberately: it is a total bijection over all 256 byte values (cp1252
  leaves several bytes, e.g. 0x9D, undefined and raises on real data). The reverse of a
  single "decode UTF-8 bytes as Latin-1" mistake is "encode the resulting text back to
  Latin-1 bytes, decode those bytes as UTF-8" - applied iteratively (bounded, stops as
  soon as it stops changing or would introduce U+FFFD) to unwind multiple layers at once.
  Verified via round-trip (original -> corrupt N times -> repair -> original) through 1-3
  layers, and confirmed a no-op on clean text (see test_fix_mojibake.py).

  If iterative repair would introduce a replacement character (U+FFFD) at any layer, the
  text is flagged UNREPAIRABLE rather than partially "fixed" - some corruption destroys
  information that can't be recovered algorithmically; guessing at it would violate
  "repair, never fabricate."

TITLE MISMATCH (the Motu Patlu-class defect)
  Separate from mojibake: an seo.title whose base (with the standard " - Eggless | Meerut"
  / " | Meerut" suffix stripped) doesn't correspond to the product's own (repaired) title
  at all - most likely a leftover from an earlier duplicate/rename. Detected via
  title_mismatch() and rebuilt with fix_seo_snippets.build_title() from the real product
  title, exactly like a from-scratch generation - never invented, always derived from the
  product's own current title field.

CRITICAL
  ProductInput.seo REPLACES wholesale - always send both title and description together
  when either changes. descriptionHtml is a separate top-level field, sent independently
  when it needs mojibake repair - it is never rebuilt or summarised, only repaired in place.

USAGE
  pip install requests
  export SHOPIFY_STORE=thebakingkaur.myshopify.com
  export SHOPIFY_TOKEN=shpat_xxx          # needs write_products, read_products
  python fix_mojibake.py                  # dry run, writes review CSV
  python fix_mojibake.py --apply          # writes to Shopify
"""
import argparse
import csv
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from typing import Dict, Iterator, List, Optional, Tuple

import requests

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from title_utils import MOJI  # noqa: E402
from fix_seo_snippets import build_title, esc  # noqa: E402

STORE = os.environ.get("SHOPIFY_STORE", "")
TOKEN = os.environ.get("SHOPIFY_TOKEN", "")
API_VERSION = "2025-01"
ENDPOINT = f"https://{STORE}/admin/api/{API_VERSION}/graphql.json"

# Fallback path: when no SHOPIFY_TOKEN is set (e.g. the MCP connector is down and no Admin
# API app token exists in this environment), fall back to the authenticated Shopify CLI's
# `store execute` command, which runs the same Admin GraphQL API under `shopify store auth`'s
# stored session - no token needs to be typed or stored by this script either way.
CLI_STORE = os.environ.get("SHOPIFY_STORE_CLI", "ae86ba-2a.myshopify.com")


def gql_via_cli(query: str, variables: Optional[Dict] = None) -> Dict:
    query_path = var_path = None
    try:
        with tempfile.NamedTemporaryFile(
            "w", suffix=".graphql", delete=False, encoding="utf-8"
        ) as qf:
            qf.write(query)
            query_path = qf.name
        shopify_bin = shutil.which("shopify") or "shopify"  # resolves .cmd shims on Windows
        cmd = [shopify_bin, "store", "execute", "--store", CLI_STORE,
               "--query-file", query_path, "--json"]
        if query.strip().startswith("mutation"):
            cmd.append("--allow-mutations")
        if variables:
            with tempfile.NamedTemporaryFile(
                "w", suffix=".json", delete=False, encoding="utf-8"
            ) as vf:
                json.dump(variables, vf)
                var_path = vf.name
            cmd += ["--variable-file", var_path]
        result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
        if result.returncode != 0:
            raise RuntimeError(f"shopify store execute failed: {result.stderr.strip()}")
        return json.loads(result.stdout)
    finally:
        for p in (query_path, var_path):
            if p and os.path.exists(p):
                os.unlink(p)

BATCH = 8  # HTTP/MCP layer gets unhappy well above ~15 aliased mutations
MAX_REPAIR_ITERS = 5

QUERY = """
query($first: Int!, $after: String) {
  products(first: $first, after: $after) {
    pageInfo { hasNextPage endCursor }
    nodes {
      id
      title
      handle
      descriptionHtml
      seo { title description }
    }
  }
}
"""

MUTATION_LINE_SEO = (
    'p{i}: productUpdate(product: {{id: "{gid}", '
    'seo: {{title: {title}, description: {desc}}}}}) '
    "{{ product {{ id }} userErrors {{ field message }} }}"
)
MUTATION_LINE_TITLE = (
    'p{i}: productUpdate(product: {{id: "{gid}", title: {title}}}) '
    "{{ product {{ id }} userErrors {{ field message }} }}"
)
MUTATION_LINE_DESC_HTML = (
    'p{i}: productUpdate(product: {{id: "{gid}", descriptionHtml: {html}}}) '
    "{{ product {{ id }} userErrors {{ field message }} }}"
)


def gql(query: str, variables: Optional[Dict] = None, attempt: int = 1) -> Dict:
    if not TOKEN:
        return gql_via_cli(query, variables)
    if not STORE:
        sys.exit("Set SHOPIFY_STORE and SHOPIFY_TOKEN environment variables.")
    resp = requests.post(
        ENDPOINT,
        headers={"X-Shopify-Access-Token": TOKEN, "Content-Type": "application/json"},
        json={"query": query, "variables": variables or {}},
        timeout=60,
    )
    if resp.status_code == 429 and attempt <= 6:
        time.sleep(2 ** attempt)
        return gql(query, variables, attempt + 1)
    resp.raise_for_status()
    body = resp.json()
    if "errors" in body:
        if attempt <= 6:
            time.sleep(2 ** attempt)
            return gql(query, variables, attempt + 1)
        raise RuntimeError(body["errors"])
    cost = body.get("extensions", {}).get("cost", {})
    if cost.get("throttleStatus", {}).get("currentlyAvailable", 1000) < 300:
        time.sleep(1.5)
    return body["data"]


def iter_all_products() -> Iterator[Dict]:
    """Every product regardless of status - the mojibake defect isn't confined to active."""
    cursor = None
    while True:
        data = gql(QUERY, {"first": 100, "after": cursor})["products"]
        for node in data["nodes"]:
            yield node
        if not data["pageInfo"]["hasNextPage"]:
            return
        cursor = data["pageInfo"]["endCursor"]


def looks_corrupted(text: str) -> bool:
    """Fast pre-filter before attempting the (slightly more expensive) repair round-trip.

    Deliberately permissive - flags any non-ASCII character, not just the specific
    2-3 layer forms already observed in this store's data (see MOJI in title_utils.py).
    Safety lives in repair_mojibake()'s round-trip, not here: genuine Unicode text above
    U+00FF (em-dash, curly quotes, ellipsis...) can't even be encoded as Latin-1, so the
    repair attempt fails cleanly and the text is returned untouched; a lone, correctly-used
    Latin-1-range character (e.g. a real degree sign) fails the UTF-8 re-decode step for
    the same reason - only an actual mis-decoded byte sequence survives the full round trip.
    """
    if not text:
        return False
    return any(ord(c) > 127 for c in text)


def is_definitely_corrupted(text: str) -> bool:
    """Specific corruption signature - unlike looks_corrupted(), NOT triggered by ordinary
    legitimate non-ASCII content (em-dashes, curly quotes, degree signs are all over this
    store's real descriptions). Used only to decide what's worth flagging for manual review
    after a repair attempt already failed to change anything - looks_corrupted() alone would
    flag most of the catalogue's genuinely fine copy as "unrepairable" noise.
    """
    if not text:
        return False
    if any(m in text for m in MOJI) or "\ufffd" in text:
        return True
    return any("\x80" <= c <= "\x9f" for c in text)


def repair_mojibake(text: str) -> Tuple[str, bool]:
    """Iteratively reverse UTF-8-decoded-as-cp1252 corruption.

    Returns (result, repaired). repaired is False when the text wasn't corrupted, or
    when repair would introduce U+FFFD (information genuinely lost - flagged, not
    guessed at) - in both cases `result` equals the original input, untouched.
    """
    if not looks_corrupted(text):
        return text, False

    current = text
    for _ in range(MAX_REPAIR_ITERS):
        try:
            nxt = current.encode("latin-1", errors="strict").decode("utf-8", errors="strict")
        except (UnicodeDecodeError, UnicodeEncodeError):
            break
        if "\ufffd" in nxt:
            break
        if nxt == current:
            break
        current = nxt

    if current == text or "\ufffd" in current:
        return text, False  # no safe progress made - leave untouched, flag for manual review
    return current, True


TITLE_SUFFIXES = (
    r"\s*-\s*Eggless\s*\|\s*Meerut\s*$",
    r"\s*\|\s*Meerut\s*$",
)


def strip_seo_suffix(seo_title: str) -> str:
    base = seo_title
    for pat in TITLE_SUFFIXES:
        base = re.sub(pat, "", base, flags=re.I)
    return base.strip()


def title_mismatch(seo_title: str, product_title: str) -> bool:
    """True if the seo title's base names a plainly different product than the real title.

    Conservative on purpose: only flags when neither string is a prefix of the other
    (after case-folding), so legitimate truncation or minor rewording never trips it -
    this only exists to catch the Motu-Patlu class of defect (a stale/unrelated name).
    """
    if not seo_title or not product_title:
        return False
    base = strip_seo_suffix(seo_title).lower().strip()
    real = product_title.lower().strip()
    if not base:
        return False
    return not (real.startswith(base) or base.startswith(real))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="write to Shopify")
    ap.add_argument("--limit", type=int, default=0, help="cap products processed")
    ap.add_argument("--csv", default="mojibake_review.csv")
    args = ap.parse_args()

    planned = []
    unrepairable = []
    scanned = 0

    for prod in iter_all_products():
        scanned += 1
        gid = prod["id"]
        handle = prod.get("handle", "")
        title = prod.get("title") or ""
        seo = prod.get("seo") or {}
        old_seo_title = seo.get("title") or ""
        old_seo_desc = seo.get("description") or ""
        old_desc_html = prod.get("descriptionHtml") or ""

        new_title, title_repaired = repair_mojibake(title)
        new_seo_title, seo_title_repaired = repair_mojibake(old_seo_title)
        new_seo_desc, seo_desc_repaired = repair_mojibake(old_seo_desc)
        new_desc_html, desc_html_repaired = repair_mojibake(old_desc_html)

        effective_title = new_title if title_repaired else title
        # Never derive a "fixed" seo.title from a product title that's still corrupted -
        # that would propagate the corruption instead of eliminating it.
        mismatched = not looks_corrupted(effective_title) and title_mismatch(
            new_seo_title if seo_title_repaired else old_seo_title, effective_title
        )
        rebuild_seo_title = mismatched
        if rebuild_seo_title:
            new_seo_title = build_title(effective_title)
            seo_title_repaired = True  # reuse the same "changed" flag for planning

        row = {
            "handle": handle,
            "id": gid,
            "title_before": title,
            "title_after": new_title if title_repaired else "",
            "seo_title_before": old_seo_title,
            "seo_title_after": new_seo_title if seo_title_repaired else "",
            "seo_title_rebuilt_mismatch": rebuild_seo_title,
            "seo_desc_before": old_seo_desc[:80],
            "seo_desc_after": (new_seo_desc[:80] if seo_desc_repaired else ""),
            "desc_html_repaired": desc_html_repaired,
        }

        # Flag genuinely corrupted text the repair round-trip couldn't resolve. Deliberately
        # NOT looks_corrupted() here - that's a permissive pre-filter (any non-ASCII), and
        # most of this catalogue's real copy legitimately uses em-dashes/curly quotes, which
        # would swamp this list with false positives for perfectly fine content.
        for label, before in (
            ("title", title), ("seo_title", old_seo_title),
            ("seo_desc", old_seo_desc), ("descriptionHtml", old_desc_html),
        ):
            if is_definitely_corrupted(before) and before == {
                "title": new_title, "seo_title": new_seo_title,
                "seo_desc": new_seo_desc, "descriptionHtml": new_desc_html,
            }[label]:
                unrepairable.append({"handle": handle, "id": gid, "field": label,
                                      "sample": before[:80]})

        if any([title_repaired, seo_title_repaired, seo_desc_repaired, desc_html_repaired]):
            planned.append({
                "gid": gid, "row": row,
                "new_title": new_title if title_repaired else None,
                "new_seo_title": new_seo_title if seo_title_repaired else old_seo_title,
                "new_seo_desc": new_seo_desc if seo_desc_repaired else old_seo_desc,
                "seo_changed": seo_title_repaired or seo_desc_repaired,
                "new_desc_html": new_desc_html if desc_html_repaired else None,
            })

        if args.limit and scanned >= args.limit:
            break

    print(f"Scanned {scanned} products (all statuses).")
    print(f"Planned fixes: {len(planned)}")
    print(f"Unrepairable (flagged, not touched): {len(unrepairable)}")

    with open(args.csv, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=[
            "handle", "id", "title_before", "title_after",
            "seo_title_before", "seo_title_after", "seo_title_rebuilt_mismatch",
            "seo_desc_before", "seo_desc_after", "desc_html_repaired",
        ])
        w.writeheader()
        for p in planned:
            w.writerow(p["row"])
    print(f"Review CSV written: {args.csv}")

    if unrepairable:
        with open("mojibake_unrepairable.csv", "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=["handle", "id", "field", "sample"])
            w.writeheader()
            w.writerows(unrepairable)
        print("Unrepairable CSV written: mojibake_unrepairable.csv (needs manual review)")

    if not args.apply:
        print("Dry run only. Re-run with --apply to write these changes to Shopify.")
        return

    for i in range(0, len(planned), BATCH):
        batch = planned[i:i + BATCH]
        lines = []
        for j, p in enumerate(batch):
            if p["new_title"] is not None:
                lines.append(MUTATION_LINE_TITLE.format(i=f"t{j}", gid=p["gid"],
                                                          title=esc(p["new_title"])))
            if p["seo_changed"]:
                lines.append(MUTATION_LINE_SEO.format(i=f"s{j}", gid=p["gid"],
                                                        title=esc(p["new_seo_title"]),
                                                        desc=esc(p["new_seo_desc"])))
            if p["new_desc_html"] is not None:
                lines.append(MUTATION_LINE_DESC_HTML.format(i=f"h{j}", gid=p["gid"],
                                                              html=esc(p["new_desc_html"])))
        mutation = "mutation {\n" + "\n".join(lines) + "\n}"
        result = gql(mutation)
        for key, val in result.items():
            errs = val.get("userErrors") or []
            if errs:
                print(f"ERROR {key}: {errs}")
        print(f"Batch {i // BATCH + 1}/{(len(planned) + BATCH - 1) // BATCH} applied.")


if __name__ == "__main__":
    main()

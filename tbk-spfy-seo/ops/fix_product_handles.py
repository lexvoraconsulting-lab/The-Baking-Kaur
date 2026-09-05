#!/usr/bin/env python3
"""
The Baking Kaur - replace opaque product handles with keyword handles.

WHY
  The bulk import left most of the catalogue on meaningless URLs:
      /products/b166      Royal Princess Baby Girl Birthday Cake
      /products/ch57      ...
      /products/hamper46  ...
      /products/40        ...
  A handle is the URL. "b166" tells a shopper and a crawler nothing.

SCOPE - ONLY OPAQUE HANDLES
  This deliberately does NOT touch handles that already read well
  ("eternal-story-anniversary-cake", "motu-patlu-designer-birthday-cake-meerut").
  Renaming those buys nothing and costs a redirect. Verified 20 Jul 2026 the store
  already carries 816 redirects (316 -> /collections/all) with 554 Not found +
  13 Soft 404 in GSC, so every additional redirect is a real cost, not free.

  Opaque = the whole handle is an import identifier: an optional known prefix
  followed by digits and nothing else (b166, ch57, h2, hamper46, avng3, 40).

STANDARD
  new handle = slug( clean_base(product title) )
      "Royal Princess Baby Girl Birthday Cake"
        -> royal-princess-baby-girl-birthday-cake
  clean_base (title_utils) strips trailing brand/locality noise first, so
  "X - The Baking Kaur, Meerut" does not become "x-the-baking-kaur-meerut".
  No locality suffix: locality belongs in the SEO title, not the URL.

REDIRECTS
  Applied with redirectNewHandle: true, so Shopify creates the 301 itself and
  printed QR codes / existing inbound links keep resolving. That is the whole
  reason this is survivable.

SAFETY
  - Writes product.handle only. Never touches title, SEO, description, variants,
    price, status or media.
  - Skips any product whose title carries mojibake - slugging corrupt text bakes
    the corruption into the URL permanently. Fix encoding first, rerun after.
  - Collision-safe against every existing handle in the shop and within the run.
  - --status lets you do DRAFT products first: zero live-SEO risk, 584 products.

USAGE
  pip install requests
  export SHOPIFY_STORE=thebakingkaur.myshopify.com
  export SHOPIFY_TOKEN=shpat_xxx          # needs write_products, read_products
  python fix_product_handles.py --selfcheck          # logic check, no network
  python fix_product_handles.py --status draft       # dry run -> review CSV
  python fix_product_handles.py --status draft --apply
  python fix_product_handles.py --status active      # only after drafts look right
"""
import argparse
import csv
import os
import re
import sys
import time
import unicodedata
from typing import Dict, Iterator, List, Optional

import requests

from title_utils import MOJI, clean_base

STORE = os.environ.get("SHOPIFY_STORE", "")
TOKEN = os.environ.get("SHOPIFY_TOKEN", "")
API_VERSION = "2025-01"
ENDPOINT = f"https://{STORE}/admin/api/{API_VERSION}/graphql.json"

BATCH = 8  # the HTTP layer gets unhappy well above ~15 aliased mutations

# Import identifiers seen in this catalogue. Documented in repoint_redirects.py:
#   h<n> hamper, ch<n> cake, avng<n> Avengers, floz<n> Frozen, uni<n> unicorn,
#   jg<n> jungle, b<n> and bare <n> bulk-imported cakes.
# Anchored: the WHOLE handle must be prefix+digits. "cocomelon-theme-cake-2" has
# hyphens and so is never opaque.
OPAQUE_HANDLE = re.compile(r"^(?:b|ch|h|hamper|avng|floz|uni|jg)?\d+$", re.I)

QUERY = """
query($first: Int!, $after: String, $q: String!) {
  products(first: $first, after: $after, query: $q) {
    pageInfo { hasNextPage endCursor }
    nodes { id handle title status }
  }
}
"""

MUTATION_LINE = (
    'p{i}: productUpdate(product: {{id: "{gid}", handle: {handle}}}, '
    "redirectNewHandle: true) "
    "{{ product {{ id handle }} userErrors {{ field message }} }}"
)


def gql(query: str, variables: Optional[Dict] = None, attempt: int = 1) -> Dict:
    if not STORE or not TOKEN:
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
    return body["data"]


def iter_products(search: str) -> Iterator[Dict]:
    cursor = None
    while True:
        data = gql(QUERY, {"first": 100, "after": cursor, "q": search})["products"]
        for node in data["nodes"]:
            yield node
        if not data["pageInfo"]["hasNextPage"]:
            return
        cursor = data["pageInfo"]["endCursor"]


def slugify(text: str) -> str:
    """Title -> Shopify handle. ASCII, lowercase, hyphen-separated."""
    s = unicodedata.normalize("NFKD", text or "")
    s = s.encode("ascii", "ignore").decode("ascii")
    s = re.sub(r"[^A-Za-z0-9]+", "-", s)
    return re.sub(r"-{2,}", "-", s).strip("-").lower()


def is_opaque(handle: str) -> bool:
    return bool(OPAQUE_HANDLE.match(handle or ""))


def has_mojibake(title: str) -> bool:
    return any(m in (title or "") for m in MOJI) or "Ã" in (title or "")


def plan_handle(title: str, taken: set) -> Optional[str]:
    """Return a free keyword handle for this title, or None if unusable."""
    base = slugify(clean_base(title))
    if not base:
        return None
    candidate = base
    n = 2
    while candidate in taken:
        candidate = f"{base}-{n}"
        n += 1
    return candidate


def esc(value: str) -> str:
    """GraphQL string literal - escape backslash and double quote."""
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def selfcheck() -> None:
    # ponytail: minimal runnable check - fails loudly if the logic regresses.
    assert is_opaque("b166") and is_opaque("ch57") and is_opaque("40")
    assert is_opaque("hamper46") and is_opaque("h2") and is_opaque("avng3")
    assert not is_opaque("motu-patlu-designer-birthday-cake-meerut")
    assert not is_opaque("eternal-story-anniversary-cake")
    assert not is_opaque("cocomelon-theme-cake-2")   # digits but hyphenated
    assert not is_opaque("")

    assert slugify("Royal Princess Baby Girl Birthday Cake") == \
        "royal-princess-baby-girl-birthday-cake"
    assert slugify("100% Eggless  Cake!!") == "100-eggless-cake"

    # clean_base strips brand/locality before slugging
    assert plan_handle("Blush Rose Cake - The Baking Kaur", set()) == "blush-rose-cake"

    # collisions get a numeric suffix, never silently overwrite
    taken = {"blush-rose-cake"}
    assert plan_handle("Blush Rose Cake", taken) == "blush-rose-cake-2"

    assert has_mojibake("Cake ÃƒÂ¢?? Eggless")
    assert not has_mojibake("Royal Princess Cake")
    print("fix_product_handles self-check: OK")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="write to Shopify")
    ap.add_argument("--status", default="draft", choices=["draft", "active", "any"],
                    help="which products to rename (default: draft = zero live risk)")
    ap.add_argument("--limit", type=int, default=0, help="cap products changed")
    ap.add_argument("--csv", default="product_handle_review.csv")
    ap.add_argument("--selfcheck", action="store_true", help="run logic asserts, no network")
    args = ap.parse_args()

    if args.selfcheck:
        selfcheck()
        return

    # Every handle in the shop, so a new handle can never collide with a product
    # we are not touching.
    all_products = list(iter_products("*"))
    taken = {p["handle"] for p in all_products}

    if args.status == "any":
        pool = all_products
    else:
        pool = [p for p in all_products if p["status"].lower() == args.status]

    planned, skipped = [], []
    for prod in pool:
        if not is_opaque(prod["handle"]):
            continue
        if has_mojibake(prod["title"]):
            skipped.append({"handle": prod["handle"], "title": prod["title"],
                            "reason": "mojibake in title - fix encoding first"})
            continue
        new = plan_handle(prod["title"], taken)
        if not new or new == prod["handle"]:
            skipped.append({"handle": prod["handle"], "title": prod["title"],
                            "reason": "title yields no usable slug"})
            continue
        taken.add(new)
        planned.append({"id": prod["id"], "status": prod["status"],
                        "old_handle": prod["handle"], "new_handle": new,
                        "title": prod["title"]})
        if args.limit and len(planned) >= args.limit:
            break

    with open(args.csv, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=["id", "status", "old_handle", "new_handle", "title"])
        w.writeheader()
        w.writerows(planned)

    print(f"products in shop : {len(all_products)}")
    print(f"in scope ({args.status:<6}): {len(pool)}")
    print(f"opaque -> rename : {len(planned)}")
    print(f"skipped          : {len(skipped)}")
    for s in skipped[:10]:
        print(f"  - {s['handle']}: {s['reason']}")
    print(f"review CSV       : {args.csv}")

    if not args.apply:
        print("\nDRY RUN - nothing written. Re-run with --apply once the CSV looks right.")
        return

    done = failed = 0
    for start in range(0, len(planned), BATCH):
        chunk = planned[start : start + BATCH]
        lines = [
            MUTATION_LINE.format(i=i, gid=p["id"], handle=esc(p["new_handle"]))
            for i, p in enumerate(chunk)
        ]
        result = gql("mutation {\n" + "\n".join(lines) + "\n}")
        for key, payload in result.items():
            errs = payload.get("userErrors") or []
            if errs:
                failed += 1
                print(f"  ! {key}: {errs}")
            else:
                done += 1
        print(f"  applied {done}/{len(planned)}")
        time.sleep(0.6)

    print(f"\ndone: {done} renamed, {failed} failed")


if __name__ == "__main__":
    main()

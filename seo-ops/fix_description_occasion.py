#!/usr/bin/env python3
"""
The Baking Kaur - fix mis-assigned "occasion" in product descriptions.

WHY
  The generated product descriptions weave an occasion into two places:
      opening : "Designed for anniversaries, {Name} is hand-finished ..."
      sizes   : "This anniversary cake is available in 1 kg, 1.5 kg ..."

  During the bulk import the occasion was frequently mis-assigned. Baby-girl,
  unicorn, butterfly and other kids/theme cakes were labelled "anniversaries"
  even though they are birthday cakes (verified live 23 Jul 2026 on
  /products/b158 "Dreamy Princess Baby Girl Cake" - "Designed for
  anniversaries ... This anniversary cake"). The products actually titled
  "... Anniversary Cake" and "... Wedding Cake" are correct and MUST be left
  alone.

DETECTION (high-confidence, no false positives)
  A product is mis-labelled when its description carries an occasion word that
  its TITLE contradicts:
      desc says anniversary  AND  title has no "anniversary"  -> birthday
      desc says wedding      AND  title has no "wedding"      -> birthday
  Real anniversary/wedding products keep the word in the title, so they are
  never touched. "Wedding Anniversary" titles contain both words and are
  skipped by both rules.

FIX
  Only the occasion phrasing is rewritten; design detail is preserved. The
  replacements are applied to the description string, and only for products
  the detection flags. Design words like "a princess theme in soft pastels"
  are never matched because we replace the whole token "anniversary"/"wedding",
  not "theme".

CRITICAL
  Writes product.descriptionHtml only. Does not touch title, handle, variants,
  price, SEO tags, status or media. Dry-run by default; review the CSV first.

USAGE
  pip install requests
  export SHOPIFY_STORE=thebakingkaur.myshopify.com
  export SHOPIFY_TOKEN=shpat_xxx          # needs write_products, read_products
  python fix_description_occasion.py              # dry run -> review CSV
  python fix_description_occasion.py --apply
"""
import argparse
import csv
import os
import re
import sys
import time
from typing import Dict, Iterator, List, Optional, Tuple

import requests

STORE = os.environ.get("SHOPIFY_STORE", "")
TOKEN = os.environ.get("SHOPIFY_TOKEN", "")
API_VERSION = "2025-01"
ENDPOINT = f"https://{STORE}/admin/api/{API_VERSION}/graphql.json"

BATCH = 8  # the HTTP layer gets unhappy well above ~15 aliased mutations

QUERY = """
query($first: Int!, $after: String) {
  products(first: $first, after: $after, query: "status:active") {
    pageInfo { hasNextPage endCursor }
    nodes { id title descriptionHtml }
  }
}
"""

MUTATION_LINE = (
    'p{i}: productUpdate(product: {{id: "{gid}", '
    "descriptionHtml: {desc}}}) "
    "{{ product {{ id }} userErrors {{ field message }} }}"
)

# (wrong occasion, replacement). Whole-word tokens only, case-insensitive on
# the leading letter so "Anniversary"/"anniversary" both convert.
REPLACERS: List[Tuple[re.Pattern, str]] = [
    (re.compile(r"\banniversaries\b"), "birthdays"),
    (re.compile(r"\bAnniversaries\b"), "Birthdays"),
    (re.compile(r"\banniversary\b"), "birthday"),
    (re.compile(r"\bAnniversary\b"), "Birthday"),
]
WEDDING_REPLACERS: List[Tuple[re.Pattern, str]] = [
    (re.compile(r"\bweddings and receptions\b"), "birthdays"),
    (re.compile(r"\bweddings\b"), "birthdays"),
    (re.compile(r"\bWeddings\b"), "Birthdays"),
    (re.compile(r"\bwedding\b"), "birthday"),
    (re.compile(r"\bWedding\b"), "Birthday"),
]


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


def iter_active() -> Iterator[Dict]:
    cursor = None
    while True:
        data = gql(QUERY, {"first": 100, "after": cursor})["products"]
        for node in data["nodes"]:
            yield node
        if not data["pageInfo"]["hasNextPage"]:
            return
        cursor = data["pageInfo"]["endCursor"]


def plan_fix(title: str, desc: str) -> Optional[str]:
    """Return the corrected description, or None if nothing needs changing."""
    if not desc:
        return None
    low_title = title.lower()
    new = desc
    # Anniversary mis-label: only when the title is NOT an anniversary cake.
    if "anniversary" not in low_title and "anniversaries" not in low_title:
        for pat, repl in REPLACERS:
            new = pat.sub(repl, new)
    # Wedding mis-label: only when the title is NOT a wedding cake.
    if "wedding" not in low_title:
        for pat, repl in WEDDING_REPLACERS:
            new = pat.sub(repl, new)
    return new if new != desc else None


def esc(value: str) -> str:
    """GraphQL string literal - escape backslash and double quote."""
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="write to Shopify")
    ap.add_argument("--limit", type=int, default=0, help="cap products changed")
    ap.add_argument("--csv", default="description_occasion_review.csv")
    args = ap.parse_args()

    planned = []
    scanned = 0
    for prod in iter_active():
        scanned += 1
        fixed = plan_fix(prod.get("title") or "", prod.get("descriptionHtml") or "")
        if fixed is None:
            continue
        planned.append({"id": prod["id"], "title": prod["title"], "new_desc": fixed})
        if args.limit and len(planned) >= args.limit:
            break

    with open(args.csv, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=["id", "title", "new_desc"])
        w.writeheader()
        w.writerows(planned)

    print(f"scanned active : {scanned}")
    print(f"need fixing    : {len(planned)}")
    print(f"review CSV     : {args.csv}")

    if not args.apply:
        print("\nDRY RUN - nothing written. Re-run with --apply once the CSV looks right.")
        return

    done = failed = 0
    for start in range(0, len(planned), BATCH):
        chunk = planned[start : start + BATCH]
        lines = [
            MUTATION_LINE.format(i=i, gid=p["id"], desc=esc(p["new_desc"]))
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

    print(f"\ndone: {done} updated, {failed} failed")


if __name__ == "__main__":
    main()

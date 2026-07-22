#!/usr/bin/env python3
"""
The Baking Kaur - rewrite SEO titles and meta descriptions on ACTIVE products.

WHY
  Search Console (3 months, verified 20 Jul 2026): 332K impressions, 3.58K clicks,
  1.1% CTR at average position 5.3. Position 5.3 should return 2-4%. The gap is the
  snippet, not the ranking.

  The legacy template still on a large share of active products:
      title: "{Name} in Meerut | The Baking Kaur"
      desc:  "{Name} - completely eggless, made to order. 9 flavours, 2 sizes. ..."

  Three defects: "1 sizes" grammar bug visible in live results; every product sharing
  one description skeleton so nothing differentiates them; and "| The Baking Kaur"
  costing ~18 chars to truncation when Google appends the site name anyway.

REPLACEMENT (title <= 60, description <= 155)
      title: "{Name} - Eggless | Meerut"
      desc:  "{hook} 100% eggless. From Rs.{price}. {n} size(s). Same-day & midnight
              delivery in Meerut."

NOTE ON HOOKS
  The hook is chosen from the product NAME first (any name containing "anniversary"
  gets the anniversary hook) and only then from productType. This deliberately avoids
  rewriting productType on hundreds of products just to get the right hook - the
  earlier handoff proposed mutating productType, which is a heavier data change than
  the problem requires.

CRITICAL
  ProductInput.seo is a nested object and REPLACES wholesale - it does not patch.
  Sending seo: {title} alone NULLS the description. This script always sends both.

USAGE
  pip install requests
  export SHOPIFY_STORE=thebakingkaur.myshopify.com
  export SHOPIFY_TOKEN=shpat_xxx          # needs write_products, read_products
  python fix_seo_snippets.py              # dry run, writes review CSV
  python fix_seo_snippets.py --apply      # writes to Shopify
"""
import argparse
import csv
import os
import re
import sys
import time
from typing import Dict, Iterator, List, Optional

import requests

STORE = os.environ.get("SHOPIFY_STORE", "")
TOKEN = os.environ.get("SHOPIFY_TOKEN", "")
API_VERSION = "2025-01"
ENDPOINT = f"https://{STORE}/admin/api/{API_VERSION}/graphql.json"

TITLE_MAX = 60
DESC_MAX = 155
BATCH = 8  # the MCP/HTTP layer gets unhappy well above ~15 aliased mutations

HOOKS = {
    "Wedding Cake": "Hand-finished tiers for the big day.",
    "Anniversary Cake": "Made to mark the years together.",
    "Theme Cake": "Custom-designed, hand-painted to your brief.",
    "Designer Cake": "Bespoke design, finished entirely by hand.",
    "Birthday Cake": "Made to order for the celebration.",
}
DEFAULT_HOOK = "Handcrafted to order in our Meerut atelier."

# Name-based hooks take precedence over productType.
NAME_HOOKS = [
    ("anniversary", "Made to mark the years together."),
    ("gender reveal", "Cut to reveal the colour inside."),
    ("strawberry", "Fresh strawberries, whipped cream, made to order."),
    ("kunafa", "Sold per piece - freshly made to order."),
    ("wedding", "Hand-finished tiers for the big day."),
]

QUERY = """
query($first: Int!, $after: String) {
  products(first: $first, after: $after, query: "status:active") {
    pageInfo { hasNextPage endCursor }
    nodes {
      id
      title
      productType
      priceRangeV2 { minVariantPrice { amount } }
      options(first: 5) { name optionValues { name } }
      seo { title description }
    }
  }
}
"""

MUTATION_LINE = (
    'p{i}: productUpdate(product: {{id: "{gid}", '
    'seo: {{title: {title}, description: {desc}}}}}) '
    "{{ product {{ id }} userErrors {{ field message }} }}"
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
    cost = body.get("extensions", {}).get("cost", {})
    if cost.get("throttleStatus", {}).get("currentlyAvailable", 1000) < 300:
        time.sleep(1.5)
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


def needs_fix(seo_title: Optional[str]) -> bool:
    """Legacy template is identified by the literal 'in Meerut' infix, or a null title."""
    if not seo_title:
        return True
    return "in Meerut" in seo_title


def size_count(options: List[Dict]) -> int:
    """Count DISTINCT sizes.

    Weights are stored in several formats in this catalogue - "1 kg", "1kg", "1 KG"
    and "2 k" all occur. A naive len() reports 4 sizes for a product that really has
    3 (observed on Luxury Exclusive Birthday Cake: 1kg / 1.5kg / 2kg / 1 kg).
    Normalise before counting or the description overstates the range.
    """
    for opt in options:
        if opt.get("name", "").strip().lower() in ("weight", "size"):
            seen = {
                re.sub(r"[^0-9a-z.]", "", (v.get("name") or "").lower())
                for v in (opt.get("optionValues") or [])
            }
            seen.discard("")
            if seen:
                return len(seen)
    return 1


def pick_hook(name: str, product_type: str) -> str:
    low = name.lower()
    for needle, hook in NAME_HOOKS:
        if needle in low:
            return hook
    return HOOKS.get((product_type or "").strip(), DEFAULT_HOOK)


def build_title(name: str) -> str:
    full = f"{name} - Eggless | Meerut"
    if len(full) <= TITLE_MAX:
        return full
    short = f"{name} | Meerut"
    if len(short) <= TITLE_MAX:
        return short
    # Truncate the name on a word boundary so " - Eggless | Meerut" still fits.
    budget = TITLE_MAX - len(" - Eggless | Meerut")
    clipped = name[:budget]
    if " " in clipped:
        clipped = clipped[: clipped.rfind(" ")]
    return f"{clipped.rstrip()} - Eggless | Meerut"


def build_desc(hook: str, price: float, sizes: int) -> str:
    unit = "size" if sizes == 1 else "sizes"
    desc = (
        f"{hook} 100% eggless. From Rs.{int(round(price)):,}. "
        f"{sizes} {unit}. Same-day & midnight delivery in Meerut."
    )
    if len(desc) > DESC_MAX:
        desc = desc[: DESC_MAX - 1].rstrip() + "."
    return desc


def esc(value: str) -> str:
    """GraphQL string literal."""
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="write to Shopify")
    ap.add_argument("--limit", type=int, default=0, help="cap products processed")
    ap.add_argument("--csv", default="seo_snippets_review.csv")
    args = ap.parse_args()

    planned = []
    scanned = 0
    for prod in iter_active():
        scanned += 1
        seo = prod.get("seo") or {}
        if not needs_fix(seo.get("title")):
            continue
        name = (prod.get("title") or "").strip()
        price = float(prod["priceRangeV2"]["minVariantPrice"]["amount"])
        sizes = size_count(prod.get("options") or [])
        hook = pick_hook(name, prod.get("productType") or "")
        planned.append(
            {
                "id": prod["id"],
                "name": name,
                "type": prod.get("productType") or "",
                "old_title": seo.get("title") or "",
                "new_title": build_title(name),
                "new_desc": build_desc(hook, price, sizes),
            }
        )
        if args.limit and len(planned) >= args.limit:
            break

    with open(args.csv, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(
            fh, fieldnames=["id", "name", "type", "old_title", "new_title", "new_desc"]
        )
        writer.writeheader()
        writer.writerows(planned)

    over_t = [p for p in planned if len(p["new_title"]) > TITLE_MAX]
    over_d = [p for p in planned if len(p["new_desc"]) > DESC_MAX]
    print(f"scanned active : {scanned}")
    print(f"need rewrite   : {len(planned)}")
    print(f"title > {TITLE_MAX}     : {len(over_t)}")
    print(f"desc  > {DESC_MAX}    : {len(over_d)}")
    print(f"review CSV     : {args.csv}")

    if not args.apply:
        print("\nDRY RUN - nothing written. Re-run with --apply once the CSV looks right.")
        return

    done = failed = 0
    for start in range(0, len(planned), BATCH):
        chunk = planned[start : start + BATCH]
        lines = [
            MUTATION_LINE.format(
                i=i, gid=p["id"], title=esc(p["new_title"]), desc=esc(p["new_desc"])
            )
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

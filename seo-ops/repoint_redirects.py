#!/usr/bin/env python3
"""
Repoint the remaining /collections/all catch-all redirects.

WHY THIS EXISTS
  Verified live 20 Jul 2026: the store has 816 URL redirects, of which **316 still
  target /collections/all**. Google treats a redirect to a generic catch-all listing
  as a SOFT 404 - which is precisely why "fixed" 404s keep reappearing in Search
  Console. GSC currently reports 554 Not found + 13 Soft 404 against this store.

  This walks every redirect still pointing at /collections/all, infers what the dead
  URL was about from its path, and repoints it at the closest real collection.

HONEST LIMITATION - READ THIS
  Repointing to a *category* is an improvement, not a cure. Google's own guidance is
  that a redirect should go to a closely-related page; a broad category page standing
  in for a deleted product can still be classified soft 404. Where a product is
  genuinely gone and has no near-equivalent, letting it return 404 is the correct
  outcome and NOT something to "fix".

  So: expect this to reduce the soft-404 count, not zero it. The paths that get the
  FALLBACK rule are the weakest - review those in the CSV before applying.

HANDLE SIGNALS FOUND IN THIS CATALOGUE
  h<n>      -> hamper, not cake        (h2, h5, h6, h37 ...)
  ch<n>     -> cake                    (ch11 ... ch298)
  avng<n>   -> Avengers theme
  floz<n>   -> "Flozan"/Frozen theme
  uni<n>    -> unicorn
  jg<n>     -> jungle
  <n>       -> bulk-imported cake, no semantic signal

USAGE
  pip install requests
  export SHOPIFY_STORE=thebakingkaur.myshopify.com
  export SHOPIFY_TOKEN=shpat_xxx        # needs write_online_store_navigation
  python repoint_redirects.py           # dry run -> redirect_repoint_review.csv
  python repoint_redirects.py --apply
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

CATCH_ALL = "/collections/all"
BATCH = 8

# (regex, destination collection handle, human label).
# ORDER MATTERS - first match wins. Specific before generic.
RULES: List[Tuple[str, str, str]] = [
    (r"diwali",                             "luxury-diwali-hampers",       "diwali hamper"),
    (r"hamper|^/products/h\d+$",            "cake-hampers",                "hamper"),
    (r"avng|avenger|super-?hero|spider|marvel", "designer-theme-cakes",    "superhero theme"),
    (r"floz|frozen",                        "designer-theme-cakes",        "frozen theme"),
    (r"unicorn|^/products/uni\d+$",         "unicorn",                     "unicorn"),
    (r"jungle|safari|^/products/jg\d+$|lion", "jungle-animal-theme",       "jungle"),
    (r"cocomelon|paw|kids|spiderman",       "kids-birthday-cakes-meerut",  "kids"),
    (r"butterfly",                          "butterfly",                   "butterfly"),
    (r"roblox",                             "roblox",                      "roblox"),
    (r"teddy",                              "teddy",                       "teddy"),
    (r"cricket|criciket",                   "criciket",                    "cricket"),
    (r"photo",                              "photo-cakes",                 "photo cake"),
    (r"strawberr|starberr|strawbeer|kunafa", "winter-strawberry-collection","strawberry"),
    (r"motu",                               "motu-patlu",                  "motu patlu"),
    (r"kpop",                               "kpop-cake",                   "kpop"),
    (r"baby-?girl|boy-or-girl|gender",      "baby-girl",                   "baby girl"),
    (r"wedding",                            "wedding-cakes",               "wedding"),
    (r"anniversar",                         "anniversary-cakes",           "anniversary"),
    (r"bow|ribbon",                         "ribbon-cake",                 "bow cake"),
    # Novelty / designer signals - all land in the designer & theme collection.
    (r"gym|makeup|cosmetic|fashionista|shopping|software|computer|engineer|"
     r"whisky|alcohol|jack-?daniel|starbucks|mercedes|audi|car|jersey|football|"
     r"ronaldo|messi|advocate|doctor|office|army|retirement|chartered|^/products/ca\b",
     "designer-theme-cakes", "designer/novelty theme"),
    (r"birthday",                           "birthday-cakes",              "birthday"),
    # Opaque bulk-import handles: ch12, b11, 98 - cake, but nothing more specific.
    (r"^/products/(ch|b)?\d+(\?|$)",        "cakes",                       "opaque handle"),
]
FALLBACK = ("cakes", "FALLBACK - no signal")

LIST_Q = """
query($first: Int!, $after: String) {
  urlRedirects(first: $first, after: $after, query: "target:/collections/all") {
    pageInfo { hasNextPage endCursor }
    nodes { id path target }
  }
}
"""

MUT_LINE = (
    'r{i}: urlRedirectUpdate(id: "{gid}", '
    'urlRedirect: {{path: {path}, target: {target}}}) '
    "{{ userErrors {{ field message }} }}"
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


def iter_catch_all() -> Iterator[Dict]:
    cursor = None
    while True:
        data = gql(LIST_Q, {"first": 250, "after": cursor})["urlRedirects"]
        for node in data["nodes"]:
            # Guard: the search filter is a token match, so confirm exact target.
            if node.get("target") == CATCH_ALL:
                yield node
        if not data["pageInfo"]["hasNextPage"]:
            return
        cursor = data["pageInfo"]["endCursor"]


def classify(path: str) -> Tuple[str, str]:
    """Return (collection_handle, reason) for a dead path."""
    low = path.lower()
    for pattern, handle, label in RULES:
        if re.search(pattern, low):
            return handle, label
    return FALLBACK


def esc(value: str) -> str:
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--csv", default="redirect_repoint_review.csv")
    args = ap.parse_args()

    planned = []
    for node in iter_catch_all():
        handle, reason = classify(node["path"])
        planned.append(
            {
                "id": node["id"],
                "path": node["path"],
                "old_target": node["target"],
                "new_target": f"/collections/{handle}",
                "reason": reason,
            }
        )

    with open(args.csv, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(
            fh, fieldnames=["id", "path", "old_target", "new_target", "reason"]
        )
        w.writeheader()
        w.writerows(planned)

    by_reason: Dict[str, int] = {}
    for p in planned:
        by_reason[p["reason"]] = by_reason.get(p["reason"], 0) + 1

    print(f"catch-all redirects found : {len(planned)}")
    for reason, n in sorted(by_reason.items(), key=lambda kv: -kv[1]):
        print(f"  {n:4}  {reason}")
    weak = by_reason.get(FALLBACK[1], 0)
    if weak:
        print(f"\n{weak} landed on the FALLBACK rule - review those rows in the CSV.")
    print(f"review CSV : {args.csv}")

    if not args.apply:
        print("\nDRY RUN - nothing written. Re-run with --apply once the CSV looks right.")
        return

    done = failed = 0
    for start in range(0, len(planned), BATCH):
        chunk = planned[start : start + BATCH]
        lines = [
            MUT_LINE.format(
                i=i, gid=p["id"], path=esc(p["path"]), target=esc(p["new_target"])
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

    print(f"\ndone: {done} repointed, {failed} failed")
    print("\nNext: in Search Console, hit Validate Fix on 'Not found (404)' and")
    print("'Soft 404'. Expect 4-8 weeks for counts to move - that lag is Google's.")


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""SEO title architecture v2 + identifier_exists, from the pre-change export.

TITLE ARCHITECTURE (evidence-based)
  PRODUCTS  : "{Clean Product Title} | The Baking Kaur"   <- no appended locality
  COLLECTIONS / LOCAL PAGES : carry "in Meerut" (handled separately, already largely correct)

Why products carry no locality:
  - only 81/607 (13%) product titles mention Meerut natively, so appending to
    100% imposed a template the catalogue does not support
  - product titles are effectively unique (606 distinct of 607) and average 32
    chars, so uniqueness is already carried by the name
  - a locality token repeated across 606 titles is a rewrite signal to Google
    and buys nothing on the map pack, which is driven by GBP/proximity/reviews
  - locality belongs where the query volume is: category and service pages
  Revisit per-product locality only when GSC impression data identifies genuine
  local-intent product queries. Guessing that subset without data is not evidence-based.
"""
import csv, re, json, collections
csv.field_size_limit(10**9)
BRAND = "The Baking Kaur"
CAP = 65

def clean_base(t):
    t = (t or '').strip()
    tails = (
        r'\s*[-–—|,]?\s*' + re.escape(BRAND) + r'\s*$',
        r'\s*[-–—|,]?\s*(?:in\s+)?Meerut\s*$',
        r'\s*[-–—|,.]+\s*$',
        r'\s+(?:by|from|at|for)\s*$',
    )
    for _ in range(6):
        b = t
        for p in tails:
            t = re.sub(p, '', t, flags=re.I)
        if t == b:
            break
    return re.sub(r'\s{2,}', ' ', t).strip()

def seo_title(product_title):
    b = clean_base(product_title)
    c = b + " | " + BRAND
    return c if len(c) <= CAP else b

rows = list(csv.DictReader(open('products_export_1.csv', encoding='utf-8-sig')))
prod = {}
for r in rows:
    h = r.get('Handle')
    if h and h not in prod:
        prod[h] = r
act = {h: r for h, r in prod.items() if (r.get('Status') or '').lower() == 'active'}

# id lookup comes from the live rollback.csv we already hold (handle isn't in it),
# so map via the earlier bulk export instead: use Handle -> we need GIDs.
gid = {}
for line in open('../seo-ops_ids.tsv', encoding='utf-8'):
    i, h = line.rstrip('\n').split('\t')
    gid[h] = i

out, skipped = [], 0
for h, r in act.items():
    if h not in gid:
        skipped += 1
        continue
    out.append((gid[h], h, r.get('Title') or '', seo_title(r.get('Title') or '')))

assert not skipped, "%d active products had no GID mapping" % skipped

# invariants
for i, h, pt, nt in out:
    assert nt.strip(), h
    assert 'Ã' not in nt and 'Â' not in nt, "mojibake " + h
    assert nt.count(BRAND) <= 1, "brand repeated " + h
    assert nt.lower().count('meerut') <= 1, "meerut repeated " + h
    assert not re.search(r'\b(?:by|from|at|for)\s*\|', nt), "dangling connector " + h
    assert len(nt) <= CAP, "too long " + h

titles = [t for _, _, _, t in out]
print('products            :', len(out))
print('with brand suffix   :', sum(1 for t in titles if t.endswith(BRAND)))
print('containing "Meerut" :', sum(1 for t in titles if 'meerut' in t.lower()), '  (was 606/607)')
print('len min/max/avg     : %d / %d / %.1f' % (min(map(len, titles)), max(map(len, titles)),
                                                sum(map(len, titles)) / len(titles)))
print('distinct titles     :', len(set(titles)))
json.dump([{"id": i, "handle": h, "title": nt} for i, h, _, nt in out],
          open('v2.json', 'w', encoding='utf-8'), ensure_ascii=False)
print()
print('--- 10 samples ---')
for i, h, pt, nt in out[:10]:
    print('  %-44s -> %s (%d)' % (pt[:42], nt, len(nt)))

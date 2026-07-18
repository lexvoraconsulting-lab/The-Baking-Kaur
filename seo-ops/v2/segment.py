# -*- coding: utf-8 -*-
"""Read-only. (a) Are any original SEO titles worth preserving?
   (b) Identifier segmentation A-E for Merchant Center."""
import csv, re, collections
csv.field_size_limit(10**9)
rows = list(csv.DictReader(open('products_export_1.csv', encoding='utf-8-sig')))
prod = {}
for r in rows:
    h = r.get('Handle')
    if h and h not in prod: prod[h] = r
act = {h: r for h, r in prod.items() if (r.get('Status') or '').lower() == 'active'}

MOJI = ('ÃƒÂ', 'Ã‚', 'Â¢', 'ÃÂ', 'Ã', 'Â')
def moj(s): return bool(s) and any(m in s for m in MOJI)

print('=== (a) ARE ANY ORIGINAL SEO TITLES WORTH PRESERVING? ===')
buckets = collections.Counter()
keepers = []
for h, r in act.items():
    t = (r.get('SEO Title') or '').strip()
    if not t:                                    buckets['empty'] += 1
    elif moj(t):                                 buckets['mojibake'] += 1
    elif t.lower().count('the baking kaur') > 1: buckets['brand duplicated'] += 1
    elif re.match(r'^[a-z0-9]+(-[a-z0-9]+){2,}', t): buckets['raw handle as title'] += 1
    elif len(t) > 70:                            buckets['over 70 chars'] += 1
    else:
        buckets['CLEAN — candidate to preserve'] += 1
        keepers.append((h, t))
for k, v in buckets.most_common(): print('  %-32s %d' % (k, v))
print()
print('  sample of clean originals:')
for h, t in keepers[:12]: print('    %-46s %s' % (h[:44], t))

print()
print('=== (b) IDENTIFIER SEGMENTATION (active) ===')
ven = collections.Counter((r.get('Vendor') or '(empty)') for r in act.values())
print('vendors:')
for k, v in ven.most_common(10): print('   %-28s %d' % (k, v))

bar = collections.defaultdict(int)
for r in rows:
    h = r.get('Handle')
    if h in act and (r.get('Variant Barcode') or '').strip(): bar[h] += 1
print()
print('active products with >=1 barcode/GTIN :', len(bar))
print('active products with MPN              :',
      sum(1 for r in act.values() if (r.get('Google Shopping / MPN') or '').strip()))
print('active products w/ Custom Product set :',
      sum(1 for r in act.values() if (r.get('Google: Custom Product (product.metafields.mm-google-shopping.custom_product)') or '').strip()))

# non-cake / potentially resold goods
NONCAKE = ('hamper', 'chocolate', 'balloon', 'flower', 'plant', 'mug', 'perfume', 'candle', 'dry fruit')
susp = [(h, r.get('Title'), r.get('Type')) for h, r in act.items()
        if any(w in ((r.get('Title') or '') + ' ' + (r.get('Type') or '')).lower() for w in NONCAKE)]
print()
print('active products whose name suggests packaged/resold goods:', len(susp))
for h, t, ty in susp[:15]: print('   %-34s %-46s type=%s' % (h[:32], (t or '')[:44], ty))

print()
print('=== TITLE ARCHITECTURE INPUTS ===')
print('active titles already containing "Meerut" :',
      sum(1 for r in act.values() if 'meerut' in (r.get('Title') or '').lower()))
print('active titles containing brand            :',
      sum(1 for r in act.values() if 'baking kaur' in (r.get('Title') or '').lower()))
lens = [len((r.get('Title') or '')) for r in act.values()]
print('product title length: min %d max %d avg %.1f' % (min(lens), max(lens), sum(lens)/len(lens)))
dupes = [t for t, c in collections.Counter((r.get('Title') or '').strip().lower()
         for r in act.values()).items() if c > 1]
print('duplicate product titles among active     :', len(dupes))

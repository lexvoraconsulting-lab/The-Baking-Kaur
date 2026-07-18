# -*- coding: utf-8 -*-
"""Generate combined batches: SEO title v2 + identifier_exists metafield.

The metafield is identical for every product, so it is passed ONCE as a GraphQL
variable ($mf) and referenced per alias. That keeps ~90 chars/product out of the
mutation body.

identifier_exists rationale (segmented from the export, not assumed):
  A custom-made / no manufacturer GTIN ....... 606  (all)
  B legitimate GTIN/barcode .................. 0
  C branded packaged / resold ................ 0   (vendor is "The Baking Kaur" on all 607)
  D has MPN .................................. 0
  E uncertain ................................ 0   (3 hampers reviewed -> A: the sold unit
                                                    is an in-house assembled hamper)
  => mm-google-shopping.custom_product = true is correct for every product here.
"""
import json, os

items = json.load(open('v2.json', encoding='utf-8'))
items = [x for x in items if x['handle'] != 'shopify-flow']   # test artifact, flagged for archive
SIZE = 75

def esc(s):
    return json.dumps(s, ensure_ascii=False)

os.makedirs('batches2', exist_ok=True)
for bi in range(0, len(items), SIZE):
    parts = []
    for i, it in enumerate(items[bi:bi + SIZE]):
        parts.append('a%d:productUpdate(product:{id:%s,seo:{title:%s},metafields:$mf}){userErrors{message}}'
                     % (i, esc(it['id']), esc(it['title'])))
    body = 'mutation($mf:[MetafieldInput!]!){' + ' '.join(parts) + '}'
    open('batches2/c%02d.graphql' % (bi // SIZE), 'w', encoding='utf-8').write(body)

n = len(os.listdir('batches2'))
sizes = [os.path.getsize('batches2/' + f) for f in sorted(os.listdir('batches2'))]
print('products :', len(items))
print('batches  :', n)
print('bytes    :', sum(sizes), ' largest:', max(sizes))
print()
print('variables (same for every batch):')
print(json.dumps({"mf": [{"namespace": "mm-google-shopping", "key": "custom_product",
                          "type": "boolean", "value": "true"}]}))

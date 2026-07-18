# -*- coding: utf-8 -*-
"""Emit aliased productUpdate mutations in batches (bulkOperationRunMutation is blocked).

Only writes `description` where it actually changed, which keeps the payload down.
"""
import json, csv, os

rows = list(csv.reader(open('rollback.csv', encoding='utf-8')))[1:]
SIZE = 50


def esc(s):
    return json.dumps(s, ensure_ascii=False)   # proper JSON/GraphQL string escaping


os.makedirs('batches', exist_ok=True)
n = 0
for bi in range(0, len(rows), SIZE):
    parts = []
    for i, (pid, old_t, old_d, new_t, new_d) in enumerate(rows[bi:bi + SIZE]):
        seo = 'title:' + esc(new_t)
        if new_d != old_d:                      # only when the description is genuinely changing
            seo += ',description:' + esc(new_d)
        parts.append('a%d:productUpdate(product:{id:%s,seo:{%s}}){userErrors{message}}'
                     % (i, esc(pid), seo))
    body = 'mutation{' + ' '.join(parts) + '}'
    open('batches/b%02d.graphql' % (bi // SIZE), 'w', encoding='utf-8').write(body)
    n += 1

sizes = [os.path.getsize('batches/' + f) for f in sorted(os.listdir('batches'))]
print('batches      :', n)
print('total bytes  :', sum(sizes))
print('largest batch:', max(sizes))
print('desc rewrites:', sum(1 for r in rows if r[4] != r[2]))

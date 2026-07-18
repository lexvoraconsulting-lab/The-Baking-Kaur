# -*- coding: utf-8 -*-
"""Build the SEO title/description repair set from the bulk export.

Writes:
  rollback.csv    id, old_title, old_description, new_title, new_description
  mutations.jsonl bulkOperationRunMutation input, one productUpdate per line
"""
import json, csv, collections, re
from rule import seo_title, seo_description, is_broken, MOJI, BRAND as BRAND_N

rows = [json.loads(l) for l in open('products.jsonl', encoding='utf-8') if l.strip()]

def desc_broken(d):
    return (not d) or (not d.strip()) or any(m in d for m in MOJI) or ("Ã" in d)

stats = collections.Counter()
changes = []
for r in rows:
    pid, ptitle = r['id'], r['title']
    seo = r.get('seo') or {}
    old_t, old_d = seo.get('title') or '', seo.get('description') or ''
    new_t = seo_title(ptitle)
    # only regenerate a description when the current one is corrupt or missing;
    # never overwrite a description that is merely templated (that is P2-21)
    new_d = seo_description(ptitle) if desc_broken(old_d) else old_d

    stats['total'] += 1
    if is_broken(old_t, ptitle): stats['title_broken'] += 1
    if any(m in old_t for m in MOJI) or 'Ã' in old_t: stats['title_mojibake'] += 1
    if old_t.lower().count('the baking kaur') > 1: stats['title_brand_dupe'] += 1
    if desc_broken(old_d): stats['desc_broken'] += 1

    if new_t != old_t or new_d != old_d:
        stats['will_change'] += 1
        changes.append((pid, old_t, old_d, new_t, new_d))

with open('rollback.csv', 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f)
    w.writerow(['id', 'old_seo_title', 'old_seo_description', 'new_seo_title', 'new_seo_description'])
    w.writerows(changes)

with open('mutations.jsonl', 'w', encoding='utf-8') as f:
    for pid, _, _, nt, nd in changes:
        f.write(json.dumps({"input": {"id": pid, "seo": {"title": nt, "description": nd}}},
                           ensure_ascii=False) + "\n")

# ---- invariants: nothing ships unless these hold -------------------------
for pid, ot, od, nt, nd in changes:
    assert nt and nt.strip(),               "empty title for " + pid
    assert not any(m in nt for m in MOJI),  "mojibake in new title " + pid
    assert 'Ã' not in nt and 'Ã' not in nd, "mojibake in new value " + pid
    assert nt.lower().count('the baking kaur') <= 1, "brand repeated " + pid
    assert len(nt) <= 65,                   "title too long " + pid
    # length only constrains descriptions WE generate; preserved ones are left as found
    assert nd == od or len(nd) <= 160,      "generated description too long " + pid
    assert not is_broken(nt, ''),           "new title still flagged broken " + pid
    # locality and brand must each appear at most once; catches the
    # "...The Baking Kaur, Meerut in Meerut" class of double-append
    assert nt.lower().count('meerut') <= 1, "Meerut repeated in " + pid + ": " + nt
    assert nt.count(BRAND_N) <= 1,          "brand repeated in " + pid + ": " + nt
    # a stripped brand must not leave its connector stranded ("... by in Meerut")
    assert not re.search(r'\b(?:by|from|at|for)\s+in\s+Meerut', nt), \
        "dangling connector in " + pid + ": " + nt

for k in ('total', 'title_broken', 'title_mojibake', 'title_brand_dupe', 'desc_broken', 'will_change'):
    print("%-18s %s" % (k, stats[k]))
print("unchanged        ", stats['total'] - stats['will_change'])
print("ALL INVARIANTS PASS")

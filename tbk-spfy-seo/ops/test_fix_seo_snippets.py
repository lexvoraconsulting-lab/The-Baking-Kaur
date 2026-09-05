# -*- coding: utf-8 -*-
import importlib.util, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

spec = importlib.util.spec_from_file_location(
    'f', r'F:\Shopify\The-Baking-Kaur\seo-ops\fix_seo_snippets.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

fails = []
def chk(cond, msg):
    if not cond:
        fails.append(msg)
        print('  FAIL:', msg)

# --- detection ---
chk(m.needs_fix(None), 'null title needs fix')
chk(m.needs_fix('Audi Car Theme Birthday Cake in Meerut | The Baking Kaur'), 'legacy detected')
chk(m.needs_fix('Alphabet and Number Theme Birthday Cake in Meerut'), 'truncated legacy detected')
chk(not m.needs_fix('Best Husband Cake Design - Eggless | Meerut'), 'new format skipped')
chk(not m.needs_fix('Elegant Two-Tier Wedding Anniversary Cake | Meerut'), 'short new format skipped')

# --- hook selection: name beats stored type ---
chk(m.pick_hook('Eternal Bond Heart Anniversary Cake', 'Theme Cake')
    == 'Made to mark the years together.', 'anniversary name overrides Theme Cake type')
chk(m.pick_hook('Luxury Gentleman Suit Cake', 'Designer Cake')
    == 'Bespoke design, finished entirely by hand.', 'designer type hook')
chk(m.pick_hook('Audi Car Theme Birthday Cake', 'Birthday Cake')
    == 'Made to order for the celebration.', 'birthday hook')
chk(m.pick_hook('Mystery Item', '') == m.DEFAULT_HOOK, 'fallback hook')

# --- titles ---
t = m.build_title('Personalized Photo Birthday Cake')
chk(t == 'Personalized Photo Birthday Cake - Eggless | Meerut', 'standard title: ' + t)
long_name = 'Elegant Floral Designer Cake for Birthdays and Anniversaries'
t2 = m.build_title(long_name)
chk(len(t2) <= 60, 'long title within 60: %s (%d)' % (t2, len(t2)))
chk(t2.endswith('| Meerut'), 'suffix retained: ' + t2)

# --- descriptions: the "1 sizes" grammar bug ---
d1 = m.build_desc('Romantic Whisper Wedding Cake', 'Hand-finished tiers for the big day.', 7000, 1)
chk('1 size.' in d1 and '1 sizes' not in d1, 'singular size: ' + d1)
d3 = m.build_desc('Luxe Crown Birthday Cake', 'Made to order for the celebration.', 1700, 3)
chk('3 sizes.' in d3, 'plural sizes')
chk('Rs.1,700.' in d3, 'thousands separator: ' + d3)
chk(len(m.build_desc('Motu Patlu Designer Birthday Cake',
                      'Custom-designed, hand-painted to your brief.', 15000, 3)) <= 155,
    'desc within 155')

# --- root-cause fix: description is anchored on the product name (Phase 7.4) ---
d_a = m.build_desc('Kundan Jewel Luxury Wedding Cake', 'Hand-finished tiers for the big day.', 1700, 3)
d_b = m.build_desc('Nawabi Elegance Wedding Cake', 'Hand-finished tiers for the big day.', 1700, 3)
chk(d_a != d_b, 'two products with identical hook/price/sizes get DIFFERENT descriptions: '
    + d_a + ' | ' + d_b)
chk(d_a.startswith('Kundan Jewel Luxury Wedding Cake'), 'description starts with the product name: ' + d_a)

# --- truncation priority: drop the hook before touching the name or facts ---
long_hook_name = 'Petal Symphony Luxury Wedding Cake'
d_trunc = m.build_desc(long_hook_name, 'Hand-finished tiers for the big day.', 1700, 3)
if len(long_hook_name) + 3 + len('Hand-finished tiers for the big day. 100% eggless. From Rs.1,700. 3 sizes. Same-day & midnight delivery in Meerut.') > 155:
    chk(long_hook_name in d_trunc, 'name preserved even when hook is dropped for length: ' + d_trunc)
chk(len(d_trunc) <= 155, 'truncated desc within 155')

# --- desc_needs_fix: detects the old nameless formula ---
chk(m.desc_needs_fix(None, 'Any Cake'), 'null description needs fix')
chk(m.desc_needs_fix('Made to mark the years together. 100% eggless. From Rs.1,700. 3 sizes. Same-day & midnight delivery in Meerut.', 'Eternal Bond Heart Anniversary Cake'),
    'old nameless-formula description needs fix')
chk(not m.desc_needs_fix('Eternal Bond Heart Anniversary Cake — Made to mark the years together. 100% eggless.', 'Eternal Bond Heart Anniversary Cake'),
    'new name-anchored description does not need fix')

# --- size counting (API always returns dicts) ---
def vals(*names):
    return [{'name': n} for n in names]

chk(m.size_count([{'name': 'Flavor', 'optionValues': vals('Chocolate', 'Vanilla')},
                  {'name': 'Weight', 'optionValues': vals('1 kg', '1.5 kg', '2 kg')}]) == 3,
    'counts Weight not Flavor')
chk(m.size_count([{'name': 'Flavor', 'optionValues': vals('Chocolate', 'Vanilla')}]) == 1,
    'fallback 1 size')
# Real defect seen live on Luxury Exclusive Birthday Cake: 3 sizes in 2 formats.
chk(m.size_count([{'name': 'Weight',
                   'optionValues': vals('1kg', '1.5kg', '2kg', '1 kg')}]) == 3,
    'dedupes "1kg" vs "1 kg" - naive len() would say 4')
chk(m.size_count([{'name': 'Weight', 'optionValues': vals('2kg', '2 KG')}]) == 1,
    'dedupes case and spacing')

# --- GraphQL string escaping ---
chk(m.esc('Sweet & Fresh') == '"Sweet & Fresh"', 'ampersand passes through')
quoted = m.esc('He said "hi"')
chk(quoted == '"He said \\"hi\\""', 'double quote escaped -> ' + quoted)
back = m.esc('a\\b')
chk(back == '"a\\\\b"', 'backslash escaped -> ' + back)
# Regression: descriptionHtml (real body content) contains literal newlines inside
# e.g. <ul>\n<li> blocks - an un-escaped raw newline inside a GraphQL string literal is
# a syntax error, not a formatting nit. Caught live during Phase 7.6's handle-leak fix.
nl = m.esc('<ul>\n<li>one</li>\n</ul>')
chk(nl == '"<ul>\\n<li>one</li>\\n</ul>"', 'newline escaped -> ' + repr(nl))
chk('\n' not in nl, 'no raw newline survives in the escaped output')

# --- NOTE: the old "LIVE PARITY" fixture here asserted byte-match against descriptions
# generated by the OLD nameless formula - that formula is exactly what Phase 7.4's
# root-cause fix replaces (it's what caused 84% of active products to share a duplicate
# description, see docs/SHOPIFY_SEO_REPORT.md). Asserting parity with it would just
# re-lock in the defect. Replaced with a batch-uniqueness check instead: every
# description this generator produces for a realistic mixed batch must be distinct.
print('\nBATCH UNIQUENESS (realistic mixed batch, same hook/price/sizes throughout):')
batch = [
    'Best Husband Cake Design', 'Romantic Whisper Wedding Cake',
    'Motu Patlu Designer Birthday Cake', 'Eternal Bond Heart Anniversary Cake',
    'Kundan Jewel Luxury Wedding Cake', 'Nawabi Elegance Wedding Cake',
    'Rajwada Heritage Wedding Cake', 'Maharani Royale Wedding Cake',
]
descs = [m.build_desc(n, 'Hand-finished tiers for the big day.', 1700, 3) for n in batch]
chk(len(set(descs)) == len(descs),
    'all %d descriptions unique despite identical hook/price/sizes' % len(batch))
for n, d in zip(batch, descs):
    print('  ' + n + ' -> ' + d)

print('\nFAILURES: %d' % len(fails))
sys.exit(1 if fails else 0)

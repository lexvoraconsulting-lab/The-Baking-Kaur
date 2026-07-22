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
d1 = m.build_desc('Hand-finished tiers for the big day.', 7000, 1)
chk('1 size.' in d1 and '1 sizes' not in d1, 'singular size: ' + d1)
d3 = m.build_desc('Made to order for the celebration.', 1700, 3)
chk('3 sizes.' in d3, 'plural sizes')
chk('Rs.1,700.' in d3, 'thousands separator: ' + d3)
chk(len(m.build_desc('Custom-designed, hand-painted to your brief.', 15000, 3)) <= 155,
    'desc within 155')

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

# --- parity with products the parallel session already fixed live ---
print('\nLIVE PARITY (must byte-match descriptions already on the store):')
cases = [
    ('Best Husband Cake Design', 'Theme Cake', 3000, 2,
     'Custom-designed, hand-painted to your brief. 100% eggless. From Rs.3,000. 2 sizes. Same-day & midnight delivery in Meerut.'),
    ('Romantic Whisper Wedding Cake', 'Wedding Cake', 7000, 1,
     'Hand-finished tiers for the big day. 100% eggless. From Rs.7,000. 1 size. Same-day & midnight delivery in Meerut.'),
    ('Motu Patlu Designer Birthday Cake', 'Theme Cake', 1700, 3,
     'Custom-designed, hand-painted to your brief. 100% eggless. From Rs.1,700. 3 sizes. Same-day & midnight delivery in Meerut.'),
    ('Eternal Bond Heart Anniversary Cake', 'Anniversary Cake', 2400, 3,
     'Made to mark the years together. 100% eggless. From Rs.2,400. 3 sizes. Same-day & midnight delivery in Meerut.'),
]
for name, typ, price, sizes, expect in cases:
    got = m.build_desc(m.pick_hook(name, typ), price, sizes)
    ok = (got == expect)
    if not ok:
        fails.append('parity ' + name)
    print(('  OK    ' if ok else '  DIFF  ') + name)
    if not ok:
        print('     got : ' + got)
        print('     want: ' + expect)

print('\nFAILURES: %d' % len(fails))
sys.exit(1 if fails else 0)

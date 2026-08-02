# -*- coding: utf-8 -*-
import importlib.util, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

spec = importlib.util.spec_from_file_location(
    'fm', r'F:\Shopify\The-Baking-Kaur\seo-ops\fix_mojibake.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

fails = []
def chk(cond, msg):
    if not cond:
        fails.append(msg)
        print('  FAIL:', msg)

def corrupt_once(s):
    return s.encode('utf-8').decode('latin-1')

# --- repair: no-op on clean text ---
clean, repaired = m.repair_mojibake('Best Husband Cake Design')
chk(clean == 'Best Husband Cake Design' and repaired is False, 'clean text untouched')
chk(m.repair_mojibake('')[1] is False, 'empty string untouched')

# --- repair: recovers 1/2/3-layer corruption of real characters used on this store ---
for original in ('…', '\u2019', '\u201c', '\u2014', '°'):
    c1 = corrupt_once(original)
    c2 = corrupt_once(c1)
    c3 = corrupt_once(c2)
    for depth, corrupted in ((1, c1), (2, c2), (3, c3)):
        out, ok = m.repair_mojibake(corrupted)
        chk(ok is True and out == original,
            'repairs depth-%d corruption of %r -> got %r' % (depth, original, out))

# --- is_definitely_corrupted: must NOT flag ordinary legitimate copy as corrupted ---
# Regression test for a real bug caught during the live dry-run: using looks_corrupted()
# (the permissive "any non-ASCII" pre-filter) for the post-repair "still broken" signal
# flagged every product with a real em-dash/curly quote as unrepairable - pure noise.
real_copy = 'White Love Designer Anniversary Cake — completely eggless, made to order.'
chk(m.is_definitely_corrupted(real_copy) is False,
    'a real em-dash in legitimate copy is not flagged as corrupted')
chk(m.is_definitely_corrupted('Simple clean text') is False, 'plain ASCII not flagged')
chk(m.is_definitely_corrupted(corrupt_once('’')) is True,
    'actual corruption is still flagged by the strict detector')
chk(m.looks_corrupted(real_copy) is True,
    'the permissive pre-filter DOES flag real em-dashes (by design - safety is in repair_mojibake, not here)')

# --- repair inside a realistic sentence, not just a bare character ---
sentence = 'Cake ' + '\u2014' + ' Eggless, made fresh'
corrupted_sentence = corrupt_once(sentence)
out, ok = m.repair_mojibake(corrupted_sentence)
chk(ok is True and out == sentence, 'repairs mojibake embedded in a full sentence')

# --- repair: HTML tags around corrupted text survive untouched ---
html = '<p>Cake ' + corrupt_once('\u2019') + 's Delight</p>'
out, ok = m.repair_mojibake(html)
chk(ok is True and out == '<p>Cake \u2019s Delight</p>', 'repairs mojibake inside HTML without breaking tags')

# --- repair: never introduces U+FFFD, never guesses ---
# A string containing an actual replacement character is unrecoverable - must be left alone.
lossy = 'Cake \ufffd Eggless'
out, ok = m.repair_mojibake(lossy)
chk(ok is False and out == lossy, 'text already containing U+FFFD is left untouched, not "fixed"')

# --- looks_corrupted ---
chk(m.looks_corrupted(corrupt_once('\u2019')) is True, 'flags corrupted text')
chk(m.looks_corrupted('Perfectly Clean Title') is False, 'does not flag clean text')
chk(m.looks_corrupted('') is False, 'empty string not flagged')

# --- title_mismatch: the Motu-Patlu class of defect ---
chk(m.title_mismatch('Celestial Charm - Eggless | Meerut', 'Motu Patlu Designer Birthday Cake') is True,
    'flags an seo title naming an entirely different product')
chk(m.title_mismatch('Motu Patlu Designer Birthday Cake - Eggless | Meerut',
                      'Motu Patlu Designer Birthday Cake') is False,
    'does not flag a correctly matching title')
chk(m.title_mismatch('Motu Patlu Designer | Meerut', 'Motu Patlu Designer Birthday Cake') is False,
    'does not flag legitimate truncation (seo base is a prefix of the real title)')
chk(m.title_mismatch('', 'Any Cake') is False, 'empty seo title is not a mismatch (that is needs_fix territory)')

# --- strip_seo_suffix ---
chk(m.strip_seo_suffix('Best Husband Cake Design - Eggless | Meerut') == 'Best Husband Cake Design',
    'strips the long suffix')
chk(m.strip_seo_suffix('Elegant Cake | Meerut') == 'Elegant Cake', 'strips the short suffix')
chk(m.strip_seo_suffix('No Suffix Here') == 'No Suffix Here', 'no-op when no suffix present')

print('\nFAILURES: %d' % len(fails))
sys.exit(1 if fails else 0)

# -*- coding: utf-8 -*-
import importlib.util, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
spec = importlib.util.spec_from_file_location(
    'f', r'F:\Shopify\The-Baking-Kaur\seo-ops\fix_description_occasion.py')
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)

fails = []
def chk(c, msg):
    if not c: fails.append(msg); print('  FAIL:', msg)

# 1. Baby-girl cake mislabelled anniversary -> fixed to birthday
d = m.plan_fix("Dreamy Princess Baby Girl Cake",
    "<p>Designed for anniversaries, Dreamy Princess Baby Girl Cake is hand-finished.</p>"
    "<p>This anniversary cake is available in 1 kg.</p>")
chk(d and "Designed for birthdays," in d, "opening occasion fixed")
chk(d and "This birthday cake is available" in d, "sizes occasion fixed")
chk(d and "anniversary" not in d.lower(), "no anniversary left")

# 2. Design word "princess theme" and "theme" must survive untouched
d2 = m.plan_fix("Cute Doll Theme Girl Baby Cake",
    "<p>It carries a princess theme in soft pastels.</p>"
    "<p>This anniversary cake is available.</p>")
chk(d2 and "a princess theme in soft pastels" in d2, "design 'theme' preserved")
chk(d2 and "This birthday cake" in d2, "theme-page occasion still fixed")

# 3. GENUINE anniversary product -> must NOT be touched
d3 = m.plan_fix("Anniversary Eternal Bloom Cake",
    "<p>This anniversary cake is available in 1 kg.</p>")
chk(d3 is None, "genuine anniversary cake untouched")

# 4. GENUINE wedding product -> must NOT be touched
d4 = m.plan_fix("Kundan Jewel Luxury Wedding Cake",
    "<p>one of our weddings and receptions designs. This wedding cake is available.</p>")
chk(d4 is None, "genuine wedding cake untouched")

# 5. Wedding-Anniversary title contains both -> untouched by both rules
d5 = m.plan_fix("Wedding Anniversary Celebration Cake",
    "<p>This anniversary cake. This wedding cake.</p>")
chk(d5 is None, "wedding-anniversary title untouched")

# 6. Correct birthday product -> no change
d6 = m.plan_fix("Unicorn Theme Birthday Cake",
    "<p>Built for birthdays. This birthday cake is available.</p>")
chk(d6 is None, "already-correct birthday untouched")

# 7. "made-to-order anniversary cake" opener variant
d7 = m.plan_fix("Pink Butterfly Cake for Girls",
    "<p>A made-to-order anniversary cake, Pink Butterfly Cake for Girls is finished by hand.</p>")
chk(d7 and "A made-to-order birthday cake," in d7, "opener variant fixed")

print("\nFAILURES: %d" % len(fails))
sys.exit(1 if fails else 0)

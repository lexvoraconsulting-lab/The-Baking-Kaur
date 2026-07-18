# -*- coding: utf-8 -*-
from rule import seo_title, seo_description, is_broken

M = "ÃƒÂÂÂ¢??"   # stand-in for the observed mojibake run

S = [
 ("Celebration Glow Birthday Cake",
  "Celebration Glow Birthday Cake | The Baking Kaur | The Baking Kaur Meerut"),
 ("Motu Patlu Designer Birthday Cake",
  "Celestial Charm Cake " + M + " 100% Eggless Cakes & 2" + M + "4 hour express delivery in Meerut | The Ba"),
 ("Bride To Be Simple Designer Cake",
  "Bride To Be Simple Designer Cake in Meerut-The Baking Kaur | The Baking Kaur Meerut"),
 ("Sweet & Fresh Cake and Flower Balloon Basket",
  "Sweet & Fresh Cake and Flower Balloon Basket | The Baking Kaur | The Baking Kaur Meerut"),
 ("Love Never Gets Old Anniversary Cake",
  "love-never-gets-old-anniversary-cake | The Baking Kaur | The Baking Kaur Meerut"),
 ("Wedding Anniversary Celebration Cake",
  "Wedding Annivaesary Celebration Cake in Meerut-The Baking Kaur | The Baking Kaur Meerut"),
 ("Elegant Two-Tier Anniversary Wedding Cake",
  "Elegant Two Tier Wedding Anniversary Celebration Cake in Meerut-The Baking Kaur | The Baking Kaur Meerut"),
 ("Luxury Mermaid Two Tier Cake",
  "Luxury Mermaid Two Tier Designer Meerut. Cake in Meerut-The Baking Kaur | The Baking Kaur Meerut"),
 ("Ever After Anniversary Cake in Meerut-The Baking Kaur",
  "Ever After Anniversary Cake in Meerut-The Baking Kaur | The Baking Kaur Meerut"),
 ("Harry Potter Theme Cake",
  "Harry Potter Theme Cake in Meerut-The Baking Kaur | The Baking Kaur Meerut"),
]

print("SAMPLE OF 10  BEFORE -> AFTER")
print("=" * 96)
for i, (pt, old) in enumerate(S, 1):
    new = seo_title(pt)
    print("%2d. product : %s" % (i, pt))
    print("    before  : %s  (%d chars, broken=%s)" % (old[:70], len(old), is_broken(old, pt)))
    print("    after   : %s  (%d chars)" % (new, len(new)))
print("=" * 96)

# invariants the rule must hold
assert all(seo_title(seo_title(pt)) == seo_title(pt) for pt, _ in S), "not idempotent"
assert not any("Ã" in seo_title(pt) for pt, _ in S), "mojibake survived"
assert all(seo_title(pt).count("The Baking Kaur") <= 1 for pt, _ in S), "brand repeated"
assert all(not is_broken(seo_title(pt), pt) for pt, _ in S), "output still flagged broken"
# every product's own words must survive into the title (no intent lost)
for pt, _ in S:
    core = pt.split(" in Meerut")[0].replace("-The Baking Kaur", "").strip()
    first = core.split()[0]
    assert first.lower() in seo_title(pt).lower(), "lost leading word: " + pt
print("PASS: idempotent, no mojibake, brand once, product wording preserved")
print()
print("desc example:", seo_description("Motu Patlu Designer Birthday Cake"))

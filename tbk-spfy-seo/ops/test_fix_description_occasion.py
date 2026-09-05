# -*- coding: utf-8 -*-
from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path

if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

script_dir = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("f", script_dir / "fix_description_occasion.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


class TestFixDescriptionOccasion(unittest.TestCase):
    def test_all_cases(self):
        # 1. Baby-girl cake mislabelled anniversary -> fixed to birthday
        d = m.plan_fix(
            "Dreamy Princess Baby Girl Cake",
            "<p>Designed for anniversaries, Dreamy Princess Baby Girl Cake is hand-finished.</p>"
            "<p>This anniversary cake is available in 1 kg.</p>",
        )
        self.assertTrue(d and "Designed for birthdays," in d, "opening occasion fixed")
        self.assertTrue(d and "This birthday cake is available" in d, "sizes occasion fixed")
        self.assertTrue(d and "anniversary" not in d.lower(), "no anniversary left")

        # 2. Design word "princess theme" and "theme" must survive untouched
        d2 = m.plan_fix(
            "Cute Doll Theme Girl Baby Cake",
            "<p>It carries a princess theme in soft pastels.</p>"
            "<p>This anniversary cake is available.</p>",
        )
        self.assertTrue(d2 and "a princess theme in soft pastels" in d2, "design 'theme' preserved")
        self.assertTrue(d2 and "This birthday cake" in d2, "theme-page occasion still fixed")

        # 3. GENUINE anniversary product -> must NOT be touched
        d3 = m.plan_fix(
            "Anniversary Eternal Bloom Cake",
            "<p>This anniversary cake is available in 1 kg.</p>",
        )
        self.assertIsNone(d3, "genuine anniversary cake untouched")

        # 4. GENUINE wedding product -> must NOT be touched
        d4 = m.plan_fix(
            "Kundan Jewel Luxury Wedding Cake",
            "<p>one of our weddings and receptions designs. This wedding cake is available.</p>",
        )
        self.assertIsNone(d4, "genuine wedding cake untouched")

        # 5. Wedding-Anniversary title contains both -> untouched by both rules
        d5 = m.plan_fix(
            "Wedding Anniversary Celebration Cake",
            "<p>This anniversary cake. This wedding cake.</p>",
        )
        self.assertIsNone(d5, "wedding-anniversary title untouched")

        # 6. Correct birthday product -> no change
        d6 = m.plan_fix(
            "Unicorn Theme Birthday Cake",
            "<p>Built for birthdays. This birthday cake is available.</p>",
        )
        self.assertIsNone(d6, "already-correct birthday untouched")

        # 7. "made-to-order anniversary cake" opener variant
        d7 = m.plan_fix(
            "Pink Butterfly Cake for Girls",
            "<p>A made-to-order anniversary cake, Pink Butterfly Cake for Girls is finished by hand.</p>",
        )
        self.assertTrue(d7 and "A made-to-order birthday cake," in d7, "opener variant fixed")


if __name__ == "__main__":
    unittest.main()

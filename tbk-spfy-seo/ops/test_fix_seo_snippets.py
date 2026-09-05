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
spec = importlib.util.spec_from_file_location("f", script_dir / "fix_seo_snippets.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


def vals(*names):
    return [{"name": n} for n in names]


class TestFixSeoSnippets(unittest.TestCase):
    def test_needs_fix(self):
        self.assertTrue(m.needs_fix(None))
        self.assertTrue(m.needs_fix("Audi Car Theme Birthday Cake in Meerut | The Baking Kaur"))
        self.assertTrue(m.needs_fix("Alphabet and Number Theme Birthday Cake in Meerut"))
        self.assertFalse(m.needs_fix("Best Husband Cake Design - Eggless | Meerut"))
        self.assertFalse(m.needs_fix("Elegant Two-Tier Wedding Anniversary Cake | Meerut"))

    def test_pick_hook(self):
        self.assertEqual(
            m.pick_hook("Eternal Bond Heart Anniversary Cake", "Theme Cake"),
            "Made to mark the years together.",
        )
        self.assertEqual(
            m.pick_hook("Luxury Gentleman Suit Cake", "Designer Cake"),
            "Bespoke design, finished entirely by hand.",
        )
        self.assertEqual(
            m.pick_hook("Audi Car Theme Birthday Cake", "Birthday Cake"),
            "Made to order for the celebration.",
        )
        self.assertEqual(m.pick_hook("Mystery Item", ""), m.DEFAULT_HOOK)

    def test_titles(self):
        t = m.build_title("Personalized Photo Birthday Cake")
        self.assertEqual(t, "Personalized Photo Birthday Cake - Eggless | Meerut")
        long_name = "Elegant Floral Designer Cake for Birthdays and Anniversaries"
        t2 = m.build_title(long_name)
        self.assertLessEqual(len(t2), 60)
        self.assertTrue(t2.endswith("| Meerut"))

    def test_descriptions_formatting(self):
        d1 = m.build_desc("Romantic Whisper Wedding Cake", "Hand-finished tiers for the big day.", 7000, 1)
        self.assertIn("1 size.", d1)
        self.assertNotIn("1 sizes", d1)
        d3 = m.build_desc("Luxe Crown Birthday Cake", "Made to order for the celebration.", 1700, 3)
        self.assertIn("3 sizes.", d3)
        self.assertIn("Rs.1,700.", d3)
        self.assertLessEqual(
            len(
                m.build_desc(
                    "Motu Patlu Designer Birthday Cake",
                    "Custom-designed, hand-painted to your brief.",
                    15000,
                    3,
                )
            ),
            155,
        )

    def test_descriptions_anchored_and_unique(self):
        d_a = m.build_desc("Kundan Jewel Luxury Wedding Cake", "Hand-finished tiers for the big day.", 1700, 3)
        d_b = m.build_desc("Nawabi Elegance Wedding Cake", "Hand-finished tiers for the big day.", 1700, 3)
        self.assertNotEqual(d_a, d_b)
        self.assertTrue(d_a.startswith("Kundan Jewel Luxury Wedding Cake"))

        batch = [
            "Best Husband Cake Design",
            "Romantic Whisper Wedding Cake",
            "Motu Patlu Designer Birthday Cake",
            "Eternal Bond Heart Anniversary Cake",
            "Kundan Jewel Luxury Wedding Cake",
            "Nawabi Elegance Wedding Cake",
            "Rajwada Heritage Wedding Cake",
            "Maharani Royale Wedding Cake",
        ]
        descs = [m.build_desc(n, "Hand-finished tiers for the big day.", 1700, 3) for n in batch]
        self.assertEqual(len(set(descs)), len(descs))

    def test_desc_needs_fix(self):
        self.assertTrue(m.desc_needs_fix(None, "Any Cake"))
        self.assertTrue(
            m.desc_needs_fix(
                "Made to mark the years together. 100% eggless. From Rs.1,700. 3 sizes. Same-day & midnight delivery in Meerut.",
                "Eternal Bond Heart Anniversary Cake",
            )
        )
        self.assertFalse(
            m.desc_needs_fix(
                "Eternal Bond Heart Anniversary Cake — Made to mark the years together. 100% eggless.",
                "Eternal Bond Heart Anniversary Cake",
            )
        )

    def test_size_count(self):
        self.assertEqual(
            m.size_count(
                [
                    {"name": "Flavor", "optionValues": vals("Chocolate", "Vanilla")},
                    {"name": "Weight", "optionValues": vals("1 kg", "1.5 kg", "2 kg")},
                ]
            ),
            3,
        )
        self.assertEqual(
            m.size_count([{"name": "Flavor", "optionValues": vals("Chocolate", "Vanilla")}]),
            1,
        )
        self.assertEqual(
            m.size_count(
                [{"name": "Weight", "optionValues": vals("1kg", "1.5kg", "2kg", "1 kg")}]
            ),
            3,
        )
        self.assertEqual(
            m.size_count([{"name": "Weight", "optionValues": vals("2kg", "2 KG")}]),
            1,
        )

    def test_graphql_escaping(self):
        self.assertEqual(m.esc("Sweet & Fresh"), '"Sweet & Fresh"')
        self.assertEqual(m.esc('He said "hi"'), '"He said \\"hi\\""')
        self.assertEqual(m.esc("a\\b"), '"a\\\\b"')
        nl = m.esc("<ul>\n<li>one</li>\n</ul>")
        self.assertEqual(nl, '"<ul>\\n<li>one</li>\\n</ul>"')
        self.assertNotIn("\n", nl)


if __name__ == "__main__":
    unittest.main()

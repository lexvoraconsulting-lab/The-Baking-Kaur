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
spec = importlib.util.spec_from_file_location("fm", script_dir / "fix_mojibake.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


def corrupt_once(s: str) -> str:
    return s.encode("utf-8").decode("latin-1")


class TestFixMojibake(unittest.TestCase):
    def test_repair_clean_text(self):
        clean, repaired = m.repair_mojibake("Best Husband Cake Design")
        self.assertEqual(clean, "Best Husband Cake Design")
        self.assertFalse(repaired)
        self.assertFalse(m.repair_mojibake("")[1])

    def test_repair_corrupted_characters(self):
        for original in ("…", "\u2019", "\u201c", "\u2014", "°"):
            c1 = corrupt_once(original)
            c2 = corrupt_once(c1)
            c3 = corrupt_once(c2)
            for depth, corrupted in ((1, c1), (2, c2), (3, c3)):
                out, ok = m.repair_mojibake(corrupted)
                self.assertTrue(ok, f"failed repair at depth {depth} for {original}")
                self.assertEqual(out, original)

    def test_is_definitely_corrupted(self):
        real_copy = "White Love Designer Anniversary Cake — completely eggless, made to order."
        self.assertFalse(m.is_definitely_corrupted(real_copy))
        self.assertFalse(m.is_definitely_corrupted("Simple clean text"))
        self.assertTrue(m.is_definitely_corrupted(corrupt_once("’")))
        self.assertTrue(m.looks_corrupted(real_copy))

    def test_repair_in_sentence_and_html(self):
        sentence = "Cake \u2014 Eggless, made fresh"
        corrupted_sentence = corrupt_once(sentence)
        out, ok = m.repair_mojibake(corrupted_sentence)
        self.assertTrue(ok)
        self.assertEqual(out, sentence)

        html = "<p>Cake " + corrupt_once("\u2019") + "s Delight</p>"
        out, ok = m.repair_mojibake(html)
        self.assertTrue(ok)
        self.assertEqual(out, "<p>Cake \u2019s Delight</p>")

        lossy = "Cake \ufffd Eggless"
        out, ok = m.repair_mojibake(lossy)
        self.assertFalse(ok)
        self.assertEqual(out, lossy)

    def test_looks_corrupted(self):
        self.assertTrue(m.looks_corrupted(corrupt_once("\u2019")))
        self.assertFalse(m.looks_corrupted("Perfectly Clean Title"))
        self.assertFalse(m.looks_corrupted(""))

    def test_title_mismatch(self):
        self.assertTrue(
            m.title_mismatch("Celestial Charm - Eggless | Meerut", "Motu Patlu Designer Birthday Cake")
        )
        self.assertFalse(
            m.title_mismatch(
                "Motu Patlu Designer Birthday Cake - Eggless | Meerut",
                "Motu Patlu Designer Birthday Cake",
            )
        )
        self.assertFalse(
            m.title_mismatch("Motu Patlu Designer | Meerut", "Motu Patlu Designer Birthday Cake")
        )
        self.assertFalse(m.title_mismatch("", "Any Cake"))

    def test_strip_seo_suffix(self):
        self.assertEqual(
            m.strip_seo_suffix("Best Husband Cake Design - Eggless | Meerut"),
            "Best Husband Cake Design",
        )
        self.assertEqual(m.strip_seo_suffix("Elegant Cake | Meerut"), "Elegant Cake")
        self.assertEqual(m.strip_seo_suffix("No Suffix Here"), "No Suffix Here")


if __name__ == "__main__":
    unittest.main()

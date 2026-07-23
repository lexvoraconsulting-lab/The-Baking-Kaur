#!/usr/bin/env python3
"""Reusable title-hygiene utilities for The Baking Kaur.

Extracted from the 2026-07 SEO title-repair scripts (`rule.py`, `v2/v2.py`) when
those one-off generators were removed. The catalogue is import-heavy and has a
documented mojibake-at-source issue (see SHOPIFY_ARCHITECTURE.md), so these
detectors/cleaners are worth keeping for the next import.

  clean_base(title) -> a clean SEO base, stripping trailing brand/locality noise
  is_broken(seo, product_title) -> True if an existing SEO title is corrupt/unusable
  MOJI -> substrings that flag double-encoded UTF-8

Not imported by the production scripts today; kept as a utility for future imports.
The v1/v2 SEO *title formats* these once fed are superseded — see docs/DECISIONS.md.
"""
import re

BRAND = "The Baking Kaur"

# Substrings that betray double-encoded UTF-8 ("mojibake"), seen live at the data source.
MOJI = ("Ãƒ", "Ã‚", "Â¢", "ÃÂ")


def clean_base(product_title: str) -> str:
    """Derive a clean base from a PRODUCT title, never from a broken SEO title.

    Product titles carry brand and locality in many pasted orders, e.g.
    'X-The Baking Kaur', 'X | The Baking Kaur Meerut', 'X The Baking Kaur, Meerut'.
    A single end-anchored strip misses cases where the brand sits BEFORE the
    locality, so peel trailing tokens repeatedly until the string stops changing.
    """
    t = (product_title or "").strip()
    tails = (
        r"\s*[-–—|,]?\s*" + re.escape(BRAND) + r"\s*$",   # trailing brand
        r"\s*[-–—|,]?\s*(?:in\s+)?Meerut\s*$",            # trailing locality
        r"\s*[-–—|,.]+\s*$",                              # trailing separators
        r"\s+(?:by|from|at|for)\s*$",                     # connector left dangling once
                                                          # the brand it introduced is gone
    )
    for _ in range(6):                                     # bounded; converges in <=3
        before = t
        for pat in tails:
            t = re.sub(pat, "", t, flags=re.I)
        if t == before:
            break
    return re.sub(r"\s{2,}", " ", t).strip()


def is_broken(seo: str, product_title: str = "") -> bool:
    """True if an existing SEO title is corrupt/unusable and should be rebuilt."""
    if not seo or not seo.strip():
        return True
    if any(m in seo for m in MOJI) or "Ã" in seo:          # double-encoded UTF-8
        return True
    if seo.lower().count(BRAND.lower()) > 1:               # brand duplicated
        return True
    if re.match(r"^[a-z0-9]+(-[a-z0-9]+){2,}", seo):       # raw handle used as title
        return True
    return False


if __name__ == "__main__":
    # ponytail: minimal runnable check — fails loudly if the logic regresses.
    assert clean_base("Blush Rose Cake - The Baking Kaur") == "Blush Rose Cake"
    assert clean_base("Bespoke Wedding Cake by The Baking Kaur, Meerut") == "Bespoke Wedding Cake"
    assert clean_base("X | The Baking Kaur Meerut") == "X"
    assert clean_base("Simple Cake") == "Simple Cake"          # nothing to strip
    assert is_broken("") is True
    assert is_broken("cocomelon-theme-cake-2") is True         # raw handle
    assert is_broken("Cake ÃƒÂ¢?? Eggless") is True            # mojibake
    assert is_broken("X | The Baking Kaur | The Baking Kaur") is True  # brand duplicated
    assert is_broken("Blush Rose Cake - Eggless | Meerut") is False
    print("title_utils self-check: OK")

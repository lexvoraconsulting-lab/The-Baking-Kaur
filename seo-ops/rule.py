import re
BRAND = "The Baking Kaur"

def clean_base(product_title):
    """Derive a clean SEO base from the PRODUCT title, never from the broken seo title.

    Product titles carry brand and locality in many pasted orders, e.g.
    'X-The Baking Kaur', 'X | The Baking Kaur Meerut', 'X The Baking Kaur, Meerut'.
    A single end-anchored strip misses the cases where the brand sits BEFORE the
    locality, so peel trailing tokens repeatedly until the string stops changing.
    """
    t = product_title.strip()
    tails = (
        r'\s*[-–—|,]?\s*' + re.escape(BRAND) + r'\s*$',   # trailing brand
        r'\s*[-–—|,]?\s*(?:in\s+)?Meerut\s*$',            # trailing locality
        r'\s*[-–—|,.]+\s*$',                              # trailing separators
    )
    for _ in range(6):                                     # bounded; converges in <=3
        before = t
        for pat in tails:
            t = re.sub(pat, '', t, flags=re.I)
        if t == before:
            break
    return re.sub(r'\s{2,}', ' ', t).strip()

def seo_title(product_title, cap=65):
    """Candidates in descending value. 'in Meerut' outranks the brand token:
    this is a local business and the local qualifier earns more than a brand
    repeat the searcher already sees in the URL."""
    b = clean_base(product_title)
    for c in (b + " in Meerut | " + BRAND,
              b + " in Meerut",
              b + " | " + BRAND,
              b):
        if len(c) <= cap:
            return c
    return b   # product name alone; never truncate mid-word

def seo_description(product_title, cap=160):
    b = clean_base(product_title)
    d = ("Order " + b + " in Meerut from " + BRAND +
         ". 100% eggless, freshly made, with same-day and midnight delivery.")
    if len(d) <= cap:
        return d
    d = "Order " + b + " in Meerut. 100% eggless, freshly made, same-day and midnight delivery."
    return d if len(d) <= cap else d[:cap].rsplit(' ', 1)[0]

MOJI = ("Ãƒ", "Ã‚", "Â¢", "ÃÂ")

def is_broken(seo, product_title):
    if not seo or not seo.strip():
        return True
    if any(m in seo for m in MOJI) or "Ã" in seo:      # double-encoded UTF-8
        return True
    if seo.lower().count(BRAND.lower()) > 1:                 # brand duplicated
        return True
    if re.match(r'^[a-z0-9]+(-[a-z0-9]+){2,}', seo):         # raw handle used as title
        return True
    return False

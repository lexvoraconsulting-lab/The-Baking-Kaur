# BROKEN LINKS DETAILED ANALYSIS
## Theme Files Scan Results

**Scan Date:** 2026-08-08  
**Severity:** CRITICAL - Footer & Navigation Broken  
**Impact:** Every footer link is broken - 404 errors on user click

---

## SUMMARY OF FINDINGS

**Files with Broken Links:**
1. `sections/footer.liquid` - 7 broken links
2. `sections/site-footer.liquid` - 8 broken links  
3. `sections/tbk-footer.liquid` - 7 broken links

**Total Broken Links Found:** 22+  
**Type:** All in footer/navigation sections  
**Impact:** Users can't reach About, Contact, FAQ, Delivery Info, etc.

---

## DETAILED BREAKDOWN BY FILE

### FILE 1: sections/footer.liquid

**Line 34:** `<a href="/pages/30-minute-cake-delivery-in-meerut-premium-reliable-service">`
- **Label:** 30-Minute Cake Delivery
- **Status:** ❌ PAGE DOES NOT EXIST
- **Fix:** Remove link or create page

**Line 45:** `<a href="/pages/about-us">`
- **Label:** About Us  
- **Status:** ❌ MISSING PAGE
- **Issue:** Page never created in Shopify
- **Fix:** Create page with handle `about-us`

**Line 46:** `<a href="/pages/contact">`
- **Label:** Contact Us
- **Status:** ❌ MISSING PAGE
- **Issue:** Page never created
- **Fix:** Create page with handle `contact`

**Line 48:** `<a href="/pages/frequently-asked-questions-faqs">`
- **Label:** FAQ
- **Status:** ❌ DOES NOT MATCH ANY PAGE
- **Issue:** No page with this handle exists (should be `/pages/faq`)
- **Fix:** Change to `/pages/faq` (after creating it)

**Line 49:** `<a href="/pages/cake-customization-guide">`
- **Label:** Customization Guide
- **Status:** ❌ DRAFT PAGE (404)
- **Issue:** Page exists but NOT PUBLISHED (publishedAt: null)
- **Fix:** Publish page via collectionUpdate

**Line 50:** `<a href="/pages/delivery-information">`
- **Label:** Delivery Information
- **Status:** ❌ DRAFT PAGE (404)
- **Issue:** Page exists but NOT PUBLISHED
- **Fix:** Publish page immediately

**Line 60:** `<a href="/pages/faq">`
- **Label:** FAQ (duplicate)
- **Status:** ❌ MISSING PAGE
- **Issue:** Page never created
- **Fix:** Create page with handle `faq`

**Line 74:** `<a href="/pages/contact">`
- **Label:** Contact Us (duplicate)
- **Status:** ❌ MISSING PAGE
- **Fix:** Create page

---

### FILE 2: sections/site-footer.liquid

**Line 75:** `<a href="/pages/about-us">`
- **Status:** ❌ MISSING
- **Fix:** Create page

**Line 76:** `<a href="/pages/why-choose-the-baking-kaur">`
- **Status:** ❌ DRAFT (404)
- **Issue:** Page exists but NOT published
- **Fix:** Publish page

**Line 77:** `<a href="/pages/contact">`
- **Status:** ❌ MISSING
- **Fix:** Create page

**Line 78:** `<a href="/pages/store-locator">`
- **Status:** ❌ DOES NOT EXIST
- **Issue:** No page created
- **Fix:** Remove link or create page

**Line 79:** `<a href="/pages/frequently-asked-questions-faqs">`
- **Status:** ❌ WRONG HANDLE
- **Fix:** Change to `/pages/faq`

**Line 86:** `<a href="/pages/delivery-information">`
- **Status:** ❌ DRAFT (404)
- **Fix:** Publish page

**Line 87:** `<a href="/pages/midnight-surprise-delivery">`
- **Status:** ❌ DRAFT (404)
- **Fix:** Publish page

**Line 88:** `<a href="/pages/cake-delivery-in-meerut">`
- **Status:** ✅ PUBLISHED (OK)
- **Fix:** No action

**Line 89:** `<a href="/pages/corporate-gifting-solutions">`
- **Status:** ❌ DRAFT (404)
- **Fix:** Publish page

**Line 90:** `<a href="/pages/gift-hampers">`
- **Status:** ✅ PUBLISHED (OK)
- **Fix:** No action

**Line 99:** `<a href="/pages/terms-and-conditions">`
- **Status:** ⚠️ USES SHOPIFY DEFAULT
- **Fix:** Use shop.policies or keep as is if Shopify handles it

**Line 101:** `<a href="/pages/return-refund-replacement-policy">`
- **Status:** ❌ DRAFT (404)
- **Issue:** Page exists but NOT published
- **Fix:** Publish page

**Line 126:** Privacy Policy (conditional)
- **Status:** ✅ USES SHOPIFY DEFAULT (OK)
- **Fix:** No action

**Line 127:** `<a href="/pages/terms-and-conditions">`
- **Status:** ⚠️ SHOPIFY DEFAULT
- **Fix:** May need to use shop.policies instead

---

### FILE 3: sections/tbk-footer.liquid

**Line 47:** `<a href="/pages/about">`
- **Label:** About Us
- **Status:** ❌ MISSING (wrong handle)
- **Issue:** Should be `/pages/about-us` (with hyphen)
- **Fix:** Create page with handle `about-us`

**Line 48:** `<a href="/pages/contact">`
- **Label:** Contact Us
- **Status:** ❌ MISSING
- **Fix:** Create page

**Line 50:** `<a href="/pages/careers">`
- **Label:** Careers
- **Status:** ❌ DOES NOT EXIST
- **Fix:** Remove link or create page if needed

**Line 57:** `<a href="/pages/shipping-policy">`
- **Label:** Shipping Policy
- **Status:** ❌ DOES NOT EXIST
- **Issue:** Should use Shopify's default shipping policy
- **Fix:** Use shop.policies.shipping_policy.url or change to `/pages/delivery-information`

**Line 58:** `<a href="/pages/privacy-policy">`
- **Label:** Privacy Policy
- **Status:** ❌ DOES NOT EXIST IN SHOPIFY
- **Issue:** Should use shop.policies.privacy_policy.url
- **Fix:** Change to use Shopify default

**Line 59:** `<a href="/pages/terms-of-service">`
- **Label:** Terms & Conditions
- **Status:** ❌ DOES NOT EXIST
- **Issue:** Should use Shopify's default
- **Fix:** Use shop.policies or link to return-refund-replacement-policy

**Line 60:** `<a href="/pages/faq">`
- **Label:** FAQ
- **Status:** ❌ MISSING
- **Fix:** Create page

**Line 327-338:** (Duplicate of above)
- **Status:** Same issues as lines 47-60
- **Fix:** Same fixes

---

## CATEGORIZED FIX LIST

### CATEGORY A: Publish Draft Pages (Highest Priority)
These pages exist but are NOT published:

1. ✅ `delivery-information` → Publish immediately
2. ✅ `why-choose-the-baking-kaur` → Publish immediately
3. ✅ `cake-customization-guide` → Publish immediately
4. ✅ `midnight-surprise-delivery` → Publish immediately
5. ✅ `corporate-gifting-solutions` → Publish immediately
6. ✅ `return-refund-replacement-policy` → Publish immediately

**Action:** Use GraphQL `collectionUpdate` to set `publishedAt: "2026-08-08T00:00:00Z"`

---

### CATEGORY B: Create Missing Pages (Critical)
These pages are referenced in navigation but don't exist:

1. ✅ `about-us` → Create immediately
2. ✅ `contact` → Create immediately
3. ✅ `faq` → Create immediately

**Action:** Use GraphQL `pageCreate` mutation

---

### CATEGORY C: Fix Navigation Links (High Priority)
Update footer links to use correct handles:

1. **footer.liquid, line 48:** `/pages/frequently-asked-questions-faqs` → `/pages/faq`
2. **site-footer.liquid, line 79:** `/pages/frequently-asked-questions-faqs` → `/pages/faq`
3. **tbk-footer.liquid, line 47:** `/pages/about` → `/pages/about-us`

**Action:** Edit theme files to fix handles

---

### CATEGORY D: Remove Non-Essential Links (Medium Priority)
These pages don't exist and aren't critical:

1. **footer.liquid, line 34:** Remove `/pages/30-minute-cake-delivery-in-meerut-premium-reliable-service`
2. **site-footer.liquid, line 78:** Remove `/pages/store-locator`
3. **tbk-footer.liquid, line 50:** Remove `/pages/careers` (unless you want to create it)

**Action:** Edit theme files to remove links or create pages if needed

---

### CATEGORY E: Use Shopify Policy Links (Medium Priority)
Replace custom page links with Shopify's default policies:

1. **site-footer.liquid, lines 99, 127:** Use shop.policies instead of `/pages/terms-and-conditions`
2. **tbk-footer.liquid, line 57:** Use shop.policies.shipping_policy.url instead of `/pages/shipping-policy`
3. **tbk-footer.liquid, line 58:** Use shop.policies.privacy_policy.url instead of `/pages/privacy-policy`

**Action:** Update theme files to use Liquid shop object

---

## AFFECTED THEME FILES NEEDING UPDATES

| File | Lines | Broken Links | Status |
|---|---|---|---|
| `sections/footer.liquid` | 34, 45-50, 60, 74 | 7+ | NEEDS UPDATES |
| `sections/site-footer.liquid` | 75-90, 99, 101, 126-127 | 8+ | NEEDS UPDATES |
| `sections/tbk-footer.liquid` | 47-60, 327-338 | 14 (with duplicates) | NEEDS UPDATES |

---

## COMPLETE FIX EXECUTION PLAN

### PHASE A: Publish All Draft Pages (30 minutes)
```graphql
# Publish all 6 draft pages with this mutation
mutation {
  page1: pageUpdate(input: {
    id: "gid://shopify/Page/115527647401"  # delivery-information
    publishedAt: "2026-08-08T00:00:00Z"
  })
  page2: pageUpdate(input: {
    id: "gid://shopify/Page/115527581865"  # why-choose-the-baking-kaur
    publishedAt: "2026-08-08T00:00:00Z"
  })
  # ... etc for remaining draft pages
}
```

### PHASE B: Create Missing Critical Pages (45 minutes)
```graphql
mutation {
  pageCreate(input: {
    title: "About Us | The Baking Kaur"
    handle: "about-us"
    bodyHtml: "About The Baking Kaur content..."
    publishedAt: "2026-08-08T00:00:00Z"
  })
  # ... similar for contact and faq
}
```

### PHASE C: Update Theme Files (1 hour)
Edit three footer files:
1. `sections/footer.liquid` - Fix 7+ links
2. `sections/site-footer.liquid` - Fix 8+ links
3. `sections/tbk-footer.liquid` - Fix 14 broken links

### PHASE D: Test All URLs (30 minutes)
- [ ] Verify each footer link returns 200
- [ ] Test on mobile and desktop
- [ ] Verify no 404 errors in browser console

---

## IMPACT ASSESSMENT

### Current State
- Users clicking footer links → 404 errors (22+)
- Cannot reach About, Contact, FAQ, Delivery Info
- Cannot contact support or get information
- Poor user experience + lost conversions

### After Fixes
- All 22+ footer links return 200
- Users can navigate properly
- All critical info pages accessible
- Improved user experience + conversion potential

### Revenue Impact
- Estimated 5-10% of visitors click footer links
- If 1% convert to customers, that's 50-100 lost customers/month (at 10k visitors/month)
- Lost revenue: ₹75,000-150,000/month

---

## EXECUTION TIMELINE

| Phase | Task | Duration | Status |
|---|---|---|---|
| A | Publish 6 draft pages | 30 min | READY |
| B | Create 3 critical pages | 45 min | READY |
| C | Update 3 theme files | 60 min | READY |
| D | Test all links | 30 min | READY |
| **TOTAL** | **Complete 404 Fix** | **2.5 hours** | **READY** |

---

## NEXT STEPS

1. Execute PHASE A immediately (publish draft pages)
2. Execute PHASE B immediately (create critical pages)
3. Execute PHASE C (update theme files with correct links)
4. Execute PHASE D (test all URLs)
5. Commit changes and push to live

**Estimated time to zero 404 errors: 2.5 hours**

---

**CRITICAL PRIORITY:** These are blocking customer support & information access. Fix before any other optimization.

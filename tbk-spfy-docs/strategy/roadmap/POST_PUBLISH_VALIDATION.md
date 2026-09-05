# POST-PUBLISH VALIDATION PLAN

**Purpose:** Verify all 6 pages are live, properly linked, and return 200 status  
**Timeline:** 15 minutes  
**Success Criteria:** All checks pass, 0 broken links, 0 orphan pages

---

## PRE-VALIDATION CHECKLIST

Before running validation:

- [ ] All 3 draft pages have been manually published in Shopify Admin
- [ ] Each page has content from PAGE_OPTIMIZATION_CONTENT.md
- [ ] Each page has schema markup (JSON-LD) added
- [ ] All pages were saved and published successfully
- [ ] Waited 2-3 minutes for Shopify to cache updates

---

## VALIDATION SUITE

### **SECTION 1: Page Status Verification (200 Status)**

**Test Command:**
```bash
# Test all 6 critical pages
curl -I https://thebakingkaur.com/pages/about-us
curl -I https://thebakingkaur.com/pages/contact
curl -I https://thebakingkaur.com/pages/frequently-asked-questions-faqs
curl -I https://thebakingkaur.com/pages/why-choose-the-baking-kaur
curl -I https://thebakingkaur.com/pages/delivery-information
curl -I https://thebakingkaur.com/pages/cake-customization-guide
```

**Expected Output for Each:**
```
HTTP/2 200
```

**Pass Criteria:**
- ✅ All 6 pages return HTTP 200 (not 404, not 503)
- ✅ No pages in draft state
- ✅ All pages accessible via HTTPS

**If Failed:**
- If 404: Page not published yet. Retry publishing via Shopify Admin.
- If 503: Shopify servers slow. Wait 5 minutes and retry.
- If draft: Check publishedAt timestamp in Shopify Admin.

---

### **SECTION 2: Draft Page Status Check**

**Verify no draft pages remain:**

```graphql
{
  pages(first: 100) {
    nodes {
      handle
      publishedAt
      title
    }
  }
}
```

**Expected Results:**
- ✅ why-choose-the-baking-kaur: publishedAt is NOT null
- ✅ delivery-information: publishedAt is NOT null
- ✅ cake-customization-guide: publishedAt is NOT null
- ✅ All 3 should show "2026-08-09" or current date

**Pass Criteria:**
- ✅ 0 draft pages in critical set
- ✅ All 6 pages have publishedAt timestamps
- ✅ No null publishedAt values

---

### **SECTION 3: Internal Link Validation**

**Test all internal collection links work:**

**From About Us page:**
```
✓ /collections/birthday-cakes → 200
✓ /collections/anniversary-cakes → 200
✓ /collections/wedding-cakes → 200
✓ /collections/designer-theme-cakes → 200
✓ /collections/photo-cakes → 200
✓ /collections/cake-hampers → 200
```

**From Contact page:**
```
✓ /collections/birthday-cakes → 200
✓ /collections/designer-theme-cakes → 200
✓ /collections/photo-cakes → 200
✓ /collections/wedding-cakes → 200
✓ /collections/cake-hampers → 200
✓ /pages/frequently-asked-questions-faqs → 200
```

**From FAQ page:**
```
✓ /pages/contact → 200
✓ /pages/about-us → 200
✓ /collections/birthday-cakes → 200
✓ /collections/anniversary-cakes → 200
✓ /collections/wedding-cakes → 200
✓ /collections/designer-theme-cakes → 200
✓ /collections/photo-cakes → 200
✓ /collections/cake-hampers → 200
✓ /collections/midnight-cake-delivery → 200
```

**Pass Criteria:**
- ✅ All collection links return 200
- ✅ All cross-page links work
- ✅ No 404 links anywhere
- ✅ WhatsApp link functions

---

### **SECTION 4: Navigation & Footer Validation**

**Verify pages are properly linked in navigation:**

**Footer Navigation Check:**
- [ ] "About Us" link → /pages/about-us (200)
- [ ] "Contact Us" link → /pages/contact (200)
- [ ] "FAQ" link → /pages/frequently-asked-questions-faqs (200)

**Header Navigation Check (if applicable):**
- [ ] Pages accessible via header menu
- [ ] No broken links in header

**Pass Criteria:**
- ✅ All 6 pages are either in footer or internally linked
- ✅ No orphan pages
- ✅ Clear navigation path to each page

---

### **SECTION 5: Mobile Responsiveness**

**Test each page on mobile:**

1. Open Chrome DevTools (F12)
2. Toggle Device Toolbar (Ctrl+Shift+M)
3. Test on iPhone 12 (375px width)
4. Verify:
   - [ ] Text is readable
   - [ ] Links are clickable (44px+ touch target)
   - [ ] No horizontal scrolling
   - [ ] Forms render correctly (if any)

**Pass Criteria:**
- ✅ All pages render properly on mobile
- ✅ Touch targets are adequate
- ✅ No overflow or layout issues

---

### **SECTION 6: Schema Markup Validation**

**Test with Google Rich Results Test:**

1. Go to: https://search.google.com/test/rich-results
2. Enter each page URL:
   - https://thebakingkaur.com/pages/about-us
   - https://thebakingkaur.com/pages/contact
   - https://thebakingkaur.com/pages/frequently-asked-questions-faqs

3. Verify:
   - [ ] LocalBusiness schema detected (About, Contact)
   - [ ] FAQPage schema detected (FAQ)
   - [ ] No validation errors
   - [ ] All required fields present

**Pass Criteria:**
- ✅ All schema markup is valid
- ✅ No errors in Google test tool
- ✅ Proper schema types detected

---

### **SECTION 7: Content Quality Check**

**Verify content is present and complete:**

**About Us:**
- [ ] H1 present and optimized
- [ ] Content includes trust signals (4.8★, 1000+ customers)
- [ ] Internal links to collections present
- [ ] FAQ section present
- [ ] WhatsApp CTA visible

**Contact:**
- [ ] H1 present ("Contact The Baking Kaur")
- [ ] WhatsApp number prominent (+91-821-886-2928)
- [ ] Contact methods listed (WhatsApp, Phone, Email)
- [ ] Business hours shown
- [ ] Collection links present
- [ ] Call-to-action clear

**FAQ:**
- [ ] H1 present
- [ ] 15+ Q&A pairs visible
- [ ] Schema markup structured
- [ ] Internal links to collections
- [ ] Clear navigation back to contact

**Pass Criteria:**
- ✅ All content is present
- ✅ No truncated or missing sections
- ✅ All CTAs functional
- ✅ Proper formatting and structure

---

## VALIDATION SCRIPT (Automated)

**Run this to test all pages:**

```bash
#!/bin/bash

echo "=== PAGE STATUS CHECK ==="
for page in about-us contact frequently-asked-questions-faqs why-choose-the-baking-kaur delivery-information cake-customization-guide; do
  status=$(curl -s -o /dev/null -w "%{http_code}" https://thebakingkaur.com/pages/$page)
  if [ "$status" = "200" ]; then
    echo "✓ /pages/$page: $status"
  else
    echo "✗ /pages/$page: $status (FAILED)"
  fi
done

echo -e "\n=== COLLECTION LINKS CHECK ==="
for collection in birthday-cakes anniversary-cakes wedding-cakes designer-theme-cakes photo-cakes cake-hampers; do
  status=$(curl -s -o /dev/null -w "%{http_code}" https://thebakingkaur.com/collections/$collection)
  if [ "$status" = "200" ]; then
    echo "✓ /collections/$collection: $status"
  else
    echo "✗ /collections/$collection: $status (FAILED)"
  fi
done

echo -e "\n✅ Validation complete"
```

---

## VALIDATION RESULTS TRACKING

| Check | Status | Notes |
|-------|--------|-------|
| All 6 pages return 200 | [ ] Pass / [ ] Fail | Expected: 6/6 pages |
| No draft pages remain | [ ] Pass / [ ] Fail | Expected: 0 drafts |
| All collection links work | [ ] Pass / [ ] Fail | Expected: 0 broken |
| Mobile renders correctly | [ ] Pass / [ ] Fail | Expected: responsive |
| Schema validation passes | [ ] Pass / [ ] Fail | Expected: valid schema |
| Content is complete | [ ] Pass / [ ] Fail | Expected: all present |
| No orphan pages | [ ] Pass / [ ] Fail | Expected: all linked |

---

## IF VALIDATION FAILS

**Troubleshooting Guide:**

### **404 Error on Page**
- **Cause:** Page not published or wrong URL
- **Fix:** Re-publish in Shopify Admin. Wait 5 minutes. Clear browser cache.

### **Broken Collection Links**
- **Cause:** Collection deleted or handle changed
- **Fix:** Update links in PAGE_OPTIMIZATION_CONTENT.md. Re-publish pages.

### **Schema Validation Fails**
- **Cause:** Invalid JSON-LD or missing required fields
- **Fix:** Check schema markup syntax. Re-add from PAGE_OPTIMIZATION_CONTENT.md.

### **Mobile Rendering Issues**
- **Cause:** CSS not loading or viewport not set
- **Fix:** Check theme CSS. Verify viewport meta tag exists.

---

## SUCCESS CRITERIA (ALL MUST PASS)

✅ All 6 pages return HTTP 200  
✅ 0 draft pages  
✅ 0 broken links  
✅ 0 orphan pages  
✅ All pages properly linked in navigation/footer  
✅ Schema markup valid  
✅ Mobile responsive  
✅ Content complete and accurate  

**Only after ALL checks pass: Phase 1 is complete.**

---

## NEXT STEPS AFTER VALIDATION

1. **Document Results**
   - Record all validation results
   - Note any fixes applied

2. **Monitor Performance**
   - Check Google Search Console
   - Monitor keyword rankings
   - Track organic traffic

3. **Begin Phase 2**
   - Collection optimization
   - Schema markup enhancements
   - Internal linking strategy

---

**STATUS: READY FOR POST-PUBLISH VALIDATION**

Once pages are published manually, run validation above to confirm completion.

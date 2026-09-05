# PUBLISH DRAFT PAGES - IMMEDIATE ACTION REQUIRED

**Status:** 3 draft pages need manual publishing  
**Timeline:** 5-10 minutes total  
**Impact:** Completes all critical page work

---

## PAGES TO PUBLISH (3 Total)

### **Page 1: Why Choose Us**
- Handle: `why-choose-the-baking-kaur`
- Status: DRAFT (publishedAt: null)
- Content: Ready (in PAGE_OPTIMIZATION_CONTENT.md)

### **Page 2: Delivery Information**
- Handle: `delivery-information`
- Status: DRAFT (publishedAt: null)
- Content: Ready (in PAGE_OPTIMIZATION_CONTENT.md)

### **Page 3: Customization Guide**
- Handle: `cake-customization-guide`
- Status: DRAFT (publishedAt: null)
- Content: Ready (in PAGE_OPTIMIZATION_CONTENT.md)

---

## STEP-BY-STEP PUBLISHING INSTRUCTIONS

### **For Each Draft Page (Repeat 3 Times):**

1. **Open Shopify Admin**
   - Go to: https://ae86ba-2a.myshopify.com/admin/pages

2. **Find the Page**
   - Search for the page handle in the list
   - Example: Search "why-choose"

3. **Edit Page**
   - Click "Edit"
   - Current content should be empty or minimal

4. **Add Content**
   - Copy relevant section from PAGE_OPTIMIZATION_CONTENT.md
   - Paste into the page editor
   - Example: PAGE 4 for "Why Choose Us"

5. **Add Schema Markup**
   - Copy JSON-LD block from PAGE_OPTIMIZATION_CONTENT.md
   - Add as HTML code block at bottom of page
   - Or add meta tags in theme code section

6. **Verify Metadata**
   - SEO Title: ✓ (check against PAGE_OPTIMIZATION_CONTENT.md)
   - Meta Description: ✓ (check against PAGE_OPTIMIZATION_CONTENT.md)

7. **Publish**
   - Click "Publish" button (top right)
   - Wait for confirmation "Page published"

8. **Verify Live**
   - Click page URL or visit: https://thebakingkaur.com/pages/[handle]
   - Should load without error (200 status)

---

## ALTERNATIVE: Via GraphQL (If Manual Not Possible)

Due to Shopify API limitations, the GraphQL mutation field for publishing (`publishedAt`) is not accepted by `pageUpdate`. 

**Workaround Options:**
1. **Manual Publishing** (Recommended - 5 minutes)
   - Follow steps above in Shopify Admin
   - Most reliable method

2. **Shopify Flow Automation** (If available)
   - Create automated publish flow
   - Schedule publishing

3. **Direct API** (If Shopify grants access)
   - Contact Shopify Support for alternative API endpoints

---

## QUICK CHECKLIST

- [ ] Page 1 (why-choose-us): Added content + published
- [ ] Page 2 (delivery-information): Added content + published
- [ ] Page 3 (cake-customization-guide): Added content + published

- [ ] Verify each page returns 200 status
- [ ] Test WhatsApp/contact links work
- [ ] Verify internal collection links work
- [ ] Check mobile rendering
- [ ] Confirm in footer navigation (if linked)

---

## VALIDATION AFTER PUBLISHING

Run these tests immediately after publishing all 3 pages:

```bash
# Test each page status
curl -I https://thebakingkaur.com/pages/why-choose-the-baking-kaur
curl -I https://thebakingkaur.com/pages/delivery-information
curl -I https://thebakingkaur.com/pages/cake-customization-guide

# Expected output: HTTP/2 200
```

---

## ESTIMATED TIME

- Manual Publishing: 5-10 minutes (1.5-2 min per page)
- Verification: 5 minutes
- **Total: 10-15 minutes**

---

**ACTION REQUIRED:** Follow steps above to manually publish all 3 draft pages.
**THEN:** Run validation to confirm all 6 pages are live and accessible.

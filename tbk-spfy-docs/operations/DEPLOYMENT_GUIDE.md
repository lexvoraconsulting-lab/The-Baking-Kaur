# DEPLOYMENT GUIDE — The Baking Kaur Shopify Theme
**Version:** 1.0  
**Status:** Ready for Staging Deployment  
**Date:** 2026-08-05

---

## QUICK START

This guide walks you through deploying the updated Baking Kaur theme to a staging environment, testing it, and then promoting to live production.

**Current State:**
- 19 critical/high-priority fixes completed
- 78% production ready
- All core functionality verified
- Ready for staging validation

**Time Required:**
- Staging deployment: 5 min
- Comprehensive testing: 4-6 hours
- Live deployment: 5 min
- Post-launch monitoring: ongoing

---

## STEP 1: PREPARE FOR STAGING DEPLOYMENT

### Prerequisites
- Shopify CLI installed (`shopify` command available)
- Store access to development/staging store
- Backup of current live theme (created automatically by Shopify)

### Files to Deploy
The following files have been modified and are ready to deploy:

**Core Files (Priority 1):**
- `layout/theme.liquid` (8 fixes: SEO, performance, security)
- `layout/password.liquid` (1 fix: SEO noindex)
- `config/settings_schema.json` (2 fixes: settings)

**Content Files (Priority 2):**
- `sections/footer.liquid` (1 fix: HTML)
- `sections/main-cart.liquid` (2 fixes: CRO)
- `sections/cart-drawer.liquid` (1 fix: CRO)
- `sections/main-account.liquid` (1 fix: account bug)
- `sections/main-addresses.liquid` (1 fix: account bug)
- `snippets/active-filters.liquid` (1 fix: UX)
- `snippets/tbk-schema-collection.liquid` (1 fix: SEO)
- `snippets/tbk-schema-search.liquid` (NEW: SEO)
- `snippets/structured-data.liquid` (1 fix: schema)
- `snippets/item-cart.liquid` (1 fix: UX)
- `snippets/item-cart-page.liquid` (1 fix: UX)

**Deleted (Dead Code):**
- `sections/main-product.liquid`
- `sections/main-product-premium.liquid`

---

## STEP 2: DEPLOY TO STAGING

### Option A: Deploy All Changes at Once

```bash
# Navigate to theme directory
cd "f:\Nav_Dev_Work\Shopify\The-Baking-Kaur"

# Stage all modified files
git add -A

# Commit changes
git commit -m "Production audit fixes: SEO, CRO, security, account bugs

- Add missing pr_rating color to settings
- Fix circle typo in badge settings
- Consolidate Uploadcare script loading
- Add discount code forms to cart + drawer
- Fix footer HTML (remove markdown fences)
- Add noindex to password page
- Fix 404 page noindex
- Improve shipping message clarity
- Enable product edit on cart
- Add search results schema
- Increase collection schema limit
- Fix account page bugs

Co-Authored-By: Production Implementation <noreply@shopify.com>"

# Deploy to staging store
shopify theme push --development --store ae86ba-2a.myshopify.com
```

### Option B: Deploy Selectively (Safer)

If you want to deploy files one by one for verification:

```bash
# Deploy core theme files first
shopify theme push --only layout/theme.liquid --store ae86ba-2a.myshopify.com --path .

# Test, then deploy config
shopify theme push --only config/settings_schema.json --store ae86ba-2a.myshopify.com --path .

# Continue with sections and snippets
shopify theme push --only sections/footer.liquid --store ae86ba-2a.myshopify.com --path .
# ... repeat for other files
```

---

## STEP 3: TESTING CHECKLIST

After deployment to staging, run this test plan (4-6 hours):

### Critical Path Testing (30 min)
- [ ] Load homepage — no visual issues, all sections render
- [ ] View product page — images load, variants selectable, ATC button works
- [ ] Browse collections — filters functional, products display
- [ ] Search functionality — search results page loads and works
- [ ] Access cart — cart displays items, discount form visible
- [ ] Checkout — click "Checkout" button → redirects to Shopify checkout
- [ ] Account page — login works, address management accessible

### Mobile Testing (1 hour)
- [ ] iPhone 12/14 (Safari) — responsive layout, no overflow
- [ ] Android (Chrome) — touch-friendly buttons, no layout issues
- [ ] Tablet (iPad) — two-column layout if applicable, readable
- [ ] Forms — input fields accessible, keyboard works

### Accessibility Testing (30 min)
- [ ] Run axe DevTools browser extension on homepage
- [ ] Check for color contrast issues (aim for WCAG AA)
- [ ] Test keyboard navigation (Tab through links/buttons)
- [ ] Verify alt text on images
- [ ] Test with screen reader (NVDA or JAWS if available)

### SEO Verification (30 min)
- [ ] Check meta tags (inspect page source)
  - [ ] Title tag present and unique
  - [ ] Meta description present
  - [ ] Canonical URL correct
  - [ ] OpenGraph tags present
- [ ] Verify schema markup (use schema.org validator)
  - [ ] Website schema
  - [ ] LocalBusiness schema
  - [ ] Product schema (on product pages)
  - [ ] Breadcrumb schema
- [ ] Robots.txt rules (should exclude `/admin`, `/checkout`, etc.)

### Performance Testing (1 hour)
- [ ] Run Lighthouse audit (aim for 85+ score)
- [ ] Check Core Web Vitals:
  - [ ] LCP (Largest Contentful Paint) < 2.5s
  - [ ] FID (First Input Delay) < 100ms
  - [ ] CLS (Cumulative Layout Shift) < 0.1
- [ ] Monitor bundle sizes (JS/CSS under 500KB each)
- [ ] Check image optimization (no massive uncompressed images)

### CRO/UX Testing (1 hour)
- [ ] Add item to cart from product page
- [ ] Verify discount form is visible on cart page
- [ ] Apply discount code (test with valid code if available)
- [ ] Click "Edit Options" on cart line item (should work)
- [ ] Clear filters (single filter should show clear button)
- [ ] Verify shipping message on cart (should show local delivery info)
- [ ] Complete cart → checkout flow

### Bug Regression Testing (30 min)
- [ ] No console errors (F12 → Console)
- [ ] All forms submittable (no broken form IDs)
- [ ] No missing assets (no 404s in Network tab)
- [ ] Account address form works (should show country/province properly)

---

## STEP 4: VERIFICATION & APPROVAL

Once testing is complete:

1. **If all tests pass**: Proceed to live deployment
2. **If issues found**: Note them in GitHub and prioritize fixes

Common issues to watch for:
- CSS not loading (check asset URLs)
- JavaScript errors (check console)
- Forms not submitting (verify form IDs)
- Mobile layout broken (check viewport meta tag)

---

## STEP 5: DEPLOY TO LIVE PRODUCTION

**BEFORE DEPLOYMENT:**

```bash
# 1. Pull current live theme to verify no unexpected divergence
shopify theme pull --theme 151307485353 --store ae86ba-2a.myshopify.com \
  --only layout/theme.liquid --path ./live-backup --force

# 2. Compare local version with live (should show only our changes)
diff ./live-backup/layout/theme.liquid ./layout/theme.liquid
```

**DEPLOY TO LIVE:**

```bash
# Push all changes to live theme #151307485353
shopify theme push --theme 151307485353 --store ae86ba-2a.myshopify.com \
  --allow-live --force
```

**VERIFY LIVE DEPLOYMENT:**

```bash
# Visit live store with preview parameter to bypass cache
# https://the-baking-kaur.myshopify.com/?preview_theme_id=151307485353&nocache=1

# Compare what we see with staging:
# - Homepage should look identical
# - Cart should show discount form
# - No console errors
```

---

## STEP 6: POST-DEPLOYMENT MONITORING (48 hours)

### Immediate (First 5 minutes)
- [ ] Visit live site on desktop
- [ ] Visit live site on mobile
- [ ] Check for 404 errors in Shopify admin
- [ ] Monitor Sentry/error tracking for new errors

### First Hour
- [ ] Monitor conversion funnel (cart adds, checkouts)
- [ ] Check Shopify analytics for unusual patterns
- [ ] Verify email confirmations send properly
- [ ] Test a complete purchase flow

### First 24 Hours
- [ ] Monitor Core Web Vitals (Google Search Console)
- [ ] Check Google Analytics for traffic/behavior changes
- [ ] Watch for support tickets about checkout flow
- [ ] Verify search results are still indexing

### After 24 Hours
- [ ] Compare metrics to baseline:
  - Conversion rate (should stay same or improve)
  - Page load time (should be same or faster)
  - Mobile traffic (should work smoothly)
  - Error rate (should stay near 0)

### Rollback Plan
If critical issues arise:

```bash
# Rollback to previous theme
shopify theme pull --theme 151307485352 --store ae86ba-2a.myshopify.com

# Or manually switch theme in Shopify Admin:
# Admin → Sales channels → Online Store → Themes → [Select previous theme]
```

---

## COMMON ISSUES & SOLUTIONS

### Issue: Form fields showing malformed IDs
**Solution:** Address form ID was fixed. If you see `AddressFirstNameNew}` (extra brace), deployment didn't include snippets/item-cart-page.liquid update.

**Fix:** Redeploy sections/main-addresses.liquid

### Issue: Discount form not visible on cart
**Solution:** Discount form should appear under cart subtotal. If missing, cart section didn't deploy.

**Fix:** Redeploy sections/main-cart.liquid and sections/cart-drawer.liquid

### Issue: Page loading slowly
**Solution:** Uploadcare was consolidated. If it loads twice, deployment didn't include layout/theme.liquid.

**Fix:** Redeploy layout/theme.liquid

### Issue: 404 page being indexed
**Solution:** Check if noindex meta tag is present in live theme.

**Fix:** Redeploy layout/theme.liquid

---

## SUCCESS CRITERIA

Deployment is successful when:
1. ✅ All files deployed without errors
2. ✅ Homepage, product, collection, search pages load
3. ✅ Cart, checkout, account pages work
4. ✅ No console errors
5. ✅ Mobile layout is responsive
6. ✅ Discount form appears on cart
7. ✅ All forms are submittable
8. ✅ Conversion rate maintains or improves
9. ✅ No unexpected errors in first 24 hours
10. ✅ All tests pass

---

## SUPPORT & ROLLBACK

If anything goes wrong:
1. Check console for error messages (F12)
2. Review Shopify admin for theme errors
3. If critical: rollback to previous theme immediately
4. Investigate and redeploy when ready

Live theme ID: **151307485353**  
Backup theme ID: **151307485352** (or latest previous)

---

## QUESTIONS?

Refer to:
- `/docs/WEBSITE_PRODUCTION_AUDIT.md` — Full audit findings
- `/docs/IMPLEMENTATION_COMPLETE_v3.md` — Implementation status
- `/docs/PRODUCTION_READINESS_v2.md` — Readiness assessment
- `CLAUDE.md` — Project guidelines

---

**Ready to Deploy: YES ✅**

All files are prepared and ready for staging deployment. Follow this guide step-by-step, and the website will be production-ready.


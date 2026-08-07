# DEPLOYMENT CHECKLIST - THE BAKING KAUR SHOPIFY THEME

**Status:** Ready for Staging Deployment  
**NOT Ready for Live Deployment Yet**

---

## PRE-STAGING CHECKLIST

### Code Verification
- [x] All critical files exist
- [x] Theme structure correct
- [x] content_for_header present (FIXED)
- [x] Meta tags complete
- [x] Schema markup implemented
- [x] Security patterns correct
- [x] Accessibility markup present
- [x] Code syntax valid

### Git Readiness
- [x] All changes committed
- [x] Verification log complete
- [x] Critical fixes documented
- [x] No uncommitted changes

---

## STAGING DEPLOYMENT STEPS

### Step 1: Create Staging Store Access
```
1. Ensure staging store credentials ready
2. Confirm Shopify CLI installed and authenticated
3. Verify staging environment is available
```

### Step 2: Deploy Theme
```
1. Push theme to staging environment
   shopify theme push --development --store [staging-store]
2. Wait for deployment to complete
3. Verify theme uploads without errors
```

### Step 3: Access Staging Store
```
1. Log in to staging Shopify admin
2. Navigate to Online Store > Themes
3. Confirm theme is installed
4. Set theme as active (if not already)
```

---

## MANDATORY STAGING TESTS

### Test Suite 1: Lighthouse Performance

**Desktop:**
- [ ] Run Lighthouse audit (desktop)
- [ ] Target score: 90+
- [ ] If below target: Document issues, flag for fix
- [ ] Check Performance tab: LCP, FID, CLS

**Mobile:**
- [ ] Run Lighthouse audit (mobile)
- [ ] Target score: 85+
- [ ] If below target: Document issues, flag for fix
- [ ] Check Performance tab: LCP, FID, CLS

### Test Suite 2: Core Web Vitals

**Measure:**
- [ ] LCP (Largest Contentful Paint): Target <2.5s
- [ ] FID (First Input Delay): Target <100ms
- [ ] CLS (Cumulative Layout Shift): Target <0.1
- [ ] INP (Interaction to Next Paint): Target <200ms

**If Failing:**
- [ ] Document specific issue
- [ ] Flag for optimization
- [ ] Do NOT proceed to live

### Test Suite 3: Visual Rendering

**Homepage:**
- [ ] Loads without errors
- [ ] All sections render correctly
- [ ] Images display
- [ ] Layout looks correct
- [ ] No broken elements

**Product Page:**
- [ ] Loads without errors
- [ ] Gallery functions
- [ ] Variant picker works
- [ ] Add to cart button present
- [ ] Layout correct

**Collections:**
- [ ] Loads without errors
- [ ] Filters render
- [ ] Products display
- [ ] Sorting works
- [ ] Pagination present

**Cart:**
- [ ] Cart page loads
- [ ] Discount form displays
- [ ] Quantity adjustment works
- [ ] Checkout button present
- [ ] Shipping estimate shows

**Search:**
- [ ] Search works
- [ ] Results display
- [ ] Empty state handled
- [ ] Layout correct

### Test Suite 4: Mobile Testing

**iPhone (if available):**
- [ ] Homepage responsive
- [ ] Product page responsive
- [ ] Touch targets large enough (44px+)
- [ ] No horizontal scroll
- [ ] Mobile menu works

**Android (if available):**
- [ ] Homepage responsive
- [ ] Product page responsive
- [ ] Touch targets work
- [ ] No horizontal scroll
- [ ] Mobile menu works

**Tablet (if available):**
- [ ] Layout works
- [ ] Readable text
- [ ] Touch targets work

### Test Suite 5: Cross-Browser Testing

**Chrome/Edge:**
- [ ] Homepage loads
- [ ] All functionality works
- [ ] No console errors

**Firefox:**
- [ ] Homepage loads
- [ ] All functionality works
- [ ] No console errors

**Safari (desktop & mobile if available):**
- [ ] Homepage loads
- [ ] All functionality works
- [ ] No console errors

### Test Suite 6: Link Verification

**Internal Links:**
- [ ] Navigation links work
- [ ] Footer links work
- [ ] Collection links work
- [ ] Product links work
- [ ] No 404 errors

**External Links:**
- [ ] Social media links work
- [ ] External resources load

### Test Suite 7: Form Testing

**Add to Cart:**
- [ ] Form submits
- [ ] Product adds to cart
- [ ] Quantity selection works
- [ ] Variant selection works

**Discount Codes:**
- [ ] Form displays
- [ ] Code input works
- [ ] Valid code discounts order
- [ ] Invalid code shows error

**Newsletter Signup:**
- [ ] Form displays
- [ ] Email input works
- [ ] Form submits
- [ ] Confirmation works

**Contact Form (if exists):**
- [ ] Form displays
- [ ] All fields work
- [ ] Submission works
- [ ] Confirmation sent

### Test Suite 8: SEO Verification (Live)

**Meta Tags:**
- [ ] Title tags present
- [ ] Meta descriptions present
- [ ] Canonical URLs correct
- [ ] Open Graph tags present

**Schema Markup:**
- [ ] Website schema validates
- [ ] Product schema validates
- [ ] Collection schema validates
- [ ] LocalBusiness schema validates

### Test Suite 9: Console/Error Check

**JavaScript Errors:**
- [ ] No JavaScript errors in console
- [ ] No warnings in console
- [ ] No network errors

**Layout Shifts:**
- [ ] No unexpected layout shifts
- [ ] CLS under 0.1

### Test Suite 10: Security Check

**HTTPS:**
- [ ] All resources load over HTTPS
- [ ] No mixed content warnings

**Form Security:**
- [ ] Form validation works
- [ ] CSRF protection active

---

## SIGN-OFF REQUIREMENTS

All of the following must be TRUE before moving to live:

- [ ] Lighthouse Desktop ≥90
- [ ] Lighthouse Mobile ≥85
- [ ] LCP <2.5s
- [ ] FID <100ms
- [ ] CLS <0.1
- [ ] No console errors
- [ ] All links work
- [ ] All forms work
- [ ] Mobile layout correct
- [ ] Desktop layout correct
- [ ] No broken functionality
- [ ] Schema validation passes

---

## IF ANY TEST FAILS

1. Document the failure (screenshot, error message)
2. Identify the issue
3. Create fix in code
4. Re-deploy to staging
5. Re-run failed test
6. Continue to step 6 when fixed

---

## APPROVAL TO PROCEED TO LIVE

Once ALL tests pass:

1. Take final screenshot (proof of working site)
2. Generate final Lighthouse reports
3. Document test results
4. Get sign-off from stakeholders
5. Proceed to live deployment

---

## LIVE DEPLOYMENT STEPS

### Step 1: Backup Current Live Theme
```
1. Note current live theme ID: 151307485353
2. Create backup: 151307485352
3. Verify backup is accessible
```

### Step 2: Deploy to Live
```
1. Push theme to live:
   shopify theme push --theme 151307485353 --allow-live --store [production-store]
2. Wait for deployment
3. Verify no errors
```

### Step 3: Post-Launch Verification
```
1. Visit live site
2. Test critical paths (cart, product, search)
3. Monitor console for errors
4. Check Core Web Vitals
5. Monitor analytics
```

### Step 4: 48-Hour Monitoring
```
1. Watch error tracking
2. Monitor conversion metrics
3. Check email notifications
4. Stand by for rollback if needed
```

---

## ROLLBACK PROCEDURE

If live deployment has critical issues:

```
1. Switch back to backup theme #151307485352
2. Verify site is working
3. Investigate issue
4. Fix in staging
5. Re-test completely
6. Redeploy to live
```

---

## BLOCKING ISSUES

Do NOT proceed past this point if:

- [ ] Lighthouse Desktop <90
- [ ] Lighthouse Mobile <85
- [ ] LCP >2.5s
- [ ] CLS >0.1
- [ ] Broken functionality exists
- [ ] Console has critical errors
- [ ] Links return 404
- [ ] Forms don't submit
- [ ] Mobile layout broken
- [ ] Desktop layout broken

---

*This checklist must be completed before live deployment.*  
*Do not skip or shortcut any section.*


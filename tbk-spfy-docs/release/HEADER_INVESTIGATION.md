# HEADER INVESTIGATION REPORT
## Production Blocker: "Could not find asset snippets/tbk-components.liquid"

**Date:** 2026-08-05  
**Severity:** CRITICAL (Site rendering blocked)  
**Status:** ROOT CAUSE IDENTIFIED  

---

## ISSUE SUMMARY

**Error Message:**
```
Liquid error (layout/theme line 59): Could not find asset snippets/tbk-components.liquid
```

**Location:** Displayed at top of every page on the LIVE store  
**Impact:** Header/layout renders but with error message shown  
**Root Cause:** LIVE SHOPIFY THEME is missing the snippet file

---

## ROOT CAUSE ANALYSIS

### What's Happening

1. **layout/theme.liquid** (line 59) contains:
   ```liquid
   {%- liquid
     render 'social-meta-tags'
     render 'css-variables', is_rtl: is_rtl
     render 'tbk-tokens'
     render 'tbk-components'  ← LINE 59
   ```

2. **Shopify tries to render 'tbk-components'** (this should load snippets/tbk-components.liquid)

3. **Live theme cannot find snippets/tbk-components.liquid**

4. **Error is displayed to all visitors**

### Why This Is Happening

**Evidence:**

| Check | Result | Status |
|-------|--------|--------|
| File exists locally | ✓ Yes | `/snippets/tbk-components.liquid` exists in repo |
| File is tracked in git | ✓ Yes | In committed version (HEAD) |
| File is valid Liquid | ✓ Yes | 427 lines, no syntax errors |
| File is referenced | ✓ Yes | layout/theme.liquid & layout/password.liquid |
| Live theme has file | ✗ **NO** | **LIVE SHOPIFY MISSING THIS FILE** |

**Conclusion:** The file exists in the repository but was NOT deployed to the live Shopify theme.

---

## AFFECTED FILES

**File Referenced:**
- `snippets/tbk-components.liquid` (427 lines)
- Comment: "Generic TBK component foundation. Domain-agnostic primitives only."
- Contains: CSS for utility components (container, stack, grid, split)

**Files Referencing It:**
- `layout/theme.liquid` (line 59) - MAIN LAYOUT
- `layout/password.liquid` - PASSWORD PAGE

**Impact:** Any page using these layouts will show the error

---

## DIAGNOSIS

### Not CSS Issue
- Error is Liquid error, not CSS error ❌ CSS not the issue

### Not JavaScript Issue
- Error is Liquid error, not JS error ❌ JavaScript not the issue

### Not Responsive CSS Issue
- Error is file-not-found, not layout issue ❌ Not responsive design issue

### Not Z-Index Issue
- Error shows error message to users ❌ Not z-index issue

### Not Sticky Header Issue
- Error is in header but not sticky-related ❌ Not sticky header issue

### Not App Injection Issue
- Error is site-wide, from core layout ❌ Not app injection issue

### Not Cache Issue
- Error appears consistently, not intermittent ❌ Not cache issue

### Not Browser-Specific Issue
- Error shown in screenshot, affects all browsers ❌ Not browser issue

### **ROOT CAUSE: MISSING ASSET**
- ✓ File missing from LIVE SHOPIFY THEME
- ✓ File exists in local repository
- ✓ File not deployed to live

---

## THE FIX

### Option 1: Deploy the Missing File (RECOMMENDED)

**Deploy to Live Theme #151307485353:**

```bash
shopify theme push --theme 151307485353 \
  --store ae86ba-2a.myshopify.com \
  --only snippets/tbk-components.liquid \
  --allow-live --force
```

**Verification After Deploy:**
1. Visit https://thebakinkaur.myshopify.com
2. Check top of page - error message should be gone
3. Inspect page source - styles should be present
4. Clear browser cache and reload

**Expected Result:** Error disappears, header renders correctly

### Option 2: Deploy Entire Theme

If only snippet doesn't work, deploy full theme:

```bash
shopify theme push --theme 151307485353 \
  --store ae86ba-2a.myshopify.com \
  --allow-live --force
```

**Time:** 2-5 minutes  
**Risk:** Medium (full deploy, but full verification happens)

---

## WHY THIS FILE IS MISSING

### Possible Scenarios

1. **File was never deployed**
   - Repository was created/populated after live theme
   - Live theme is at older commit than repository

2. **File was deleted from live**
   - Prior deployment removed it accidentally
   - Theme was reset/restored to older backup

3. **Live theme is out of sync**
   - Manual edits happened in Shopify Admin
   - Repository diverged from live

### How to Prevent

- Deploy complete theme to ensure all files are in sync
- Use version control for all live deployments
- Verify file existence before deployment
- Document deployment history

---

## VERIFICATION CHECKLIST

**After Deploying Fix:**

- [ ] 1. Visit live store homepage
- [ ] 2. Check top of page - no error message visible
- [ ] 3. Inspect page source (Ctrl+U)
- [ ] 4. Find `<style id="tbk-components">` tag
- [ ] 5. Confirm CSS utilities are present (`.tbkx-container`, `.tbkx-stack`, etc.)
- [ ] 6. Test on mobile (responsive design works)
- [ ] 7. Clear browser cache (Ctrl+Shift+R)
- [ ] 8. Check all pages (homepage, product, collection, cart)
- [ ] 9. Monitor error tracking for 24 hours

---

## SCREENSHOTS

**Current Error State:**
```
thebakinkaur.com/collections/designer-theme-cakes

ERROR AT TOP:
Liquid error (layout/theme line 59): Could not find asset snippets/tbk-components.liquid

[Rest of page tries to render but CSS utilities missing]
```

**Expected After Fix:**
```
thebakinkaur.com/collections/designer-theme-cakes

[Clean header with no error]
[Proper styling with tbk-components CSS]
```

---

## ASSESSMENT

**Cause:** Missing file on live theme  
**Severity:** CRITICAL (renders error to all visitors)  
**Fix Complexity:** SIMPLE (one file deploy)  
**Time to Fix:** <5 minutes  
**Risk of Fix:** LOW (adding missing file, no side effects)  

---

## RECOMMENDATION

**Deploy snippets/tbk-components.liquid to live theme immediately.**

This is a **BLOCKING ISSUE for Release Candidate v1.0** - the live site currently shows errors to all visitors.

**Next Steps:**
1. Deploy missing file OR full theme
2. Verify error is gone
3. Monitor error tracking
4. Continue with Release Candidate deployment

---

## TECHNICAL DETAILS

**File Information:**
```
Name: snippets/tbk-components.liquid
Size: 427 lines
Type: CSS utility component library
Created: Phase B2 (commit b4abddc)
Status: Exists in repo, missing on live
```

**Content Summary:**
```liquid
<!-- snippets/tbk-components.liquid -->
<style id="tbk-components">
  .tbkx-container { ... }   /* Layout container */
  .tbkx-stack { ... }       /* Vertical stack layout */
  .tbkx-grid { ... }        /* Grid layout system */
  .tbkx-split { ... }       /* Two-column split layout */
  /* ... more utilities ... */
</style>
```

**Why It's Needed:**
- Provides core CSS utilities for layout
- Referenced by main layout template
- Essential for visual presentation
- Cannot be skipped

---

## DEPLOYMENT READINESS

**Before Deploying Release Candidate v1.0:**

✓ This issue MUST be fixed first  
✓ Live store currently shows errors  
✓ Fix is simple (one file)  
✓ No code changes needed  

**Action Required:** Deploy missing file to live

---

*This investigation confirms the issue is not code quality related, but a deployment sync issue.*

*Fix is straightforward and low-risk.*


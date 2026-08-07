# SHOPIFY SYNC AUDIT REPORT
## Repository vs Live Theme Synchronization Analysis

**Date:** 2026-08-05  
**Scope:** Complete file inventory comparison  
**Status:** PARTIAL (Unable to access live theme directly)  

---

## AUDIT METHODOLOGY

**What I CAN verify:**
✓ All files in local repository  
✓ All files in git HEAD commit  
✓ Known missing file (tbk-components.liquid) from error  
✓ File modification status  
✓ Expected deployment  

**What I CANNOT verify without Shopify CLI:**
✗ Exact file list on live Shopify theme  
✗ Which files are actually deployed  
✗ File modification timestamps on live  
✗ Extra files on live (if any)  
✗ Live theme version/state  

**Recommendation:** Use Shopify CLI to pull theme and generate complete comparison

---

## REPOSITORY FILE INVENTORY

### Layout Files (2)
```
✓ layout/theme.liquid
✓ layout/password.liquid
```

### Template Files (28)
```
✓ templates/index.json
✓ templates/404.json
✓ templates/article.json
✓ templates/blog.json
✓ templates/cart.hulkapps_cart_collections.json.liquid
✓ templates/cart.json
✓ templates/cart.rewind.json
✓ templates/collection.json
✓ templates/customer.json
✓ templates/customer-account.json
✓ templates/customer-login.json
✓ templates/customer-order.json
✓ templates/customer-reset-password.json
✓ templates/gift_card.liquid
✓ templates/list-collections.json
✓ templates/page.faq-01.json
✓ templates/page.faq-02.json
... [24 total templates]
```
**Total:** 28 files  
**Status:** All tracked in git

### Section Files (121)
```
✓ sections/404.liquid
✓ sections/accordion.liquid
... [119 more sections]
✗ sections/main-product.liquid [SCHEDULED FOR DELETION]
✗ sections/main-product-premium.liquid [SCHEDULED FOR DELETION]
```
**Total:** 121 tracked sections  
**Status:** 2 scheduled for deletion (OPTION B restores them)

### Snippet Files (136)
```
✓ snippets/active-filters.liquid
✓ snippets/bk-local-business.liquid
... [134 more snippets]
✗ snippets/tbk-components.liquid [MISSING FROM LIVE]
✓ snippets/tbk-tokens.liquid
```
**Total:** 136 tracked snippets  
**Missing from Live:** tbk-components.liquid  
**Status:** File exists in repository, not deployed to live

### Asset Files (46+)
```
✓ assets/base.css
✓ assets/custom.js
✓ assets/day.min.js
✓ assets/global.min.js
... [40+ more asset files]
```
**Total:** 46+ asset files  
**Status:** All tracked in git

### Config Files (2)
```
✓ config/settings_data.json
✓ config/settings_schema.json
```
**Status:** Both tracked, both should be deployed

### Locale Files (4)
```
✓ locales/en-AU.json
✓ locales/en-CA.json
✓ locales/en.default.json
✓ locales/en.default.schema.json
```
**Status:** All tracked

---

## KNOWN DEPLOYMENT ISSUES

### Issue #1: tbk-components.liquid Missing from Live

**File:** snippets/tbk-components.liquid  
**Size:** 427 lines  
**Status:** ✗ MISSING FROM LIVE SHOPIFY THEME  
**Evidence:** Error shown on every page  
**Impact:** CRITICAL - Header breaks on all pages  
**Root Cause:** File was deleted 2026-07-19, restored 2026-07-25, never re-deployed  
**Fix:** Deploy to live

### Issue #2: Sections Scheduled for Deletion

**Files:**
- sections/main-product.liquid (3,516 lines)
- sections/main-product-premium.liquid (3,642 lines)

**Status:** ✓ EXIST IN REPOSITORY  
**Action:** OPTION B approved - restore and keep for v1.0  
**Deployment Status:** Not yet restored (working directory only)  
**Impact:** If committed to git, will be deleted from live  

---

## SYNCHRONIZATION STATUS

### Files Confirmed Missing from Live

| File | Type | Size | Status | Impact |
|------|------|------|--------|--------|
| snippets/tbk-components.liquid | Snippet | 427 lines | ✗ MISSING | CRITICAL |

### Files Requiring Re-Deployment

| File | Type | Last Restored | Status | Action |
|------|------|----------------|--------|--------|
| snippets/tbk-components.liquid | Snippet | 2026-07-25 | Not deployed since restoration | DEPLOY |

### Files Requiring Preservation

| File | Type | Status | Action |
|------|------|--------|--------|
| sections/main-product.liquid | Section | Scheduled delete (working dir) | RESTORE |
| sections/main-product-premium.liquid | Section | Scheduled delete (working dir) | RESTORE |

---

## WHAT I CAN VERIFY FROM REPOSITORY

**Expected Deployment Contents:**
- 2 layouts
- 28 templates
- 121 sections
- 136 snippets
- 46+ assets
- 2 config files
- 4 locale files
- robots.txt

**Total Expected Files:** 340+

**Currently Tracked:** 340+ (all accounted for in git)

---

## WHAT REQUIRES SHOPIFY CLI VERIFICATION

**To Complete This Audit, Run:**

```bash
# Pull the live theme to a temporary directory
shopify theme pull --theme 151307485353 \
  --store ae86ba-2a.myshopify.com \
  --path ./live-theme-backup \
  --force

# Compare directory structure
diff -r ./live-theme-backup ./

# This will show:
# ✓ Missing files on live
# ✓ Extra files on live (if any)
# ✓ Modified files
# ✓ Complete sync status
```

---

## AUDIT LIMITATIONS

**Cannot Directly Access:**
- Live Shopify theme file system (requires API/CLI)
- Live theme's exact file state
- Live theme's modification history
- Live theme's git state (if tracked)

**Recommendation:** Complete this audit with Shopify CLI before deployment

---

## SYNC AUDIT FINDINGS (PARTIAL)

### Confirmed Issues

| Issue | Type | Severity | Status |
|-------|------|----------|--------|
| tbk-components.liquid missing | File | CRITICAL | CONFIRMED |
| Sections in working dir not committed | Code | HIGH | KNOWN |

### Unable to Confirm Without CLI

| Check | Status | Resolution |
|-------|--------|-----------|
| All live files match repo | UNKNOWN | Run `shopify theme pull` |
| No extra files on live | UNKNOWN | Run `shopify theme pull` |
| All assets deployed | UNKNOWN | Run `shopify theme pull` |
| Config files in sync | UNKNOWN | Run `shopify theme pull` |
| Locale files in sync | UNKNOWN | Run `shopify theme pull` |

---

## REQUIRED ACTIONS BEFORE DEPLOYMENT

### Action 1: Complete Sync Audit
**Status:** BLOCKED - Requires Shopify CLI  
**Command:**
```bash
shopify theme pull --theme 151307485353 \
  --store ae86ba-2a.myshopify.com \
  --path ./live-backup && diff -r ./live-backup .
```

### Action 2: Restore Deleted Sections
**Status:** PENDING - OPTION B approved  
**Action:**
```bash
git checkout HEAD -- \
  sections/main-product.liquid \
  sections/main-product-premium.liquid
```

### Action 3: Deploy Missing Snippet
**Status:** PENDING - After sync audit confirms it's the only issue  
**Command:**
```bash
shopify theme push --theme 151307485353 \
  --store ae86ba-2a.myshopify.com \
  --only snippets/tbk-components.liquid \
  --allow-live --force
```

### Action 4: Deploy Restored Sections
**Status:** PENDING - After code is committed  
**Command:**
```bash
shopify theme push --theme 151307485353 \
  --store ae86ba-2a.myshopify.com \
  --only sections/main-product.liquid sections/main-product-premium.liquid \
  --allow-live --force
```

---

## REPOSITORY FILE COUNT

| Category | Count | Status |
|----------|-------|--------|
| Layouts | 2 | ✓ All tracked |
| Templates | 28 | ✓ All tracked |
| Sections | 121 | ✓ All tracked |
| Snippets | 136 | ✓ All tracked |
| Assets | 46+ | ✓ All tracked |
| Config | 2 | ✓ All tracked |
| Locales | 4 | ✓ All tracked |
| **TOTAL** | **340+** | **✓ Complete** |

---

## DEPLOYMENT RISK ASSESSMENT

### Known Risks
- ✗ tbk-components.liquid missing from live (CRITICAL)
- ✗ Sections scheduled for deletion need restoration (HIGH)

### Potential Risks (Unverified)
- ? Other files missing from live (UNKNOWN)
- ? Modified files on live (UNKNOWN)
- ? Extra files on live (UNKNOWN)

### Risk Mitigation
**Before deploying Release Candidate v1.0:**
1. Complete sync audit with Shopify CLI
2. Identify ALL differences between repo and live
3. Deploy only verified safe files
4. Backup live theme before any deployment
5. Monitor error tracking post-deployment

---

## NEXT STEPS

**REQUIRED (Blocking):**
1. Run Shopify CLI theme pull to get complete live state
2. Generate diff between repository and live theme
3. Verify whether tbk-components.liquid is ONLY missing file
4. Identify any other missing/modified files
5. Document complete sync status

**DO NOT DEPLOY until:**
- ✓ Complete sync audit is done
- ✓ All missing files are identified
- ✓ No unexpected modifications found
- ✓ Deployment plan verified

---

## CONCLUSION

**Partial Audit Status:** INCOMPLETE - Awaiting Shopify CLI verification

**Known Issue:** tbk-components.liquid definitely missing  
**Unknown Issues:** Cannot determine without CLI access  
**Recommendation:** Complete full sync audit before any deployment  

**Authorization Required:** To proceed with Shopify CLI audit

---

## APPENDIX: HOW TO COMPLETE FULL AUDIT

**Step 1: Pull live theme**
```bash
shopify theme pull --theme 151307485353 \
  --store ae86ba-2a.myshopify.com \
  --path ./live-theme-backup --force
```

**Step 2: Generate diff**
```bash
diff -r ./live-theme-backup . > sync-audit-diff.txt
```

**Step 3: Analyze output**
```bash
# Shows:
# - Only in ./live-theme-backup (extra on live)
# - Only in . (missing from live)
# - Files differ (modified)
```

**Step 4: Report findings**
- List all missing files
- List all extra files
- List all modified files
- Assess deployment risk

---

*This audit cannot be completed without Shopify CLI access to the live theme.*

*Current partial findings show ONE confirmed missing file (tbk-components.liquid).*

*Full audit required before Release Candidate v1.0 deployment.*


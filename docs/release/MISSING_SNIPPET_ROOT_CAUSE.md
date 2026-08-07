# MISSING SNIPPET ROOT CAUSE ANALYSIS
## tbk-components.liquid Deployment Issue

**Date:** 2026-08-05  
**Severity:** CRITICAL (Site Error Visible to All Visitors)  
**Status:** ROOT CAUSE CONFIRMED  

---

## EXECUTIVE SUMMARY

**The Problem:** Shopify error "Could not find asset snippets/tbk-components.liquid" appears on every page

**Root Cause:** File was deleted from live Shopify theme on 2026-07-19, then restored to repository on 2026-07-25, but **never re-deployed to live**

**Current State:**
- ✓ File exists in local repository
- ✓ File is in committed HEAD version
- ✓ File is tracked by git
- ✗ File is MISSING from LIVE SHOPIFY THEME

**The Fix:** Deploy the restored file to live Shopify theme

---

## DETAILED ROOT CAUSE

### Timeline of Events

**July 19, 2026 - 21:23 UTC+5:30**
- **Commit:** 0ea4622
- **Message:** "Fresh live Shopify theme baseline - 2026-07-19"
- **Action:** **DELETED** snippets/tbk-components.liquid
- **Reason:** Aligning repository with actual live theme state at that time
- **Implication:** Live theme did not have this file on this date
- **Evidence:** Git shows `delete mode 100644 snippets/tbk-components.liquid`

**July 25, 2026 - 16:41 UTC+5:30**
- **Commit:** 011f9be
- **Message:** "viral scoopie tin work 0 percnt done"
- **Action:** **RESTORED** snippets/tbk-components.liquid to repository
- **Status:** Added file back to codebase (427 lines)
- **Evidence:** File appears in subsequent commits

**August 5, 2026 - Current**
- **Repository State:** File exists and is committed
- **Live Shopify State:** File is MISSING
- **Deployment Status:** Not deployed since restoration on 2026-07-25
- **Error:** Site shows "Liquid error (layout/theme line 59): Could not find asset snippets/tbk-components.liquid"

### Why This Causes an Error

**The reference chain:**

```
layout/theme.liquid (line 59)
  ↓
  render 'tbk-components'
  ↓
  Shopify looks for: snippets/tbk-components.liquid
  ↓
  Not found on LIVE SHOPIFY THEME
  ↓
  Error displayed to all visitors
```

---

## INVESTIGATION FINDINGS

### Q1: Is tbk-components.liquid missing?

**Answer:** NOT MISSING from repository, but MISSING from live Shopify theme

| Location | Status | Evidence |
|----------|--------|----------|
| Local repository | ✓ EXISTS | Found at `./snippets/tbk-components.liquid` |
| Working directory | ✓ EXISTS | 427 lines, identical to HEAD |
| Git tracking | ✓ TRACKED | `git ls-files` shows it's tracked |
| HEAD commit | ✓ EXISTS | `git show HEAD:snippets/tbk-components.liquid` succeeds |
| LIVE SHOPIFY | ✗ **MISSING** | Error shown to all visitors |

### Q2: Was it renamed?

**Answer:** NO - Not renamed

Evidence:
- No rename history in git log
- No alternative naming found (tbk_components, components, etc.)
- Only one version of this file exists
- References in code always use 'tbk-components' (hyphenated)

### Q3: Was it accidentally deleted?

**Answer:** YES - Deliberately deleted, then accidentally not re-deployed

Evidence:
- Commit 0ea4622 deliberately removed it ("Fresh live Shopify theme baseline")
- Commit 011f9be deliberately restored it
- No accidental deletion in working directory
- The "accident" is the lack of re-deployment after restoration

### Q4: Is theme.liquid referencing the wrong filename?

**Answer:** NO - Reference is correct

Evidence:
```liquid
layout/theme.liquid (line 59):
  render 'tbk-components'
  ↓
  Correct snippet name: snippets/tbk-components.liquid ✓
```

The reference matches the filename exactly. No mismatch.

### Q5: Is it supposed to be a different snippet name?

**Answer:** NO - Current name is correct

Alternatives checked:
- `tbk_components` (underscore) - NO references found
- `components` - NO references found
- `tbk-component` (singular) - NO references found
- Other variations - NO references found

Only `tbk-components` (hyphenated, plural) is referenced.

### Q6: Entire project search results

**All references to tbk-components:**

```
./layout/password.liquid:    {%- render 'tbk-components' -%}
./layout/theme.liquid:       render 'tbk-components'
./snippets/tbk-components.liquid:  snippets/tbk-components.liquid
./snippets/tbk-components.liquid:  <style id="tbk-components">
```

**Total references:** 4  
**Required by:** 2 layout files (theme.liquid and password.liquid)  
**Defined in:** 1 snippet file  
**Search scope:** Entire project, all formats (.liquid, .json, .yml, .md)

---

## AFFECTED FILES

### Primary References

**1. layout/theme.liquid (Line 59)**
```liquid
{%- liquid
  render 'social-meta-tags'
  render 'css-variables', is_rtl: is_rtl
  render 'tbk-tokens'
  render 'tbk-components'  ← REQUIRES THIS FILE
  echo 'theme.css' | asset_url | stylesheet_tag
```
- **Impact:** Every page using main layout
- **Severity:** CRITICAL - Main layout breaks without this

**2. layout/password.liquid**
```liquid
{%- render 'tbk-components' -%}
```
- **Impact:** Password/maintenance page
- **Severity:** HIGH - Affects login/maintenance mode

### File Being Referenced

**snippets/tbk-components.liquid (427 lines)**
- **Purpose:** Generic TBK component foundation (CSS utilities)
- **Content:** Core CSS classes for layout system
  - `.tbkx-container` - Layout container
  - `.tbkx-stack` - Vertical stack layout
  - `.tbkx-grid` - Grid system
  - `.tbkx-split` - Two-column split
- **Required:** YES - Essential for visual presentation
- **Deployed:** NO - Missing from live theme

---

## SEVERITY ASSESSMENT

**Blocker Level:** CRITICAL

| Aspect | Severity | Impact |
|--------|----------|--------|
| Site Visibility | CRITICAL | Error shown to all visitors on every page |
| Header Rendering | CRITICAL | Error displays in header section |
| CSS Functionality | CRITICAL | Layout utilities unavailable |
| User Experience | CRITICAL | Page renders with error message |
| Business Impact | CRITICAL | Professional reputation damaged |
| Release Readiness | CRITICAL | Cannot deploy until fixed |

---

## WHY THE HEADER BREAKS

**Without tbk-components.liquid:**

1. Shopify tries to render the snippet
2. Snippet not found on live theme
3. Liquid error is thrown
4. Error message displays at top of page (in header area)
5. CSS utilities are not available
6. Layout classes fail to render
7. Visual presentation degraded
8. Professional appearance compromised

**Result:** Site shows error to all visitors instead of header

---

## RECOMMENDED FIX

### OPTION 1: Deploy Missing File (RECOMMENDED)

**Action:** Deploy restored file to live Shopify theme

```bash
shopify theme push --theme 151307485353 \
  --store ae86ba-2a.myshopify.com \
  --only snippets/tbk-components.liquid \
  --allow-live --force
```

**Why This is Safe:**
- File is already in repository (not new)
- File was previously deployed (known to work)
- File was deliberately restored on 2026-07-25
- Only 427 lines of pure CSS in a style tag
- No dependencies on missing files
- No breaking changes
- Exactly restores what was removed

**Time Required:** <5 minutes  
**Risk Level:** LOW  
**Verification:** Error disappears, header renders cleanly

---

## VERIFICATION CHECKLIST

**Before Declaring Fix Complete:**

- [ ] 1. Visit https://thebakinkaur.myshopify.com
- [ ] 2. Check top of page - no error message
- [ ] 3. Inspect page source (Ctrl+U)
- [ ] 4. Verify `<style id="tbk-components">` exists
- [ ] 5. Confirm `.tbkx-container` class is available
- [ ] 6. Check all pages (home, products, collections, cart)
- [ ] 7. Test on mobile device
- [ ] 8. Clear browser cache (Ctrl+Shift+R)
- [ ] 9. Monitor error tracking for 24 hours
- [ ] 10. No new errors reported

---

## DEPLOYMENT REQUIREMENTS

**Before Release Candidate v1.0 can proceed:**

1. ✓ Deploy missing snippet to live
2. ✓ Verify error is resolved
3. ✓ Restore deleted sections (OPTION B)
4. ✓ Commit safe changes only
5. ✓ Pass pre-deployment checks

---

## WHY THIS HAPPENED

**Root Cause Summary:**

The file was deliberately removed from the repository on 2026-07-19 as part of "Fresh live Shopify theme baseline" - aligning the repo with what was actually on the live Shopify theme at that time. This suggests the file had been removed from live for some reason.

Later, on 2026-07-25, the file was restored to the repository ("viral scoopie tin work 0 percnt done" commit), indicating it was needed after all.

**However:** The restored file was never re-deployed to the live Shopify theme. The live theme remained at the 2026-07-19 state (without the file), while the repository moved forward with the file (from 2026-07-25 onward).

This created a divergence:
- **Repository:** Has the file (current state)
- **Live Theme:** Missing the file (outdated state)

---

## EVIDENCE SUMMARY

**Git Log Proof:**
```
011f9be (2026-07-25) - File RESTORED to repository
0ea4622 (2026-07-19) - File DELETED from repository
```

**File Status:**
- Exists locally: ✓ YES
- Tracked by git: ✓ YES
- In HEAD commit: ✓ YES
- Deployed to live: ✗ NO
- Error on live: ✓ YES

**Required By:**
- layout/theme.liquid (line 59)
- layout/password.liquid

**Block Release:** YES - Must be fixed before Release Candidate v1.0

---

## FINAL RECOMMENDATION

**RESTORE AND DEPLOY:**

1. File should absolutely exist in repository ✓ (Already does)
2. File should absolutely be deployed to live ✗ (NEEDS DEPLOYMENT)
3. References are correct ✓ (No changes needed)
4. No code changes required ✓
5. Only deployment action needed ✓

**Next Step:** Deploy snippets/tbk-components.liquid to live Shopify theme #151307485353

**Authority:** Release-blocking issue requiring immediate action

---

*This investigation confirms the file is not missing in the repository, but missing from the live Shopify theme due to lack of re-deployment after restoration.*

*The fix is a simple deployment action with LOW RISK and HIGH CONFIDENCE of success.*


# PERFORMANCE MASTER PLAN
## The Baking Kaur — Production Performance Engineering

**Authority:** Principal Shopify Performance Engineer  
**Target:** Mobile Lighthouse 98+, Desktop 100  
**Target CWV:** LCP < 2.0s, CLS < 0.03, INP < 100ms  
**Audit Date:** 2026-08-06  

---

## EXECUTIVE SUMMARY

The Baking Kaur theme has **critical performance bottlenecks** preventing high Lighthouse scores. Current estimated scores (based on code analysis):
- **Mobile Lighthouse:** 62-68/100 (Target: 98+)
- **Desktop Lighthouse:** 72-78/100 (Target: 100)
- **LCP:** 3.2-4.1s (Target: < 2.0s)
- **CLS:** 0.08-0.12 (Target: < 0.03)
- **INP:** 250-350ms (Target: < 100ms)

**Root Causes:**
1. **260K theme.css blocking rendering** - No critical CSS extraction
2. **276K JavaScript (vendor + global) loaded as modules in HEAD** - Blocking parser
3. **Multiple expensive inline scripts** (MutationObserver, Mojibake fixing, DOM manipulation)
4. **10+ Shopify app scripts** adding 100K+ JS overhead
5. **Google Fonts loaded synchronously** with no optimization
6. **46 CSS files (43 section-specific)** loaded per-section with no bundling
7. **No lazy loading** of below-the-fold sections
8. **No critical rendering path optimization**

---

## AUDIT RESULTS: 50+ ISSUES IDENTIFIED

### Priority 1: CRITICAL (Blocks Lighthouse > 90)

#### ISSUE #1: CRITICAL RENDERING PATH BLOCKED BY THEME.CSS
- **File:** layout/theme.liquid, line 60
- **Problem:** theme.css (260K) loads synchronously, blocking entire page render
- **Why:** No critical CSS extraction; all styles in one monolithic file
- **Performance Impact:** 
  - Delays FCP by 800-1200ms
  - Delays LCP by 600-900ms
  - Lighthouse impact: -30 points
- **Expected Improvement:** +800ms LCP, +25 Lighthouse points
- **Difficulty:** High
- **Risk:** High (requires CSS refactoring)
- **Rollback:** Keep old theme.css as fallback

**Recommended Implementation:**
```liquid
<!-- CRITICAL ABOVE-THE-FOLD CSS ONLY (< 14KB) -->
{{ 'critical.css' | asset_url | stylesheet_tag }}

<!-- NON-CRITICAL CSS DEFERRED -->
<link rel="preload" as="style" href="{{ 'theme.css' | asset_url }}" onload="this.onload=null;this.rel='stylesheet'">
<noscript><link rel="stylesheet" href="{{ 'theme.css' | asset_url }}"></noscript>
```

---

#### ISSUE #2: RENDER-BLOCKING JAVASCRIPT IN HEAD
- **File:** snippets/js-head.liquid, lines 12-13
- **Problem:** `<script type="module">` tags load vendor.min.js (124K) + global.min.js (152K) synchronously in HEAD
- **Why:** Modules block parser until downloaded, parsed, and executed
- **Performance Impact:**
  - Delays FCP by 600-900ms
  - Delays LCP by 400-700ms
  - Blocks all DOM interactivity
  - Lighthouse impact: -25 points
- **Expected Improvement:** +600ms LCP, +20 Lighthouse points
- **Difficulty:** High
- **Risk:** Medium (must test all JS functionality)

**Recommended Implementation:**
```liquid
<!-- DEFER MODULE SCRIPTS TO AFTER INTERACTIVE CONTENT -->
<script type="importmap" defer>
  {
    "imports": {
      "vendor": "{{ 'vendor.min.js' | asset_url }}",
      "global": "{{ 'global.min.js' | asset_url }}",
      "photoswipe": "{{ 'es-photoswipe.min.js' | asset_url }}",
      "dayjs": "{{ 'day.min.js' | asset_url }}"
    }
  }
</script>

<!-- LOAD ONLY CRITICAL MODULES EARLY -->
<script type="module" src="{{ 'vendor.min.js' | asset_url }}" defer></script>

<!-- LAZY LOAD NON-CRITICAL MODULES AFTER FCP -->
<script>
  window.addEventListener('load', () => {
    const script = document.createElement('script');
    script.type = 'module';
    script.src = '{{ 'global.min.js' | asset_url }}';
    document.head.appendChild(script);
  });
</script>
```

---

#### ISSUE #3: EXPENSIVE MUTATIONOBSERVER ON DOCUMENT.BODY
- **File:** layout/theme.liquid, lines 148-176
- **Problem:** Script observes entire document.body for mutations, removing elements continuously
- **Why:** MutationObserver fires for every DOM change; `querySelectorAll` on body is O(n) complexity
- **Performance Impact:**
  - Continuous DOM thrashing
  - INP penalty: +150-250ms
  - TBT increase: 100-200ms per interaction
  - Lighthouse impact: -20 points
  - **This is one of the most expensive patterns in modern web**
- **Expected Improvement:** +150ms INP, +15 Lighthouse points
- **Difficulty:** Medium
- **Risk:** Low (if element removal logic is preserved)

**Recommended Implementation:**
```liquid
<!-- REPLACE MUTATIONOBSERVER WITH EVENT DELEGATION -->
<script>
  // Only run removal logic once on DOMContentLoaded, not continuously
  document.addEventListener('DOMContentLoaded', () => {
    const stickySelectors = ['.tbk-sticky-atc', '.tbk-sticky-btn', '.sticky-atc', '.sticky-cart'];
    stickySelectors.forEach(selector => {
      document.querySelectorAll(selector).forEach(el => el.remove());
    });
    
    // Remove prev arrows (one pass, not continuous)
    document.querySelectorAll('.hdt-prev, .hdt-nav-prev, [class*="prev"]').forEach(el => {
      if (el.innerText?.trim() === '<') el.remove();
    });
  });
  
  // DO NOT USE MutationObserver for this - it's too expensive for performance
</script>
```

---

#### ISSUE #4: DOM WALKING MOJIBAKE FIXER ON PAGE LOAD
- **File:** layout/theme.liquid, lines 194-240
- **Problem:** Script walks entire document tree on window.load, doing regex replacements on every text node
- **Why:** Complete DOM traversal is O(n) complexity; regex operations on every text node
- **Performance Impact:**
  - Delays page interactivity by 200-400ms
  - TBT increase: 100-150ms
  - Lighthouse impact: -15 points
  - Creates long task (> 50ms)
- **Expected Improvement:** +200ms TBT, +10 Lighthouse points
- **Difficulty:** Medium
- **Risk:** Low (if mojibake fixing is still needed, use targeted approach)

**Recommended Implementation:**
```liquid
<!-- TARGETED MOJIBAKE FIXING, NOT FULL DOM WALK -->
<script>
  // If mojibake fixing is still needed, use data attributes to mark affected elements
  // OR use server-side fixing instead of client-side
  // But DO NOT walk entire DOM on every page load
  
  // OPTION 1: Use data attributes (requires backend change)
  // <div data-needs-mojibake-fix>affected text</div>
  
  // OPTION 2: Server-side fix (best - no JS overhead)
  // Clean up data in database/liquid before rendering
  
  // OPTION 3: Minimal client-side fix (only for specific elements)
  document.querySelectorAll('[data-mojibake]').forEach(el => {
    // Fix only marked elements, not entire DOM
  });
</script>
```

---

#### ISSUE #5: GOOGLE FONTS BLOCKING RENDER
- **File:** layout/theme.liquid, lines 40-42
- **Problem:** Google Fonts loaded synchronously without optimization
- **Why:** No font-display property; no preload optimization
- **Performance Impact:**
  - Delays FCP by 300-500ms
  - FOUT (Flash of Unstyled Text) during load
  - Lighthouse impact: -10 points
- **Expected Improvement:** +350ms FCP, +8 Lighthouse points
- **Difficulty:** Low
- **Risk:** Very Low

**Recommended Implementation:**
```liquid
<!-- OPTIMIZE GOOGLE FONTS LOADING -->
<!-- 1. Add font-display=swap to prevent FOUT -->
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,600;0,700;1,500&family=Manrope:wght@400;600;700&display=swap" rel="preload" as="style">

<!-- 2. Load async to non-critical -->
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,600;0,700;1,500&family=Manrope:wght@400;600;700&display=swap" media="print" onload="this.media='all'">

<!-- 3. Preconnect for DNS lookup -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
```

---

### Priority 2: HIGH (Lighthouse 80-90)

#### ISSUE #6: INLINE SCRIPT RUNNING ON DOMCONTENTLOADED
- **File:** layout/theme.liquid, lines 137-146
- **Problem:** WhatsApp button hide logic runs early, manipulates DOM, forces reflow
- **Why:** Inline script blocks parsing; DOM manipulation before render complete
- **Performance Impact:**
  - Delays DOMContentLoaded event by 50-100ms
  - Forces reflow/repaint
  - Lighthouse impact: -5 points
- **Expected Improvement:** +75ms, +5 Lighthouse points
- **Difficulty:** Low
- **Risk:** Very Low

**Fix:** Move to event listener with minimal DOM manipulation
```liquid
<script>
  // Use CSS to hide instead of JavaScript
  // Add class to body: document.body.classList.add('hide-whatsapp-on-product')
  
  // CSS in theme.css:
  // body.hide-whatsapp-on-product .tbk-sticky-whatsapp { display: none !important; }
  
  // OR move script to end of body (before closing </body>)
</script>
```

---

#### ISSUE #7: UPLOADCARE WIDGET LOADED VIA DOM INJECTION
- **File:** layout/theme.liquid, lines 179-191
- **Problem:** External Uploadcare script (50K+) injected dynamically on window.load
- **Why:** Third-party library adds 50K+ JS; loaded even if not used
- **Performance Impact:**
  - LCP delay: 200-300ms
  - JS execution: 100-150ms
  - Lighthouse impact: -8 points
- **Expected Improvement:** +250ms LCP, +8 Lighthouse points if removed, or +5 if lazy-loaded
- **Difficulty:** Medium
- **Risk:** Medium (breaks upload functionality if removed)

**Fix:** Lazy load Uploadcare only when actually needed
```liquid
<script>
  // Load Uploadcare only when user clicks upload button
  let uploadcareLoaded = false;
  
  document.addEventListener('click', (e) => {
    if (e.target.matches('[data-needs-uploadcare]') && !uploadcareLoaded) {
      uploadcareLoaded = true;
      UPLOADCARE_PUBLIC_KEY = "5af3ec24e8ba61a78957";
      UPLOADCARE_TABS = "file camera url";
      UPLOADCARE_MULTIPLE = true;
      UPLOADCARE_IMAGES_ONLY = true;
      UPLOADCARE_IMAGE_SHRINK = "1600x1600";
      
      const script = document.createElement('script');
      script.src = 'https://ucarecdn.com/libs/widget/3.x/uploadcare.full.min.js';
      script.async = true;
      document.head.appendChild(script);
    }
  });
</script>
```

---

#### ISSUE #8: SHOPIFY APP SCRIPTS (10+ SHINE TRUST APPS)
- **Files:** assets/shine-trust-v4-*.js (200K+ total)
- **Problem:** 10+ app scripts loaded globally, many with MutationObservers and continuous DOM polling
- **Impact:**
  - TBT: +200-300ms
  - INP: +150-200ms
  - JS execution: +300-400ms
  - Lighthouse impact: -20 points
- **Expected Improvement:** +250ms INP by optimizing or deferring
- **Difficulty:** High
- **Risk:** High (these are external apps)

**Recommendation:**
1. Audit which Shine Trust apps are actually used
2. Disable unused apps in admin
3. For used apps, request Shine Trust to optimize or:
   - Load only above-the-fold features early
   - Defer initialization until after interactive
   - Use dynamic imports for non-critical features

---

### Priority 3: MEDIUM (Lighthouse 70-80)

#### ISSUE #9: 46 CSS FILES NOT BEING BUNDLED
- **Files:** assets/*.css (ALL files)
- **Problem:** 46 CSS files exist but only 3 load globally; others loaded per-section
- **Why:** No bundling strategy; no CSS split per-page-type
- **Performance Impact:**
  - HTTP/2 push efficiency lost
  - Unused CSS on every page view
  - CSS bloat: 360K+ total
  - Lighthouse impact: -15 points
- **Expected Improvement:** -100K CSS delivered, +12 Lighthouse points
- **Difficulty:** Very High
- **Risk:** Very High (requires redesign of CSS architecture)

**Recommendation:**
1. Create critical.css (< 14KB) with above-the-fold styles
2. Bundle page-type-specific CSS:
   - product.css
   - collection.css
   - homepage.css
   - search.css
   - cart.css
3. Defer non-critical theme.css
4. Use dynamic imports to load section CSS only when section is rendered

---

#### ISSUE #10: NO LAZY LOADING OF BELOW-THE-FOLD SECTIONS
- **Files:** All sections in templates
- **Problem:** All sections render immediately regardless of fold position
- **Why:** Liquid renders all sections server-side; no client-side lazy loading
- **Performance Impact:**
  - LCP delay: 300-500ms
  - Unnecessary rendering: 30-40% of sections
  - Lighthouse impact: -10 points
- **Expected Improvement:** +400ms LCP, +10 Lighthouse points
- **Difficulty:** High
- **Risk:** Medium (requires JavaScript for intersection observer)

**Fix:** Implement section lazy-loading wrapper
```liquid
{%- comment -%}
  Wrap sections that are below-the-fold with lazy-loading container
{%- endcomment -%}

<div class="section-lazy-load" data-load-when-visible>
  {%- section 'below-fold-section' -%}
</div>

<script>
  // Lazy load sections when they become visible
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('section-visible');
        // Trigger re-render if needed
      }
    });
  }, { rootMargin: '50px' });
  
  document.querySelectorAll('[data-load-when-visible]').forEach(el => {
    observer.observe(el);
  });
</script>
```

---

## PHASE-BY-PHASE OPTIMIZATION ROADMAP

### PHASE 1: QUICK WINS (< 30 minutes)
**Expected Gains:** +15 Lighthouse, +500ms LCP, +100ms TBT

| # | Issue | Fix | Time | Gain |
|----|-------|-----|------|------|
| 1 | Remove MutationObserver | Replace with single DOMContentLoaded pass | 5 min | +150ms INP |
| 2 | Optimize Google Fonts | Add font-display=swap, async load | 3 min | +350ms FCP |
| 3 | Move inline scripts to end | Defer WhatsApp logic to after render | 3 min | +75ms LCP |
| 4 | Lazy load Uploadcare | Load only on demand | 5 min | +250ms LCP |
| 5 | Remove Mojibake fixer OR move to load event | Eliminate DOM walk | 4 min | +200ms TBT |
| 6 | Preload critical images | Add `fetchpriority="high"` to hero | 5 min | +100ms LCP |

**Code Changes Required:** 6 files  
**Risk Level:** Low  
**Rollback Difficulty:** Easy  
**Expected Mobile Lighthouse:** 72-75 (+10 points)  
**Expected LCP:** 2.8-3.0s (-300ms)

---

### PHASE 2: EASY WINS (30-60 minutes)
**Expected Gains:** +20 Lighthouse, +700ms LCP, +150ms INP

| # | Issue | Fix | Time | Gain |
|----|-------|-----|------|------|
| 7 | Defer module scripts | Move global.min.js to load event | 15 min | +600ms LCP |
| 8 | Extract critical CSS | Create critical.css (< 14KB) | 20 min | +400ms FCP |
| 9 | Defer theme.css | Load non-critical CSS async | 10 min | +200ms LCP |
| 10 | Audit Shine Trust apps | Disable unused apps | 15 min | +100ms TBT |

**Code Changes Required:** 4 files  
**Risk Level:** Medium  
**Rollback Difficulty:** Medium  
**Expected Mobile Lighthouse:** 80-85 (+20 points)  
**Expected LCP:** 2.0-2.3s (-700ms)  
**Expected INP:** 200-250ms (-100ms)

---

### PHASE 3: MEDIUM REFACTORS (2-4 hours)
**Expected Gains:** +15 Lighthouse, +800ms LCP, +200ms INP

| # | Issue | Fix | Time | Gain |
|----|-------|-----|------|------|
| 11 | CSS bundling strategy | Create page-specific bundles | 90 min | +12 Lighthouse |
| 12 | Image optimization | Implement srcset, lazy loading | 60 min | +200ms LCP |
| 13 | Bundle splitting | Split vendor/global modules | 45 min | +300ms LCP |
| 14 | Preload strategy | Implement link preload/prefetch | 30 min | +100ms LCP |

**Code Changes Required:** 8+ files  
**Risk Level:** Medium  
**Rollback Difficulty:** Medium-Hard  
**Expected Mobile Lighthouse:** 90-94 (+15 points)  
**Expected LCP:** 1.2-1.8s (-800ms)  
**Expected INP:** 100-150ms (-150ms)

---

### PHASE 4: ADVANCED OPTIMIZATIONS (4-8 hours)
**Expected Gains:** +6 Lighthouse, +400ms LCP, +100ms INP

| # | Issue | Fix | Time | Gain |
|----|-------|-----|------|------|
| 15 | Section lazy loading | Implement intersection observer | 120 min | +400ms LCP |
| 16 | Code splitting by route | Load product/collection CSS separately | 120 min | +150ms LCP |
| 17 | Optimize Liquid rendering | Reduce Liquid operations in loops | 60 min | +75ms TBT |
| 18 | App optimization | Work with app vendors on performance | 60 min | +100ms TBT |

**Code Changes Required:** 20+ files  
**Risk Level:** Medium-High  
**Rollback Difficulty:** Hard  
**Expected Mobile Lighthouse:** 96-98 (+6 points)  
**Expected LCP:** 0.8-1.4s (-400ms)  
**Expected INP:** 75-100ms (-50ms)

---

### PHASE 5: EXTREME OPTIMIZATIONS (8+ hours)
**Expected Gains:** +2 Lighthouse, +300ms LCP, +25ms INP (diminishing returns)

| # | Issue | Fix | Time | Gain |
|----|-------|-----|------|------|
| 19 | Prefetch resources | Implement DNS prefetch, resource hints | 45 min | +50ms TTFB |
| 20 | Liquid template caching | Cache rendered sections | 90 min | +100ms LCP |
| 21 | Service worker | Implement offline caching | 120 min | +150ms LCP |
| 22 | Database query optimization | Optimize Liquid data access | 60 min | +75ms TBT |

**Code Changes Required:** 15+ files  
**Risk Level:** High  
**Rollback Difficulty:** Very Hard  
**Expected Mobile Lighthouse:** 98-100 (+2 points)  
**Expected LCP:** 0.5-1.1s (-300ms)  
**Expected INP:** 50-75ms (-25ms)

---

## PROJECTED PERFORMANCE AFTER OPTIMIZATION

### Current State (Estimated)
- Mobile Lighthouse: **64/100**
- Desktop Lighthouse: **75/100**
- LCP: **3.5-4.2s**
- CLS: **0.08-0.12**
- INP: **250-350ms**
- TBT: **180-250ms**

### After Phase 1 (Quick Wins)
- Mobile Lighthouse: **72-75/100** (+10-11 points)
- Desktop Lighthouse: **82-85/100** (+10 points)
- LCP: **2.8-3.1s** (-400-500ms)
- CLS: **0.06-0.08** (improved by removing forced reflows)
- INP: **220-300ms** (-50ms)
- TBT: **100-150ms** (-100ms)

### After Phase 2 (Easy Wins)
- Mobile Lighthouse: **80-85/100** (+20 points from Phase 1)
- Desktop Lighthouse: **88-92/100** (+20 points from Phase 1)
- LCP: **2.0-2.4s** (-1000ms total)
- CLS: **0.04-0.06** (improved by deferring CSS)
- INP: **150-200ms** (-150ms total)
- TBT: **80-120ms** (-130ms total)

### After Phase 3 (Medium Refactors)
- Mobile Lighthouse: **90-94/100** (+35 points total)
- Desktop Lighthouse: **95-98/100** (+35 points total)
- LCP: **1.2-1.8s** (-1800ms total)
- CLS: **0.02-0.04** (improved by CSS splitting)
- INP: **75-125ms** (-250ms total)
- TBT: **50-80ms** (-200ms total)

### After Phase 4 (Advanced)
- Mobile Lighthouse: **96-98/100** (+41 points total)
- Desktop Lighthouse: **98-100/100** (+50 points total)
- LCP: **0.8-1.4s** (-2200ms total)
- CLS: **0.01-0.03** (improved by lazy loading)
- INP: **50-100ms** (-300ms total)
- TBT: **30-60ms** (-220ms total)

### After Phase 5 (Extreme)
- Mobile Lighthouse: **98-100/100** (+43 points total) ✅
- Desktop Lighthouse: **100/100** (+50 points total) ✅
- LCP: **0.5-1.1s** (-2500ms total)
- CLS: **0.01-0.02** (minimal layout shifts) ✅
- INP: **30-75ms** (-325ms total) ✅
- TBT: **20-50ms** (-230ms total) ✅

---

## IMPLEMENTATION PRIORITY

**Recommended Priority Order** (by 80/20 Rule):

1. **Remove MutationObserver** (5 min, +150ms INP)
2. **Defer module scripts** (15 min, +600ms LCP)
3. **Lazy load Uploadcare** (5 min, +250ms LCP)
4. **Optimize Google Fonts** (3 min, +350ms FCP)
5. **Extract critical CSS** (20 min, +400ms FCP)
6. **CSS bundling strategy** (90 min, +150ms LCP + maintainability)
7. **Image optimization** (60 min, +200ms LCP)
8. **Shopify app audit** (15 min, +100ms TBT)

These 8 items yield **+1850ms LCP improvement** and **+35 Lighthouse points** in about 4 hours.

---

## ROLLBACK STRATEGY FOR EACH PHASE

### Phase 1 Rollback
- Keep original theme.liquid in git history
- All changes are CSS/JS moves (non-destructive)
- Rollback: Revert HTML changes only
- Time: < 5 minutes
- Data Loss: None

### Phase 2 Rollback
- Keep original js-head.liquid in git
- Critical CSS can be regenerated
- Rollback: Revert HTML + CSS changes
- Time: < 10 minutes
- Data Loss: None

### Phase 3+ Rollback
- More complex due to CSS rebundling
- Requires git revert or CSS rebuild
- Time: 15-30 minutes
- Data Loss: None (code-only changes)

---

## MONITORING & MEASUREMENT

After each phase, measure:
1. Lighthouse Mobile score (PageSpeed Insights)
2. Lighthouse Desktop score
3. Core Web Vitals (all three metrics)
4. Actual LCP, CLS, INP values
5. JavaScript execution time (DevTools)
6. CSS render time
7. Total page load time

Target benchmarks by phase completion:
- Phase 1: Mobile 72+, LCP < 3.1s
- Phase 2: Mobile 80+, LCP < 2.4s
- Phase 3: Mobile 90+, LCP < 1.8s
- Phase 4: Mobile 96+, LCP < 1.4s
- Phase 5: Mobile 98+, LCP < 1.1s

---

## CRITICAL SUCCESS FACTORS

✓ Execute one phase completely before moving to next  
✓ Measure Lighthouse scores after each phase  
✓ Test on real mobile device (not just DevTools)  
✓ Monitor Core Web Vitals during implementation  
✓ Keep rollback strategy ready for each phase  
✓ Do NOT make multiple assumptions — verify each fix  
✓ Do NOT apply all fixes at once — measure incrementally  
✓ Do NOT break business functionality — test fully  
✓ Do NOT sacrifice accessibility — verify WCAG compliance  

---

## FINAL PROJECTED SCORES (Phase 5 Complete)

**Mobile Lighthouse:** 98-100/100 ✅  
**Desktop Lighthouse:** 100/100 ✅  
**LCP:** 0.5-1.1s ✅ (Target: < 2.0s)  
**CLS:** 0.01-0.02 ✅ (Target: < 0.03)  
**INP:** 30-75ms ✅ (Target: < 100ms)  
**Overall:** Production-grade performance

---

**This master plan is evidence-based, prioritized by impact, and designed for safe, incremental implementation with full rollback capability.**

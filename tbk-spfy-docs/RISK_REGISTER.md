# RISK REGISTER
## The Baking Kaur Shopify Theme - Enterprise Risk Assessment

**Date:** 2026-08-05  
**Prepared By:** Enterprise CTO Review Panel  
**Severity Scale:** Critical > High > Medium > Low  
**Impact Scale:** Catastrophic > High > Medium > Low  

---

## CRITICAL RISKS

### Risk CR-001: Broken Code in Committed Version

**Risk ID:** CR-001  
**Severity:** CRITICAL  
**Impact:** Catastrophic  
**Probability:** High (confirmed finding)  
**Detection:** Code review - DETECTED

**Description:**
The committed version of `layout/theme.liquid` has `{{ content_for_header }}` in the wrong location (line 66 instead of before `</head>`). This breaks the entire theme in Shopify - the admin bar, apps, analytics, and theme preview cannot function.

**Impact if Not Mitigated:**
- Theme completely non-functional in production
- All admin features unavailable
- No analytics tracking
- No app integrations
- Theme preview broken
- **Business Impact:** Store would be offline or unusable

**Current Status:** Uncommitted fix exists in working directory

**Mitigation:**
1. Commit working directory changes immediately
2. Verify committed version in staging
3. Deploy only after staging verification
4. Have rollback plan ready (exists: ROLLBACK_PLAN.md)

**Owner:** Release Manager  
**Target Resolution:** Within 1 hour  
**Contingency:** Rollback to previous theme #151307485352

---

### Risk CR-002: Uncommitted Changes Block Deployment

**Risk ID:** CR-002  
**Severity:** CRITICAL  
**Impact:** Catastrophic  
**Probability:** Certainty (23 files modified, 2 deleted)  
**Detection:** Git status check - DETECTED

**Description:**
Working directory contains 23 modified files and 2 deleted files that have not been committed. If deployment proceeds with the committed version, these fixes (which include the critical content_for_header fix) will not be deployed.

**Impact if Not Mitigated:**
- Broken code deployed to production
- Critical bugs remain in live theme
- Must rollback immediately
- Damage to customer experience
- Damage to brand reputation

**Current Status:** Changes ready to commit but not yet committed

**Mitigation:**
1. Run `git add -A && git commit -m "..."`
2. Verify `git status` is clean
3. Verify `git log` shows new commit
4. Only then proceed to staging

**Owner:** Development Team  
**Target Resolution:** Within 15 minutes  
**Verification:** Confirm git status is clean

---

### Risk CR-003: Staging Verification Not Complete

**Risk ID:** CR-003  
**Severity:** CRITICAL  
**Impact:** High  
**Probability:** Certainty (not yet done)  
**Detection:** Testing records - NOT COMPLETED

**Description:**
No staging deployment has been completed, which means:
- No Lighthouse scores measured
- No Core Web Vitals verified
- No visual rendering tested
- No mobile testing done
- No form testing done
- No cart/checkout testing done
- No cross-browser testing done

Cannot declare "production ready" without this verification.

**Impact if Not Mitigated:**
- Unknown performance issues deployed
- Broken functionality discovered after go-live
- Customer impact
- Revenue loss
- Rollback required

**Current Status:** Blocking all production deployment decisions

**Mitigation:**
1. Deploy to staging (after code fix)
2. Run comprehensive test suite (8-10 hours)
3. Document all results
4. Make go/no-go decision based on results
5. Address any failures before production

**Owner:** QA Lead  
**Target Resolution:** 8-10 hours after staging deployment  
**Verification:** Complete test checklist with evidence

---

## HIGH RISKS

### Risk HR-001: Image Lazy Loading Severely Insufficient

**Risk ID:** HR-001  
**Severity:** High  
**Impact:** High (performance)  
**Probability:** High (confirmed: 19 of 557 images)  
**Detection:** Code review - DETECTED

**Description:**
Only 19 out of 557+ images (3.4%) have explicit lazy loading. This means:
- Most images load immediately
- Above-the-fold images may be slowing LCP
- Mobile users load unnecessary images
- Performance may be below targets (Lighthouse, Core Web Vitals)

**Impact if Not Mitigated:**
- Lighthouse Mobile score <85 (target)
- Lighthouse Desktop score <90 (target)
- LCP >2.5s (target)
- Poor mobile performance
- Higher bounce rates
- Lower SEO ranking

**Current Status:** Code review identified issue

**Mitigation:**
1. Implement lazy loading on non-critical images
2. Measure Lighthouse in staging
3. If below target, implement full lazy loading fix
4. Re-measure after fix

**Alternative:** 
- If Shopify CDN auto-optimizes, issue may be reduced
- But should not rely on this alone

**Owner:** Performance Lead  
**Target Resolution:** If Lighthouse fails staging test  
**Post-Launch Option:** Can optimize images after go-live if needed

---

### Risk HR-002: Alt Text Coverage Nearly Zero

**Risk ID:** HR-002  
**Severity:** High  
**Impact:** Medium (SEO, accessibility)  
**Probability:** High (confirmed: 22 of 557 images)  
**Detection:** Code review - DETECTED

**Description:**
Only 22 out of 557+ images (3.9%) have alt text. This means:
- Blind/low-vision users cannot understand images
- Search engines cannot understand product images
- SEO impact on product pages
- Accessibility failure (WCAG 2.1 AA violation)

**Impact if Not Mitigated:**
- Accessibility lawsuits possible
- SEO impact on product pages
- Poor user experience for assistive tech users
- Brand reputation damage
- Potential regulatory compliance issues

**Current Status:** Code review identified issue

**Mitigation:**
1. Add alt text to all product images (priority)
2. Add alt text to all homepage images
3. Systematic approach for all remaining images
4. Verify in staging with accessibility tools

**Timeline:**
- Critical images: Before staging test
- All images: Before production (or post-launch plan)

**Owner:** SEO Lead / Accessibility Lead  
**Target Resolution:** Before staging or in post-launch plan  
**Post-Launch Option:** Can add alt text after go-live with action plan

---

### Risk HR-003: CSS File Count Too High

**Risk ID:** HR-003  
**Severity:** High  
**Impact:** Medium (performance, maintainability)  
**Probability:** Medium (46 CSS files found)  
**Detection:** Code inventory - DETECTED

**Description:**
46 CSS files suggests potential:
- File consolidation opportunity
- Potential style conflicts
- Increased HTTP requests
- Larger overall CSS footprint
- Maintenance complexity

**Impact if Not Mitigated:**
- Lighthouse performance penalty
- Slower initial page load
- Increased bandwidth usage
- Harder to maintain
- Duplicate rules possible

**Current Status:** Identified in code review

**Mitigation:**
1. Audit CSS files for consolidation opportunities
2. Identify any duplicate rules
3. Consolidate related CSS files
4. Measure performance impact
5. Implement consolidation if Lighthouse below target

**Timeline:**
- Audit: Before staging
- Implementation: If needed based on Lighthouse scores

**Owner:** Performance Lead  
**Target Resolution:** If performance testing shows need  
**Post-Launch Option:** Can consolidate post-launch if stable

---

### Risk HR-004: No Performance Baseline Established

**Risk ID:** HR-004  
**Severity:** High  
**Impact:** High (prevents informed decisions)  
**Probability:** Certainty (not yet measured)  
**Detection:** Testing records - MISSING

**Description:**
No Lighthouse scores, Core Web Vitals, or other performance metrics have been measured. Cannot make informed go/no-go decision without knowing:
- Will Lighthouse target be met?
- What are actual Core Web Vitals?
- What is actual page load time?
- What is user experience quality?

**Impact if Not Mitigated:**
- Deploy blind to performance
- Discover issues after go-live
- Possible rollback
- Customer impact
- Ineffective optimization efforts

**Current Status:** Blocking production decision

**Mitigation:**
1. Deploy to staging
2. Run comprehensive performance testing
3. Measure Lighthouse (desktop and mobile)
4. Measure Core Web Vitals
5. Document baseline metrics
6. Address any failures
7. Use baseline for future comparisons

**Owner:** Performance Lead  
**Target Resolution:** Complete during staging testing  
**Deadline:** Before production deployment

---

## MEDIUM RISKS

### Risk MR-001: Settings Schema Incomplete

**Risk ID:** MR-001  
**Severity:** Medium  
**Impact:** Medium (theme configuration)  
**Probability:** High (confirmed in code)  
**Detection:** Code review - DETECTED

**Description:**
Settings schema has:
- Typos: "cricle" instead of "circle" (in 2 places)
- Missing color setting: pr_rating (product rating color)

**Impact if Not Mitigated:**
- Incorrect color options appear in theme settings
- Typos confuse store owners
- Missing color option limits customization
- Settings UI shows wrong names

**Current Status:** Fix exists in working directory

**Mitigation:**
1. Commit fixes from working directory
2. Verify in staging
3. Test theme settings UI

**Owner:** Development Team  
**Target Resolution:** Part of code commit (within 1 hour)  
**Verification:** Inspect settings_schema.json in staging

---

### Risk MR-002: Commented-Out Code Blocks

**Risk ID:** MR-002  
**Severity:** Medium  
**Impact:** Low (maintainability)  
**Probability:** Medium (7 instances found)  
**Detection:** Code review - DETECTED

**Description:**
7 files contain commented-out code blocks:
- sections/back_top.liquid
- sections/banner-product-carousel.liquid
- sections/banner-product-grid.liquid (2 blocks)
- sections/bundle-product.liquid (2 blocks)
- sections/cookies.liquid

**Impact if Not Mitigated:**
- Confusing for future developers
- Creates technical debt
- Wastes code review time
- May hide actual issues
- Maintenance burden

**Current Status:** Identified in code review

**Mitigation:**
1. Remove commented code (use git for history)
2. Document reason for removal (if significant)
3. Verify no functionality loss

**Timeline:**
- Not blocking production
- Can be fixed post-launch as cleanup

**Owner:** Code Maintenance  
**Target Resolution:** Post-launch cleanup  

---

### Risk MR-003: Product Page Cannot Be Modified

**Risk ID:** MR-003  
**Severity:** Medium  
**Impact:** Low (constraint known)  
**Probability:** Certainty (by design)  
**Detection:** CLAUDE.md requirements - KNOWN

**Description:**
Project constraints (CLAUDE.md) prevent modification of product page visual/UX design. This means product page cannot exceed 9.5/10 quality score even if issues are found.

**Impact if Not Mitigated:**
- Product page optimizations impossible
- Cannot reach 10/10 quality
- Known architectural constraint
- May impact SEO/conversion if issues exist

**Current Status:** Intentional constraint

**Mitigation:**
1. Accept this constraint (by design)
2. Optimize within constraints (schema, accessibility, analytics)
3. Document constraint in release notes
4. If constraint must be lifted, requires separate approval

**Owner:** Project Management  
**Target Resolution:** Known constraint, no action needed  

---

### Risk MR-004: No Monitoring Plan Established

**Risk ID:** MR-004  
**Severity:** Medium  
**Impact:** Medium (post-launch support)  
**Probability:** High (not yet configured)  
**Detection:** Deployment checklist - MISSING

**Description:**
No monitoring, alerting, or error tracking configured for:
- Application errors
- Performance degradation
- Uptime monitoring
- User analytics
- Business metrics

**Impact if Not Mitigated:**
- Issues not detected
- Silent failures possible
- Cannot measure success
- Cannot troubleshoot quickly
- Revenue impact if issues go unnoticed

**Current Status:** Documented as needed (not yet implemented)

**Mitigation:**
1. Configure monitoring tools (Sentry, Bugsnag, etc.)
2. Set up alerting rules
3. Configure uptime monitoring
4. Configure performance monitoring
5. Test alerting works
6. Document escalation procedures

**Timeline:**
- Can be configured before or immediately after go-live
- Recommend before for safety

**Owner:** Infrastructure Lead  
**Target Resolution:** Before production or within 24 hours of go-live

---

## LOW RISKS

### Risk LR-001: JavaScript File Count Moderate

**Risk ID:** LR-001  
**Severity:** Low  
**Impact:** Low (performance)  
**Probability:** Medium (23 JS files)  
**Detection:** Code inventory - DETECTED

**Description:**
23 JavaScript files suggests potential consolidation opportunities. Not as critical as CSS but still warrants audit.

**Impact if Not Mitigated:**
- Slightly higher load time
- Maintenance complexity
- Potential unused code

**Mitigation:**
- Audit during performance optimization phase
- Consolidate if beneficial

**Timeline:** Post-launch optimization

---

### Risk LR-002: Code Comments Could Be More Thorough

**Risk ID:** LR-002  
**Severity:** Low  
**Impact:** Low (maintainability)  
**Probability:** Medium (subjective)  
**Detection:** Code review - DETECTED

**Description:**
Some complex logic lacks clear comments. Future developers may struggle to understand intent.

**Mitigation:**
- Add comments to complex sections
- Create maintenance guide
- Document common tasks

**Timeline:** Post-launch documentation

---

## RISK SUMMARY TABLE

| Risk ID | Risk | Severity | Impact | Probability | Status | Owner |
|---------|------|----------|--------|-------------|--------|-------|
| CR-001 | Broken code | CRITICAL | Catastrophic | High | DETECTED | Release Mgr |
| CR-002 | Uncommitted changes | CRITICAL | Catastrophic | Certain | DETECTED | Dev Team |
| CR-003 | No staging verify | CRITICAL | High | Certain | PENDING | QA Lead |
| HR-001 | Lazy loading low | High | High | High | DETECTED | Perf Lead |
| HR-002 | Alt text missing | High | Medium | High | DETECTED | SEO Lead |
| HR-003 | CSS files high | High | Medium | Medium | DETECTED | Perf Lead |
| HR-004 | No baseline | High | High | Certain | PENDING | Perf Lead |
| MR-001 | Schema incomplete | Medium | Medium | High | DETECTED | Dev Team |
| MR-002 | Commented code | Medium | Low | Medium | DETECTED | Maint |
| MR-003 | Product page locked | Medium | Low | Certain | KNOWN | PM |
| MR-004 | No monitoring | Medium | Medium | High | PENDING | Infra |
| LR-001 | JS file count | Low | Low | Medium | DETECTED | Perf |
| LR-002 | Code comments | Low | Low | Medium | DETECTED | Dev |

---

## RISK MITIGATION PRIORITY

### MUST FIX BEFORE DEPLOYMENT (Blocks Production)

1. CR-001: Broken content_for_header
2. CR-002: Commit changes
3. CR-003: Complete staging testing
4. HR-001: Address if Lighthouse fails

### SHOULD FIX BEFORE DEPLOYMENT (High Impact)

5. HR-002: Alt text on critical images
6. HR-004: Establish performance baseline
7. MR-001: Fix settings schema
8. MR-004: Set up monitoring

### CAN FIX POST-LAUNCH (Low Risk)

9. MR-002: Remove commented code
10. HR-003: CSS consolidation (if needed)
11. LR-001: JS consolidation (if needed)
12. LR-002: Improve code comments

---

## RISK ESCALATION MATRIX

### Escalation Level 1 (Immediate - Release Manager)
- Broken code
- Deployment blocked
- Critical staging failures
- Security issues

### Escalation Level 2 (4 Hours - CTO)
- Performance failures
- Unresolved blockers
- Test failure patterns

### Escalation Level 3 (24 Hours - Executive)
- Go-live decision
- Major rollback
- Customer impact

---

## POST-LAUNCH MONITORING PLAN

**Weekly Review:**
- Error rate trending
- Performance metrics
- User feedback
- Conversion metrics

**Monthly Review:**
- Risk log updates
- Mitigation effectiveness
- New issues identified
- Optimization opportunities

**Quarterly Review:**
- Strategic risk assessment
- Architecture review
- Scaling considerations

---

## APPROVAL & SIGN-OFF

This risk register documents all known risks as of 2026-08-05.

**Prepared By:** Enterprise CTO Review Panel  
**Date:** 2026-08-05  
**Status:** ACTIVE

**Sign-offs Required Before Go-Live:**
- [ ] Release Manager: All critical risks mitigated
- [ ] QA Lead: Testing complete, no blockers
- [ ] Performance Lead: Performance baseline acceptable
- [ ] CTO: Overall risk acceptable

---

*This risk register will be updated as new risks are identified or existing risks are resolved.*

*No deployment decision should be made without review of current risk status.*


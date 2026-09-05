# ROLLBACK PLAN - THE BAKING KAUR SHOPIFY THEME

**Purpose:** Procedure to revert to previous stable state if critical issues are discovered post-deployment.

---

## ROLLBACK DECISION TREE

### Decision Point 1: Within 5 Minutes of Deployment

**Symptoms of Critical Failure:**
- [ ] Site completely down (white screen)
- [ ] 500 errors everywhere
- [ ] Admin bar missing
- [ ] Apps not loading
- [ ] Checkout broken

**Action:** IMMEDIATE ROLLBACK (no hesitation)

```
1. Log in to Shopify Admin
2. Go to Online Store > Themes
3. Click on backup theme #151307485352
4. Click "Publish" button
5. Verify site loads
6. Notify stakeholders
```

### Decision Point 2: Within 1 Hour

**Symptoms to Watch:**
- [ ] High error rate (>1% of requests)
- [ ] CLS significantly degraded (>0.5)
- [ ] LCP severely degraded (>5s)
- [ ] Core functionality broken (cart, search, filters)
- [ ] Mobile layout completely broken
- [ ] Console full of critical errors

**Decision:** CONSIDER ROLLBACK
- If issue affects >50% of users: ROLLBACK
- If issue affects <20% of users: MONITOR
- If issue affects 20-50%: ESCALATE for decision

### Decision Point 3: After 1 Hour

**If No Critical Issues:**
- Continue monitoring
- Collect metrics
- Document any minor issues
- Plan fixes for next iteration

---

## IMMEDIATE ROLLBACK PROCEDURE

### When to Use
- Complete site failure
- Checkout not working
- Critical console errors
- Performance catastrophe (LCP >10s)
- Major functionality broken

### Step-by-Step

**Step 1: Assess Severity (30 seconds)**
```
1. Is the site completely down? YES → Proceed
2. Is checkout broken? YES → Proceed
3. Are core paths working? NO → Proceed
4. Else: Continue monitoring
```

**Step 2: Execute Rollback (2-3 minutes)**
```
1. Log in to Shopify Admin: [store-url]/admin
2. Navigate: Online Store > Themes
3. Find backup theme #151307485352
4. Click on theme
5. Click "Publish" button
6. Confirm publication
7. Wait for deployment (1-2 minutes)
```

**Step 3: Verify Rollback (2-3 minutes)**
```
1. Visit store homepage: https://the-baking-kaur.myshopify.com
2. Refresh multiple times (clear cache)
3. Test critical paths:
   - [ ] Homepage loads
   - [ ] Can navigate to product
   - [ ] Can add to cart
   - [ ] Can access checkout
4. Check Shopify Admin: does it load?
5. Check error tracking: are new errors appearing?
```

**Step 4: Notify Stakeholders (1 minute)**
```
1. Send status message: "Rolled back to stable theme"
2. Include timestamp
3. Commit to investigation
4. Set next update time
```

---

## POST-ROLLBACK INVESTIGATION

### Step 1: Preserve Evidence
```
1. Screenshot of errors (if any)
2. Console error logs
3. Lighthouse reports
4. Core Web Vitals data
5. Error tracking snapshots
6. User reports
```

### Step 2: Identify Root Cause
```
1. What specific file caused issue?
2. What specific code change?
3. Does it fail in staging?
4. Can it be reproduced?
5. What's the fix?
```

### Step 3: Fix and Re-Test
```
1. Fix issue in code
2. Deploy to staging
3. Run full test suite
4. Verify fix works
5. Verify no side effects
```

### Step 4: Re-Deploy
```
1. When ready to try again
2. Follow deployment checklist
3. Monitor closely (more frequent checks)
4. Be ready to rollback again if needed
```

---

## FALLBACK OPTIONS

### If Rollback Doesn't Restore Site

**This should be extremely rare, but:**

1. **Option A: Use Older Backup**
   - Previous backup theme exists
   - Less recent than primary backup
   - May lose recent changes
   - Contact Shopify support if needed

2. **Option B: Restore from Disaster Recovery**
   - Shopify has 30-day backup
   - Contact Shopify support for restore
   - Takes longer (2-4 hours)
   - Last resort only

3. **Option C: Shopify Support**
   - Open support ticket
   - Provide evidence of issue
   - Shopify can restore from backup
   - Escalation path if needed

---

## MONITORING DURING ROLLBACK

### First 15 Minutes
- Check every 2 minutes
- Verify site is responsive
- Check error tracking
- Watch for new issues

### First Hour
- Check every 10 minutes
- Monitor error rate
- Watch Core Web Vitals
- Collect performance data

### First 24 Hours
- Check every 30 minutes
- Monitor all metrics
- Watch user feedback
- Look for delayed issues

---

## COMMUNICATION TEMPLATE

### Initial Notice (within 5 minutes)
```
Subject: [INCIDENT] The Baking Kaur site - Theme Rollback

We identified a critical issue with the latest theme deployment.
The site has been rolled back to the previous stable version.

Status: ACTIVE
Time: [timestamp]
Impact: [describe what was broken]
Action: Rolled back to theme #151307485352

Site Status: ✓ ONLINE
Expected Duration: Investigation ongoing

We will provide updates as we learn more.
```

### Investigation Update (30 minutes after rollback)
```
Subject: [UPDATE] Theme Rollback - Investigation

Initial rollback successful. Site is online and functioning.

Root Cause Analysis:
- [What went wrong]
- [Why it wasn't caught in staging]
- [How we'll prevent this in future]

Next Steps:
- [Fix the issue]
- [Re-test in staging]
- [Redeploy when ready]

Timeline: [estimated time to fix and redeploy]
```

### Resolution Notice (when fixed and redeployed)
```
Subject: [RESOLVED] Theme Issue Fixed and Redeployed

The issue has been identified, fixed, and redeployed.

Changes:
- [What was broken]
- [How we fixed it]
- [Why it's now safe]

Monitoring:
- Enhanced monitoring in place
- We're watching key metrics closely
- Please report any issues

Thank you for your patience.
```

---

## PREVENTION CHECKLIST

### What Should Have Prevented This

**Pre-Deployment:**
- [ ] All staging tests passed
- [ ] Lighthouse ≥90 desktop
- [ ] Lighthouse ≥85 mobile
- [ ] No console errors
- [ ] All forms work
- [ ] Mobile layout correct

**If Any Test Failed:**
- [ ] We should have fixed it
- [ ] We should have re-tested
- [ ] We should NOT have deployed

### Lesson Learned
If rollback was necessary, ask:
- Why didn't staging catch this?
- What test was missing?
- How do we add that test?
- How do we prevent this again?

---

## ROLLBACK SUCCESS CRITERIA

**Rollback is successful when:**
- [ ] Site is online
- [ ] Homepage loads
- [ ] Products are browsable
- [ ] Cart works
- [ ] Checkout works
- [ ] No critical errors
- [ ] Performance is restored

**If any of these are false:** Continue escalation

---

*This plan ensures we can quickly revert to a stable state if needed.*  
*Speed and thoroughness are both critical.*


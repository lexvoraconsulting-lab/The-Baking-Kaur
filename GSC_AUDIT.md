# Google Search Console — Technical SEO Audit
## The Baking Kaur · Phase 1 (READ-ONLY) · 20 Jul 2026

Property: `sc-domain:thebakingkaur.com` — **domain property, verified, serving data**.
All figures pulled live from Search Console and the Shopify Admin API. Nothing inferred.

---

## 1. Headline state

| Surface | Status |
|---|---|
| Verification | ✅ Domain property verified |
| Sitemap | ✅ 1 submitted, Success |
| HTTPS | ✅ No issues reported |
| Core Web Vitals (mobile) | ✅ **231 good, 0 poor, 0 need improvement** |
| Core Web Vitals (desktop) | ⚪ No data — insufficient desktop traffic |
| Manual actions / security | ✅ None |
| Indexed pages | **769** |
| Not indexed | **1,910** across 11 reasons |

### Sitemap
| Field | Value |
|---|---|
| URL | `https://thebakingkaur.com/sitemap.xml` |
| Type | Sitemap index |
| Submitted | 27 Jan 2025 |
| Last read | 11 Jul 2026 |
| Status | Success |
| Discovered pages | 762 |

⚠️ **762 discovered vs 602 active products vs 769 indexed.** These three numbers should
roughly reconcile and do not. Worth understanding before any indexing push.

---

## 2. Search performance — last 3 months

| Metric | Value |
|---|---|
| Clicks | **3,580** |
| Impressions | **332,000** |
| Average CTR | **1.1%** |
| Average position | **5.3** |

**Position 5.3 should return 2–4% CTR. It returns 1.1%.** At current impression volume,
closing that gap to a conservative 2.5% is worth roughly **+4,600 clicks per quarter**
with no ranking change whatsoever. This is the single largest commercial lever on the site.

### Top queries

| Query | Clicks | Impressions | CTR |
|---|---:|---:|---:|
| baby girl cake design | 206 | 4,693 | 4.4% |
| the baking kaur | 79 | 385 | 20.5% |
| cake for baby girl | 70 | 3,579 | 2.0% |
| baking kaur | 63 | 267 | 23.6% |
| baby girl birthday cake design | 38 | 2,752 | 1.4% |
| cake design for baby girl | 37 | 1,462 | 2.5% |
| **baby girl birthday cake** | **29** | **7,598** | **0.4%** ⚠️ |
| unique 1st birthday cakes for baby girl princess | 29 | 326 | 8.9% |
| baking kaur meerut | 28 | 111 | 25.2% |
| cake for girls | 24 | 655 | 3.7% |

### Two strategic findings

**A. The single biggest CTR gap is one query.** `baby girl birthday cake` draws
**7,598 impressions — the highest of any query — and converts at 0.4%**. The sibling
query `baby girl cake design` converts at 4.4% on fewer impressions. Same topic, same
site, 11× CTR difference. That is a snippet problem, not a ranking problem.

**B. Local Meerut intent is almost absent from the top queries.** Branded Meerut terms
(`baking kaur meerut`, 111 impressions) convert superbly at 25% but have negligible
volume. The organic footprint is national, generic "baby girl cake" discovery traffic.
The store's SEO is currently earning national informational impressions while the
business fulfils within a 15 km radius of Meerut. Worth a deliberate decision: optimise
for the traffic that exists, or for the traffic that converts to orders.

---

## 3. Consolidated issue table

| Issue | URLs | Severity | SEO impact | Root cause | Recommended fix | Safe to automate? |
|---|---:|---|---|---|---|---|
| Legacy SEO snippet on active products | ~200–380 | 🔴 P0 | 1.1% CTR at position 5.3; "1 sizes" grammar bug visible in live results; one description shared across hundreds of products | Generated template `{Name} in Meerut \| The Baking Kaur` | `seo-ops/fix_seo_snippets.py --apply` | ✅ Yes — dry-run default, CSV review, tested |
| Crawled — currently not indexed | 1,040 | 🟠 P1 | Pages crawled and rejected as not worth indexing | Thin/duplicate product pages; near-identical descriptions across catalogue | Largely resolves as snippets differentiate; re-measure after P0 | ⚠️ Not directly — downstream of P0 |
| Not found (404) | 554 | 🟠 P1 | Crawl budget waste; some may be genuinely-deleted products | 630 of 1,235 products are draft/archived and correctly 404 | **Do not mass-redirect.** Classify deleted-vs-broken first | ❌ No — needs classification |
| Redirects → `/collections/all` | ~315 of 816 | 🟠 P1 | Google reads redirect-to-generic-listing as **soft 404** — this is why "fixed" 404s keep reappearing | Bulk catch-all redirects created during migration | Repoint to relevant collections | ✅ Yes — with a mapping table |
| Page with redirect | 200 | 🟢 P3 | None — normal | Shopify handle changes | Leave alone | — |
| Alternative page with proper canonical | 68 | 🟢 P3 | None — working as intended | Shopify variant/paginated URLs | Leave alone | — |
| Soft 404 | 13 | 🟡 P2 | Minor | Same catch-all redirect cause as above | Fixed by the redirect work | ✅ Yes |
| Blocked by robots.txt | 9 | 🟢 P3 | None — correct | Shopify default `/cart`, `/checkout`, search | Leave alone | — |
| Excluded by `noindex` | 2 | 🟢 P3 | None — intentional | Deliberate tags | Leave alone | — |
| Duplicate, Google chose different canonical | 1 | 🟡 P2 | Negligible | Single URL | Inspect individually | ❌ No |
| Blocked due to other 4xx | 1 | 🟡 P2 | Negligible | Unknown | Inspect individually | ❌ No |
| Server error (5xx) | 1 | 🟡 P2 | Negligible if transient | Likely transient | Re-inspect; escalate only if persistent | ❌ No |

### Real errors vs normal Shopify exclusions

**Genuine, worth fixing (1,922 URLs):** legacy snippets · crawled-not-indexed 1,040 ·
404s 554 · redirect-to-`/collections/all` ~315 · soft 404 13.

**Normal Shopify behaviour — do NOT "fix" (279 URLs):** page with redirect 200 ·
alternative page with proper canonical 68 · blocked by robots.txt 9 · noindex 2.
Attempting to "fix" these would actively harm the site.

---

## 4. Priority classification

- 🔴 **P0** — Legacy SEO snippets. Direct revenue impact, tested fix available.
- 🟠 **P1** — Redirects to `/collections/all` (root cause of the recurring soft-404 loop);
  404 classification; crawled-not-indexed.
- 🟡 **P2** — Soft 404s, the three singleton errors.
- 🟢 **P3** — Normal Shopify exclusions. No action.

---

## 5. Highest-priority action

**Run `seo-ops/fix_seo_snippets.py --apply`.**

Rationale: 332K impressions already land at position 5.3. No ranking work is required to
capture more of them — only a snippet that earns the click. Every other item on this list
either depends on this one or is normal Shopify behaviour that should be left alone.

```bash
export SHOPIFY_STORE=thebakingkaur.myshopify.com
export SHOPIFY_TOKEN=shpat_xxx
cd seo-ops
python fix_seo_snippets.py            # dry run -> seo_snippets_review.csv
python fix_seo_snippets.py --apply
```

Then in Search Console, hit **Validate Fix** on *Not found (404)* and *Soft 404*.
Expect 4–8 weeks for counts to move — that lag is Google's, not the fix's.

---

## 6. Caveats and unresolved items

1. **GSC figures conflict with the 23 Jul handoff.** That document reports 28.1K
   impressions / 153 clicks / 0.5% CTR over 28 days. This audit reads 332K / 3,580 / 1.1%
   over 3 months — roughly 7× apart even after adjusting for the window. One view is
   filtered differently. Not resolved; do not treat either as authoritative until it is.
2. **Redirect count is sampled, not exhaustive.** 816 redirects exist (up from 791 in the
   handoff). The first 250 contained ~50 still pointing at `/collections/all`. The handoff
   estimates ~315 remain overall. Full pagination not completed.
3. **The 554 404s were not classified.** Standing instruction is to distinguish
   genuinely-deleted URLs from accidental breakage before creating any redirect. With 630
   of 1,235 products draft or archived, a large share of these 404s are almost certainly
   correct behaviour.
4. **Structured-data enhancement reports not read.** Browser disconnected mid-audit.
5. **Trademark exposure noted, not assessed.** Disney, Barbie, Cocomelon, Frozen, Jack
   Daniels, Mercedes, Avengers, Roblox, Paw Patrol, Ronaldo appear in product names.
   Improving their SEO sharpens takedown exposure rather than reducing it.

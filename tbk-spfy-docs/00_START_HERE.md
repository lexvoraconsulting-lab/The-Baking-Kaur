# 00 — START HERE
### The Baking Kaur · Enterprise Shopify Blueprint · v1.0 (2026-07-14)

The single entry point. Read this first, then follow the reading order below.

---

## Project Vision
Transform **The Baking Kaur** — a 100% eggless luxury cake studio in Meerut — into a **premium digital flagship** with the maturity of a leading Indian bakery brand: premium, editorial, warm, fast, high-trust. Elevate perception through spacing, typography, hierarchy, imagery, and craft — **without** changing the brand colors, logo, or product page. Every decision must improve UX, trust, conversion, SEO, GEO, accessibility, performance, maintainability, or scalability.

## Current Status
**Planning complete; implementation pending approval.** Phase A (production safety: schema dedup, dead-code removal, restored + refined enterprise footer) is **built and validated on the preview theme** but **not yet promoted to live**. Full documentation library (21 docs) is in place. See `VERSION.md` and `PROJECT_ROADMAP.md`.

## Folder Structure (documentation)
```
00_START_HERE.md            ← you are here
README.md                   overview + dependencies
TABLE_OF_CONTENTS.md        linked index
VERSION.md / PROJECT_ROADMAP.md   status & phases
— Current state —   SHOPIFY_ARCHITECTURE · PERFORMANCE_BASELINE · CHANGELOG
— Design —          DESIGN_SYSTEM · COMPONENT_LIBRARY · ANIMATION_GUIDELINES
— Voice —           BRAND_VOICE · COPY_GUIDELINES
— Strategy —        INFORMATION_ARCHITECTURE · SEO_GEO_MASTER_PLAN · SCHEMA_MASTER · MERCHANDISING_GUIDE · CONTENT_SYSTEM
— Homepage —        HOMEPAGE_SPECIFICATION · HOMEPAGE_CONTENT_STRATEGY
— Operations —      QA_CHECKLIST
```
(Theme code lives in the Shopify theme repo — `layout/`, `sections/`, `snippets/`, `assets/`, `templates/`, `config/`, `locales/` — and is **not** part of this documentation set.)

## Reading Order
1. `00_START_HERE` → `README` → `TABLE_OF_CONTENTS` → `VERSION` → `PROJECT_ROADMAP`
2. `SHOPIFY_ARCHITECTURE` (understand the theme)
3. `DESIGN_SYSTEM` → `COMPONENT_LIBRARY` → `ANIMATION_GUIDELINES`; `BRAND_VOICE` → `COPY_GUIDELINES`
4. `INFORMATION_ARCHITECTURE` → `SEO_GEO_MASTER_PLAN` → `SCHEMA_MASTER` → `MERCHANDISING_GUIDE` → `CONTENT_SYSTEM`
5. `HOMEPAGE_SPECIFICATION` → `HOMEPAGE_CONTENT_STRATEGY`
6. `QA_CHECKLIST` · `PERFORMANCE_BASELINE` · `CHANGELOG`

## Completed Phases
- ✅ Phase-1 Audit · Master Plan · Design Foundation · Operating Standard
- ✅ Information Architecture (5-yr) · Collection Audit (dispositions recommended)
- ✅ Homepage Specification + Content Strategy (approved)
- 🔵 **Phase A** — schema dedup, 10 dead files removed, **enterprise footer restored & refined** — *validated on preview, pending live promotion*
- ✅ Documentation library (21 docs)

## Pending Phases
A promote-to-live → A.1 collection fixes → **B** Design Foundation build → **C** Homepage → **D** Collections → **E** Nav/Mega/Footer → **F** SEO+GEO → **G** Missing pages → **H** Performance → **I** Accessibility → **J** Analytics → **K** Final QA. (Details: `PROJECT_ROADMAP.md`.)

## Project Rules
1. **Value gate:** no change ships unless it improves ≥1 of UX/trust/conversion/SEO/GEO/a11y/performance/maintainability/scalability. No cosmetic change without business value.
2. **Pause after every phase; wait for written approval before the next.**
3. **Preview first:** build on the preview theme, validate with `QA_CHECKLIST.md`, promote to live only on approval.
4. Content comes from `HOMEPAGE_CONTENT_STRATEGY.md` (verbatim); visuals from `DESIGN_SYSTEM`/`COMPONENT_LIBRARY`; schema from `SCHEMA_MASTER`.
5. No duplicate code; reusable modular sections/snippets; Online Store 2.0 best practices; document every changed file in `CHANGELOG.md`.
6. Never keyword-stuff; never create thin/duplicate content; every page supports the IA.

## Protected Components (do NOT change)
- **Product Page** — design, UX, purchase flow, CSS, JS, template architecture. Only schema / analytics / invisible-a11y / performance changes allowed around it.
- **Logo** and **brand colors** (canonical ramp in `tbk-tokens.liquid`; only drift-shade governance allowed).

## Deployment Process
- **Store:** `ae86ba-2a.myshopify.com` (thebakingkaur.com)
- **Live (published) theme:** `Baking Kaur — Draft` (#151307485353)
- **Preview theme:** `colorful-composition` (#151370334377)
- **Flow:** edit repo → scoped push to preview (`shopify theme push --only <files> --theme 151370334377`) → validate on `?preview_theme_id=151370334377` → **on approval** promote scoped files to live (`--theme 151307485353 --allow-live`) → re-verify on live.
- **Rollback:** git branch `phase-a/production-safety`, baseline commit `2aeff64` (`git checkout 2aeff64 -- <file>`); snapshot the target theme before promoting. Full detail in `CHANGELOG.md`.
- CDN full-page cache can serve stale HTML briefly after a push; bypass with `?preview_theme_id=…`.

## Documentation Map
```
00_START_HERE ─▶ README ─▶ TABLE_OF_CONTENTS
INFORMATION_ARCHITECTURE ─┬─▶ SEO_GEO_MASTER_PLAN ─▶ SCHEMA_MASTER
                          └─▶ MERCHANDISING_GUIDE
DESIGN_SYSTEM ─▶ COMPONENT_LIBRARY ─▶ ANIMATION_GUIDELINES
BRAND_VOICE ─▶ COPY_GUIDELINES ─▶ HOMEPAGE_CONTENT_STRATEGY
CONTENT_SYSTEM ─▶ HOMEPAGE_SPECIFICATION ─▶ (references all standards)
QA_CHECKLIST + CHANGELOG ─▶ every phase
SHOPIFY_ARCHITECTURE + PERFORMANCE_BASELINE ─▶ current-state inputs
```

_Start with the Reading Order above. Nothing is implemented on the live store beyond the pending Phase-A promotion._

- **REVIEW_STRATEGY.md** — read before touching any review, rating or star. Genuine data only.
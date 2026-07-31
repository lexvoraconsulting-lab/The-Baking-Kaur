# AI Development Workflow

Recommended workflow for this specific project, based on what's actually been proven working this
session (not a generic best-practices list) — VS Code → Claude Code → Shopify CLI → GitHub → Local
Preview → Production.

## The loop that's already working (this session's real practice)

```
1. VS Code           — browse/read code, view diffs
2. Claude Code       — plan, edit, verify (Read/Edit/Grep tools)
3. Shopify CLI       — deploy-safety cycle, proven this session:
                        a. `shopify theme pull --only <file>` to a scratch path
                        b. diff --strip-trailing-cr against `git show HEAD:<path>`
                           (confirms zero drift before editing — catches the case where
                           the live theme diverged from git independent of your change)
                        c. edit locally
                        d. `shopify theme push --allow-live --only <file>`
                        e. re-pull, diff again — confirm byte-for-byte live
4. GitHub            — commit only after step 3e confirms the push is real and correct
5. Local Preview     — NOT YET USED this session; see gap below
6. Production        — the live theme IS production here (Shopify Plus/Basic single-theme
                        setup, per `CLAUDE.md`) — there's no separate staging theme currently
```

## Real gap: no local preview step

`shopify theme dev` (a local dev server with live reload against the theme) has not been used this
session — every change went straight from local edit to live push, verified after the fact via
pull-diff rather than previewed before pushing. This works because:
- The storefront's password gate already means most pages can't be visually spot-checked anyway
  this session (see `seo-audit/`'s repeated notes on this).
- Every change made was narrow and mechanically verifiable (a specific string/attribute), not a
  visual layout change needing eyeball confirmation.

**This is a real limitation, not a strength** — for any future *visual* change (the kind
`CLAUDE.md`'s protected-module rule is most worried about), `shopify theme dev` should be used
first to preview locally before pushing to the live theme. Recommended addition to the loop:

```
3b. `shopify theme dev --store ae86ba-2a.myshopify.com` — opens a local preview URL with live
    reload, lets you visually confirm a change BEFORE it reaches the live theme, using
    `--only`/unpublished-theme semantics so it never touches the live theme until you explicitly
    push
```

## Recommended workflow going forward

1. **Code-only, mechanically-verifiable changes** (schema fixes, attribute fixes, text
   corrections): the existing pull→diff→edit→push→re-pull→diff cycle, exactly as used throughout
   this session. No local preview needed — the diff-based verification already proves correctness.
2. **Visual/layout changes** (anything touching the protected product-page module, or any CSS/
   markup restructuring): add `shopify theme dev` locally first, confirm visually, *then* enter the
   same pull→diff→push→re-pull cycle for the final deploy.
3. **Multi-file features**: branch in git first (this repo already uses feature branches —
   `feature/vision-engine-v1` is the current one), commit locally, and only push to the live theme
   once the whole feature is internally consistent — never push a half-finished multi-file change.
4. **Every commit** documents deploy-safety evidence in its message (drift check result, push
   confirmation) — already the established pattern in this repo's git history; keep it.

## Related

[SHOPIFY_DEV_SETUP.md](SHOPIFY_DEV_SETUP.md), [CLAUDE_CAPABILITIES.md](CLAUDE_CAPABILITIES.md).

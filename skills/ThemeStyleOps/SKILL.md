---
name: ThemeStyleOps
description: Select and apply reusable visual themes for repository documentation diagrams, SVG assets, README visuals, GitHub callouts, architecture/workflow graphics, MathJax/LaTeX presentation, and project-memory illustrations. Use when a user names a documentation visual theme, asks for macOS Tahoe/Liquid Glass styling, asks for Lexvora-branded diagram styling, or needs repeatable color, typography, material, callout, and prompt rules for documentation graphics.
license: see repository LICENSE
metadata:
  author: Lexvora Consulting
  version: "2.2.1"
  changelog: ./CHANGELOG.md
---

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="./assets/banners/lexvora/documentation-dark.svg">
  <img alt="ThemeStyleOps Banner" src="./assets/banners/lexvora/documentation-light.svg" width="100%">
</picture>

# ThemeStyleOps

> **Reusable documentation visual themes, tokens, and vector-asset rules**  
> **Version:** `2.2.1` · **Status:** ![Active](./assets/badges/lexvora/active.svg) · **Themes:** `lexvora-company` · `macos-tahoe-liquid-glass`  
> **Owning Plan:** [`Support/plans/01-skills/ThemeStyleOps/theme-style-ops-plan.md`](../../Support/plans/01-skills/ThemeStyleOps/theme-style-ops-plan.md) · **Group:** [`Support/plans/01-skills/skills-master.md`](../../Support/plans/01-skills/skills-master.md)

---

Use this skill to choose and enforce a reusable visual theme for documentation graphics. It does
not decide whether a diagram is needed; it defines how an approved diagram should look, which
palette/material rules apply, and how the result should be documented and verified.

## Theme selection

Pick exactly one theme profile for a documentation visual:

| S.No. | Theme | Read | Use when |
| ---: | --- | --- | --- |
| 1 | `lexvora-company` | [`references/lexvora-company.md`](references/lexvora-company.md) | The user wants Lexvora Consulting brand-derived diagrams using the company website's navy, brass/gold, cream, paper, charcoal, and slate palette. |
| 2 | `macos-tahoe-liquid-glass` | [`references/macos-tahoe-liquid-glass.md`](references/macos-tahoe-liquid-glass.md) | The user wants premium translucent, glass-like, modern documentation diagrams with soft spectral color and high readability. |

## Shortcut aliases

Users do not need to know internal theme IDs. Detect these short aliases:

| S.No. | User says | Use theme |
| ---: | --- | --- |
| 1 | `LXC theme` | `lexvora-company` |
| 2 | `Lexvora theme` | `lexvora-company` |
| 3 | `Lexvora company theme` | `lexvora-company` |
| 4 | `macOS theme` | `macos-tahoe-liquid-glass` |
| 5 | `Tahoe theme` | `macos-tahoe-liquid-glass` |
| 6 | `Liquid Glass theme` | `macos-tahoe-liquid-glass` |

## Operations

This skill has only two operations:

| S.No. | Operation | Meaning |
| ---: | --- | --- |
| 1 | Apply theme | Apply the selected theme to every relevant documentation visual surface in the target. |
| 2 | Audit theme | Inspect the target and report only required theme fixes unless the user asks to edit. |

Do not create separate theme modes for README work, Plan work, diagrams, GitHub callouts, or
MathJax/LaTeX. Those are surfaces where the selected theme applies automatically when present or
when the owning documentation workflow decides they are required.

## Resolving the active theme

A theme is a project-level constant — set once, consumed many times. Resolve it in this order
([`DEC_20260902_A`](../../Support/decisions/DEC_20260902_A_theme_aware_visual_generation_flow.md),
`CON004`):

| S.No. | Step | Result |
| ---: | --- | --- |
| 1 | An alias above appears in the request | that theme, **for this run only** — never persisted |
| 2 | The repository name contains `LXC` or `Lexvora` | `lexvora-company`, automatically |
| 3 | Otherwise | `macos-tahoe-liquid-glass` — the global default |

A recorded project default (a `projectops` repo's `rules.md` §13, or an equivalent single declared
line) takes the place of steps 2–3 when present.

**Called directly (no `projectops`):** stateless. The theme is passed at runtime on each call
("apply the Tahoe theme to …"); nothing is stored between calls; with no theme named, fall to
step 2 then step 3. To set one theme for a whole repository and have every workflow use it without
repeating it, use `projectops` — it records and manages the per-repo default and feeds it here.

Resolve before emitting a themed artifact. When nothing themed is produced, the call is a no-op.

## How this skill fits

This skill is normally called by a documentation or diagram workflow:

```text
projectops
  -> svgImageOpsLoop
    -> ThemeStyleOps
      -> image-to-vector-graphics when durable SVG/PDF craft is needed
```

Use [`references/diagram-color-system.md`](references/diagram-color-system.md) for shared semantic
color roles across themes. Use [`references/svg-composition-rules.md`](references/svg-composition-rules.md)
before creating or editing SVG diagrams. Use
[`references/latex-mathjax.md`](references/latex-mathjax.md) when documentation includes equations,
formula labels, GitHub math blocks, Obsidian MathJax, or math-heavy diagram annotations. Use
[`references/github-callouts.md`](references/github-callouts.md) when documentation uses GitHub
Markdown callouts such as NOTE, TIP, IMPORTANT, WARNING, or CAUTION. Read
[`references/github-rendering.md`](references/github-rendering.md) before applying color to
any Markdown that will be read on github.com, because GitHub strips inline styling and never
loads repository CSS. Use
[`references/banner-and-badge-system.md`](references/banner-and-badge-system.md) whenever a
governed documentation area needs its banner or a table column needs status colour; the assets are
generated for both theme profiles by
[`scripts/generate_theme_assets.py`](scripts/generate_theme_assets.py).

Use [`samples/visual-theme-sample.md`](samples/visual-theme-sample.md) as the rendered proof of
each GitHub color route, [`samples/theme-asset-gallery.md`](samples/theme-asset-gallery.md) to pick
a banner or chip from the full catalogue, [`samples/lexvora/`](samples/lexvora/) and
[`samples/tahoe/`](samples/tahoe/) to see a complete governed documentation set with the theme
applied, and
[`samples/lexvora-visual-theme.css`](samples/lexvora-visual-theme.css) for Obsidian CSS-snippet
styling.

## Paste-ready prompts

Copy any line and use it as-is. The Lexvora and Tahoe lines are identical except the theme word;
`<target>` is a file, a folder, or a single asset. Same sentence for every surface — there is no
per-surface command.

```text
Apply the Lexvora theme to <target>.
Apply the Tahoe theme to <target>.
Audit the Lexvora theme in <target>.      # report the fixes, change nothing
Audit the Tahoe theme in <target>.        # report the fixes, change nothing
```

`Lexvora` / `Tahoe` are interchangeable with any alias in *Shortcut aliases*; the trailing word
`theme` is optional. Omit the theme word entirely to take the resolved default (see *Resolving the
active theme*):

```text
Apply the theme to <target>.
```

Use a structured prompt only when the target is ambiguous:

```text
Use the `ThemeStyleOps` skill.
Theme: `<LXC theme | Lexvora theme | macOS theme | Tahoe theme | Liquid Glass theme | (omit for default)>`
Operation: `<apply theme | audit theme>`
Target: `<file, folder, or asset>`
```

## Required output rules

- Keep diagrams editable SVG unless the user explicitly requests a raster-only asset.
- Never copy Apple artwork, Apple UI, Apple icons, screenshots, or proprietary brand assets into generated diagrams.
- Use external brand colors only as reference/provenance; derive documentation-safe tokens when needed for contrast and readability.
- Keep labels short enough to render at README width without clipping.
- Use explicit arrowhead geometry or verified markers; arrow direction must match the prose.
- Keep LaTeX/MathJax expressions theme-aware: equation ink, caption size, rule weight, and callout
  colors must match the selected visual profile.
- Use GitHub callouts only for information that needs visual priority; their severity and tone
  must match NOTE, TIP, IMPORTANT, WARNING, or CAUTION exactly.
- Never carry color on GitHub-facing Markdown with `style`, `bgcolor`, `color`, or `<font>`; those
  are stripped. Use a committed SVG, a themed Mermaid block, a badge chip, a callout, or a
  syntax-highlighted fence.
- Give every large GitHub visual a light/dark pair switched with `<picture>`, and keep color
  decorative: the label must still carry the meaning without it.
- Give every governed documentation area its banner, placed above the `H1`, using the generated
  asset for the selected theme rather than a hand-drawn one-off.
- Take status, risk, priority, estimate, and record-type chips from the generated badge set. Do not
  hand-write a chip or invent a status that the owning skill's ladder does not define.
- Never hand-edit anything under `assets/badges/` or `assets/banners/`; change
  `scripts/generate_theme_assets.py` and re-run it so both theme profiles stay in step.
- **Attribution mark** — every hand-authored `lexvora-company` SVG carries a small `Lexvora (LXC)`
  mark in the **bottom-right corner**, on its own layer, so a saved or forwarded file keeps its
  provenance (`DEC_20260902_B` / `CON005`). Exact markup, from the SVG's `viewBox` `W`×`H`:
  ```xml
  <!-- lxc-attribution -->
  <g class="lxc-attribution">
    <rect x="{W-108}" y="{H-22}" width="96" height="15" rx="4" fill="#ffffff" fill-opacity="0.08"/>
    <text x="{W-12}" y="{H-10}" text-anchor="end"
          font-family="ui-monospace, SFMono-Regular, Menlo, monospace"
          font-size="9" fill="#8a5723" fill-opacity="0.5">Lexvora (LXC)</text>
  </g>
  ```
  50% glass (`fill-opacity: 0.5`) over a faint chip. It sits in the outer margin only — never over
  a card, node, or the diagram body — and is deletable as one layer. `macos-tahoe-liquid-glass`
  uses the same placement with that profile's frosted tokens.
- Record the theme profile used in the owning asset register, README, worklog, or evidence record.
- Verify SVG XML, Markdown links, and visual render preview before closing the task.

## Theme extension rule

Add a new theme as a focused reference file under `references/<theme>.md`, then add it to the
Theme selection table. Do not bury a new theme in another skill's README or a one-off diagram.

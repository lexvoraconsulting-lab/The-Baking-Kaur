---
cssclasses:
  - lexvora-visual-theme-sample
---

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../assets/banners/lexvora/documentation-dark.svg">
  <img alt="Documentation Visual Theme - Lexvora Company profile" src="../assets/banners/lexvora/documentation-light.svg" width="100%">
</picture>

# Documentation Visual Theme Samples

Live rendering trials for the `ThemeStyleOps` skill. **GitHub is the primary target.**
Every technique on this page is shown as it actually renders on github.com, in both light and dark
appearance.

## Navigation

Parent: [`README.md`](../README.md) · Contract: [`SKILL.md`](../SKILL.md) · Rules:
[`github-rendering.md`](../references/github-rendering.md) · Theme:
[`lexvora-company.md`](../references/lexvora-company.md)

## Table of Contents

- [Navigation](#navigation)
- [Markdown Styling Possibilities](#markdown-styling-possibilities)
- [Colour That Works: Badge Chips in a Plain Table](#colour-that-works-badge-chips-in-a-plain-table)
- [Colour That Works: Themed Mermaid](#colour-that-works-themed-mermaid)
- [Theme Asset Gallery](./theme-asset-gallery.md)
- [Colour That Works: Committed SVG](#colour-that-works-committed-svg)
- [Colour That Works: GitHub Callouts](#colour-that-works-github-callouts)
- [Colour That Works: Diff Fences](#colour-that-works-diff-fences)
- [What GitHub Strips](#what-github-strips)
- [Obsidian CSS Snippet](#obsidian-css-snippet)
- [Obsidian Markdown Preview](#obsidian-markdown-preview)
- [Footer Navigation](#footer-navigation)

These trials use Lexvora Company palette values: navy `#061421`, blue `#102d40`, brass `#b88445`,
brass highlight `#d2a15f`, cream `#fbf8f3`, ink `#101820`, and muted text `#5c6670`.

## Markdown Styling Possibilities

| S.No. | Markdown target | What is really possible | Best use |
| ---: | --- | --- | --- |
| 1 | Pure Markdown | Tables, bold, italic, code, links, headings, lists, and GitHub callouts; no colours and no pixel font sizes. | Portable source that must work everywhere. |
| 2 | GitHub Markdown | Pure Markdown plus images, `<picture>`, `<details>`, Mermaid, and callouts. `style`, `bgcolor`, `color`, and `<font>` are **stripped**; only `align` and `width` survive. Repository CSS is never loaded. | Anything a visitor reads on github.com. |
| 3 | Obsidian Markdown | Plain Markdown plus vault CSS snippets selected by frontmatter `cssclasses`. | Reusable theme styling inside a vault only. |
| 4 | Shared GitHub and Obsidian file | Keep the canonical table in plain Markdown and carry colour in committed images. | Documentation that must stay readable in both tools. |
| 5 | Pixel font sizes | Not available in pure Markdown and not available on GitHub. Use a committed SVG when exact type size matters; use CSS snippets in Obsidian. | Visual calibration, not normal governed documentation. |

## Colour That Works: Badge Chips in a Plain Table

This is the route to take when a table column needs colour. The table itself stays plain Markdown,
so it remains selectable, diffable, and readable with images turned off. The chips are committed
SVGs in [`../assets/badges/`](../assets/badges/); the full set is in the
[theme asset gallery](./theme-asset-gallery.md).

| S.No. | Original concern | Repository had | Status | Fix feedback |
| ---: | --- | --- | --- | --- |
| 1 | `<folder>-master.md` per area | `README.md` per area | ![Resolved](../assets/badges/lexvora/gap-resolved.svg) | Deviation register now uses the accepted root entry file. |
| 2 | Numbered plan folders | Named plan folders | ![Resolved](../assets/badges/lexvora/gap-resolved.svg) | Named folders are accepted when recorded in the register. |
| 3 | Theme tokens undocumented | Ad-hoc diagram colours | ![In Delivery](../assets/badges/lexvora/in-delivery.svg) | Semantic roles now map through the colour system. |
| 4 | Inline HTML theming | `bgcolor` tables | ![Blocked](../assets/badges/lexvora/gap-blocked.svg) | Not achievable on GitHub; superseded by this page. |

The full chip set is 46 chips per theme, covering the Plan status ladder, the record status
ladder, architecture states, gap states, risk/priority/estimate, and record types. See the
[theme asset gallery](./theme-asset-gallery.md) for every one rendered in both themes.

| S.No. | Chip | Semantic role | Use on |
| ---: | --- | --- | --- |
| 1 | ![Verified](../assets/badges/lexvora/plan-verified.svg) | `success` | A Plan proven against real evidence. |
| 2 | ![Open Question](../assets/badges/lexvora/open-question.svg) | `decision` | A concept awaiting an owner answer. |
| 3 | ![Risk High](../assets/badges/lexvora/risk-high.svg) | `risk` | A row carrying material exposure. |
| 4 | ![P1](../assets/badges/lexvora/priority-p1.svg) | `risk` | Top-priority work. |
| 5 | ![Est L](../assets/badges/lexvora/estimate-l.svg) | `system` | Sizing on a task or Plan. |
| 6 | ![Plan](../assets/badges/lexvora/type-plan.svg) | `governing` | A record-type chip in a navigation table. |

## Colour That Works: Themed Mermaid

GitHub renders Mermaid natively. An `init` directive plus `classDef` rules bind the diagram to the
Lexvora palette, and the source stays text-editable and diffable.

```mermaid
%%{init: {'theme':'base','themeVariables':{'background':'#fbf8f3','primaryColor':'#ffffff','primaryTextColor':'#101820','primaryBorderColor':'#b88445','lineColor':'#102d40','fontSize':'14px'}}}%%
flowchart LR
  PDM[projectops]:::governing
  LOOP[svgImageOpsLoop]:::system
  THEME[ThemeStyleOps]:::decision
  SVG[image-to-vector-graphics]:::doc

  PDM --> LOOP --> THEME --> SVG

  classDef governing fill:#061421,stroke:#b88445,stroke-width:2px,color:#ffffff
  classDef system fill:#102d40,stroke:#b88445,stroke-width:2px,color:#ffffff
  classDef decision fill:#b88445,stroke:#8a5723,stroke-width:2px,color:#061421
  classDef doc fill:#ffffff,stroke:#b88445,stroke-width:2px,color:#101820
```

## Colour That Works: Committed SVG

The banner at the top of this page is a committed SVG pair switched by `<picture>`. This is the
only route with total control over colour, type size, spacing, and layout.

| S.No. | Asset | Appearance |
| ---: | --- | --- |
| 1 | [`documentation-light.svg`](../assets/banners/lexvora/documentation-light.svg) | Cream page, navy heading, brass rule. |
| 2 | [`documentation-dark.svg`](../assets/banners/lexvora/documentation-dark.svg) | Navy page, cream heading, brass rule. |

```markdown
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../assets/banners/lexvora/documentation-dark.svg">
  <img alt="Documentation Visual Theme" src="../assets/banners/lexvora/documentation-light.svg" width="100%">
</picture>
```

## Colour That Works: GitHub Callouts

GitHub owns these five colours and renders them correctly in both appearances.

> [!NOTE]
> The Lexvora profile derives documentation-safe tokens from the company website CSS.

> [!TIP]
> Keep the canonical table in plain Markdown and let committed images carry the colour.

> [!IMPORTANT]
> Repository CSS is never loaded by GitHub. Styling must travel inside an image or a Mermaid block.

> [!WARNING]
> An HTML table using `bgcolor` renders unstyled on GitHub. Do not ship it as a fallback.

> [!CAUTION]
> Colour must never be the only carrier of meaning. Keep the label readable without it.

## Colour That Works: Diff Fences

A `diff` fence gives grammar-driven green and red without any HTML.

```diff
+ Committed SVG, Mermaid, callouts, and badge chips render in colour on GitHub.
- Inline style, bgcolor, and font colour are stripped before the page is served.
```

## What GitHub Strips

Kept as evidence so the finding is not re-litigated. On github.com the table below renders with no
navy header, no cream rows, and no brass accent — every colour attribute is discarded.

<table>
  <tr bgcolor="#061421" style="background:#061421;">
    <th style="color:#ffffff;"><font color="#ffffff"><b>Attempted styling</b></font></th>
    <th style="color:#d2a15f;"><font color="#d2a15f"><b>Result on GitHub</b></font></th>
  </tr>
  <tr bgcolor="#fbf8f3" style="background:#fbf8f3;">
    <td><font size="2" color="#5c6670">Row background via <code>bgcolor</code></font></td>
    <td><font size="2" color="#102d40"><b>Discarded</b></font></td>
  </tr>
  <tr bgcolor="#ffffff" style="background:#ffffff;">
    <td><font size="2" color="#5c6670">Text colour via <code>&lt;font&gt;</code></font></td>
    <td><font size="2" color="#102d40"><b>Discarded</b></font></td>
  </tr>
</table>

## Obsidian CSS Snippet

Obsidian is a secondary surface. Its styling comes from a vault CSS snippet, and none of it applies
on GitHub. Use [`lexvora-visual-theme.css`](./lexvora-visual-theme.css) as the snippet source: copy
it to `<vault>/.obsidian/snippets/lexvora-visual-theme.css`, enable it under Settings → Appearance →
CSS snippets, and keep this file's `cssclasses` frontmatter.

The selectors are anchored on `.markdown-preview-view` and `.markdown-source-view.mod-cm6`, which
are Obsidian DOM classes. They have no effect on GitHub or in an editor preview.

## Obsidian Markdown Preview

Plain Markdown that the snippet styles inside a vault, and that GitHub renders as an ordinary table.

| S.No. | Surface | Obsidian | GitHub |
| ---: | --- | --- | --- |
| 1 | Table colour | Snippet-driven | Badge chips only |
| 2 | Pixel font size | Snippet-driven | Committed SVG only |
| 3 | Callouts | Partial | Native |
| 4 | Mermaid | Native | Native |

## Footer Navigation

Parent: [`README.md`](../README.md) · Contract: [`SKILL.md`](../SKILL.md) · Rules:
[`github-rendering.md`](../references/github-rendering.md)

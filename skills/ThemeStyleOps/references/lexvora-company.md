# Lexvora Company Theme

Use this profile for Lexvora-owned documentation, repository README diagrams, project-memory
graphics, and architecture/workflow visuals that should feel connected to the company website.

## Source Color Evidence

Derived from the sibling `LXC-Company-Website` CSS, especially:

| S.No. | Website token/source | Value |
| ---: | --- | --- |
| 1 | `--dark` | `#061421` |
| 2 | `--dark-2` | `#0b2233` |
| 3 | `--blue` | `#102d40` |
| 4 | `--gold` | `#b88445` |
| 5 | `--gold-light` | `#d2a15f` |
| 6 | `--cream` | `#f7f3ed` |
| 7 | `--paper` | `#ffffff` |
| 8 | `--text` | `#101820` |
| 9 | `--muted` | `#5c6670` |
| 10 | `--border` | `rgba(184,132,69,.28)` |

Treat these as provenance tokens. For diagrams, use the documentation tokens below because they
balance brand feel with Markdown readability.

## Documentation Tokens

| S.No. | Role | Token | Hex/RGBA |
| ---: | --- | --- | --- |
| 1 | Page background | `--doc-bg` | `#fbf8f3` |
| 2 | Paper panel | `--doc-paper` | `#ffffff` |
| 3 | Primary ink | `--doc-ink` | `#101820` |
| 4 | Secondary text | `--doc-muted` | `#5c6670` |
| 5 | Deep surface | `--doc-navy` | `#061421` |
| 6 | Structural blue | `--doc-blue` | `#102d40` |
| 7 | Brass accent | `--doc-brass` | `#b88445` |
| 8 | Brass highlight | `--doc-brass-light` | `#d2a15f` |
| 9 | Warm border | `--doc-border` | `rgba(184,132,69,.28)` |
| 10 | Soft shadow | `--doc-shadow` | `rgba(16,24,32,.12)` |

## Diagram Style

- Use warm paper backgrounds with navy headings and brass accent rules.
- Use navy blocks for source-of-truth or governing layers.
- Use brass for decisions, checkpoints, highlights, and active path markers.
- Use structural blue for architecture, routing, dependency, or platform nodes.
- Use cream fills for secondary containers; avoid large flat gold backgrounds.
- Keep body text charcoal, not navy, for readability on light panels.
- Prefer 8-18 px corner radius depending on scale; avoid pill-heavy layouts.
- Use subtle shadows and one brass highlight line to suggest depth.

## SVG Starter Tokens

```css
.theme-lexvora {
  --doc-bg: #fbf8f3;
  --doc-paper: #ffffff;
  --doc-ink: #101820;
  --doc-muted: #5c6670;
  --doc-navy: #061421;
  --doc-blue: #102d40;
  --doc-brass: #b88445;
  --doc-brass-light: #d2a15f;
  --doc-border: rgba(184,132,69,.28);
  --doc-shadow: rgba(16,24,32,.12);
}
```

## Prompt Add-On

```markdown
Theme profile: `lexvora-company`.
Use warm paper, deep navy structure, restrained brass highlights, and charcoal text. Preserve
high contrast and cite the LXC Company Website CSS as color provenance when recording the asset.
```

## Attribution Mark

Every hand-authored `lexvora-company` SVG carries a small `Lexvora (LXC)` mark in the **bottom-right
corner** ([`DEC_20260902_B`](../../../Support/decisions/DEC_20260902_B_lexvora_attribution_mark.md) /
`CON005`). Provenance, not decoration. Exact markup, from the SVG viewBox `W`x`H`:

```xml
<!-- lxc-attribution -->
<g class="lxc-attribution">
  <rect x="{W-108}" y="{H-22}" width="96" height="15" rx="4" fill="#ffffff" fill-opacity="0.08"/>
  <text x="{W-12}" y="{H-10}" text-anchor="end"
        font-family="ui-monospace, SFMono-Regular, Menlo, monospace"
        font-size="9" fill="#8a5723" fill-opacity="0.5">Lexvora (LXC)</text>
</g>
```

- 50% glass (`fill-opacity: 0.5`) over a faint `#ffffff` chip.
- Outer margin only — never over a card, node, or the diagram body.
- Its own layer — deletable in one move without touching content.
- `pdmcheck diagrams` must stay clean with the mark present.

# GitHub Callouts

Use GitHub callouts when Markdown documentation needs native visual priority without custom HTML or
CSS. These callouts also render well in many Obsidian workflows, but GitHub is the primary target.

## Supported Elements

```markdown
> [!NOTE]
> Useful information users should know.

> [!TIP]
> Helpful advice for doing things easier.

> [!IMPORTANT]
> Crucial information necessary for users to succeed.

> [!WARNING]
> Critical content demanding immediate user attention.

> [!CAUTION]
> Negative consequences of an action.
```

## Usage Contract

| S.No. | Callout | Use for | Do not use for |
| ---: | --- | --- | --- |
| 1 | `NOTE` | Context, scope, assumptions, provenance, version limits, or stable background facts. | Steps the user must follow to succeed. |
| 2 | `TIP` | Optional shortcuts, easier workflows, quality improvements, or productivity advice. | Required setup or warnings. |
| 3 | `IMPORTANT` | Required constraints, prerequisites, source-of-truth rules, or success conditions. | General emphasis. |
| 4 | `WARNING` | Risky actions, irreversible operations, likely failure modes, or time-sensitive hazards. | Mild caveats or normal TODOs. |
| 5 | `CAUTION` | Negative consequences, destructive outcomes, data loss, security exposure, or policy violations. | Ordinary warnings that have no concrete consequence. |

Use no more than one callout per short section unless the document is explicitly a safety or
operations guide. Too many callouts make all of them weaker.

## Theme Mapping

GitHub controls the final callout styling, so theme rules affect nearby diagrams, captions, and
parallel SVG callout treatments rather than GitHub's native CSS.

| S.No. | Callout | Lexvora Company accent | macOS Tahoe Liquid Glass accent |
| ---: | --- | --- | --- |
| 1 | `NOTE` | `#102d40` structural blue | `#2f7dff` blue |
| 2 | `TIP` | `#0f6b4f` deep green | `#00a676` teal |
| 3 | `IMPORTANT` | `#7a3f9d` restrained violet | `#7a3cff` violet |
| 4 | `WARNING` | `#b88445` brass/gold | `#ff7a1a` amber |
| 5 | `CAUTION` | `#9d2f2f` deep red | `#ff3b4f` red |

## Typography and Spacing

- Put a blank line before and after every callout block.
- Keep the first sentence short and direct.
- Use one paragraph inside a callout unless a list is necessary.
- If a callout includes a list, keep list items short and parallel.
- Do not put large tables inside callouts; introduce the table with the callout, then keep the
  table outside.
- Keep code blocks outside callouts unless the code is the warning or tip itself.

## Pattern Library

### NOTE

```markdown
> [!NOTE]
> This diagram uses the `lexvora-company` theme profile derived from the LXC Company Website CSS.
```

### TIP

```markdown
> [!TIP]
> Use the copy-paste theme prompt before asking an agent to regenerate a diagram.
```

### IMPORTANT

```markdown
> [!IMPORTANT]
> Record the selected theme profile in the asset register before closing the documentation batch.
```

### WARNING

```markdown
> [!WARNING]
> Re-render SVGs after editing arrow markers; marker direction errors are easy to miss in XML.
```

### CAUTION

```markdown
> [!CAUTION]
> Do not paste proprietary product screenshots into reusable theme assets.
```

## SVG Equivalent

When recreating a GitHub callout inside an SVG, use the same label and severity mapping:

| S.No. | SVG property | Rule |
| ---: | --- | --- |
| 1 | Label | Use uppercase `NOTE`, `TIP`, `IMPORTANT`, `WARNING`, or `CAUTION`. |
| 2 | Border | Use the selected theme accent for that callout type. |
| 3 | Fill | Use a pale tint, not a saturated fill. |
| 4 | Text | Use the theme primary ink; never rely on color alone. |
| 5 | Icon | Optional; if used, keep it simple and do not copy platform icons. |

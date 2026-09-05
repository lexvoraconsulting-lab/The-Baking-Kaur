# LaTeX/MathJax Theme Rules

Use these rules when Markdown documentation includes LaTeX, MathJax, equations, formula callouts,
or math labels inside SVG diagrams. The target renderers are GitHub Markdown and Obsidian MathJax.

## Renderer Rules

- Use standard Markdown math delimiters: inline `$...$` and block `$$...$$`.
- Avoid custom TeX macros unless they are defined in the same document and tested in Obsidian.
- Do not rely on CSS styling inside GitHub-rendered math; GitHub sanitizes and controls math output.
- Put theme styling around math blocks with Markdown headings, captions, callout tables, or SVG
  labels rather than trying to recolor the TeX itself.
- For SVG diagrams, render math as normal text labels when the expression is short. Use external
  MathJax-rendered assets only when exact typesetting is required and provenance is recorded.

## Type Scale

| S.No. | Use | Markdown/GitHub | SVG diagram |
| ---: | --- | --- | --- |
| 1 | Inline formula | Natural paragraph size | 15-17 px |
| 2 | Block equation | Natural MathJax block | 18-22 px equivalent visual size |
| 3 | Equation caption | 13-14 px, muted text | 13-14 px |
| 4 | Axis/formula label | Not applicable | 13-16 px |
| 5 | Main diagram label with formula | Heading text plus separate formula line | 18-22 px label, 14-16 px formula |

Keep formula labels shorter than prose labels. If an expression is long, put it below the diagram
or in a numbered equation block and reference it from the SVG.

## Theme Mapping

| S.No. | Role | Lexvora Company | macOS Tahoe Liquid Glass |
| ---: | --- | --- | --- |
| 1 | Equation ink | `#101820` | `#111827` |
| 2 | Formula caption | `#5c6670` | `#475569` |
| 3 | Equation rule/divider | `rgba(184,132,69,.38)` | `rgba(51,65,85,.24)` |
| 4 | Important variable accent | `#b88445` in surrounding label/caption | `#2f7dff` in surrounding label/caption |
| 5 | Validation/proof accent | `#102d40` or `#d2a15f` | `#00a676` |
| 6 | Warning/invalid formula accent | `#8a5723` on warm fill | `#ff3b4f` |

## Markdown Pattern

```markdown
### Throughput Bound

$$
R_{max} = \min(C_{api}, C_{db}, C_{queue})
$$

| S.No. | Symbol | Meaning |
| ---: | --- | --- |
| 1 | `$C_{api}$` | API capacity ceiling. |
| 2 | `$C_{db}$` | Database capacity ceiling. |
| 3 | `$C_{queue}$` | Queue processing ceiling. |
```

## SVG Label Pattern

Use plain readable SVG text for short expressions:

```xml
<text class="formula" x="600" y="420" text-anchor="middle">Rmax = min(Capi, Cdb, Cqueue)</text>
```

Use this style baseline:

```css
.formula {
  fill: #101820;
  font: 560 15px system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;
}
.formula-caption {
  fill: #5c6670;
  font: 520 13px system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;
}
```

Switch the `fill` values to the selected theme mapping above.

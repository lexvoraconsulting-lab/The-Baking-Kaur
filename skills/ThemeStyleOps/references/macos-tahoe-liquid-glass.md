# macOS Tahoe Liquid Glass Theme

Use this profile when the user asks for macOS Tahoe, macOS 26, Liquid Glass, translucent glass,
or a premium modern documentation diagram with soft spectral color.

This is an original documentation theme inspired by contemporary translucent UI materials. Do not
copy Apple interface artwork, icons, screenshots, proprietary shapes, or marketing imagery.

## Documentation Tokens

| S.No. | Role | Token | Hex/RGBA |
| ---: | --- | --- | --- |
| 1 | Page base | `--glass-bg` | `#f7fbff` |
| 2 | Cool wash | `--glass-cyan` | `#d8f7ff` |
| 3 | Blue wash | `--glass-blue` | `#dbeafe` |
| 4 | Violet wash | `--glass-violet` | `#ede9fe` |
| 5 | Pink wash | `--glass-pink` | `#fae8ff` |
| 6 | Warm wash | `--glass-warm` | `#fff2e8` |
| 7 | Ink | `--glass-ink` | `#111827` |
| 8 | Secondary text | `--glass-muted` | `#475569` |
| 9 | Blue accent | `--glass-accent-blue` | `#2f7dff` |
| 10 | Teal accent | `--glass-accent-teal` | `#00a676` |
| 11 | Violet accent | `--glass-accent-violet` | `#7a3cff` |
| 12 | Amber accent | `--glass-accent-amber` | `#ff7a1a` |
| 13 | Critical accent | `--glass-accent-red` | `#ff3b4f` |
| 14 | Panel fill | `--glass-panel` | `rgba(255,255,255,.68)` |
| 15 | Panel stroke | `--glass-stroke` | `rgba(255,255,255,.78)` |
| 16 | Connector ink | `--glass-line` | `#334155` |

## Material Rules

- Build the background from two or three broad gradients, not many decorative blobs.
- Use translucent panels with a white stroke, soft shadow, and a small highlight band.
- Keep text fully opaque and high contrast; never make labels translucent.
- Keep tinted outlines distinct: blue, teal, violet, amber, or red by semantic role.
- Use glass effects to frame information, not to reduce legibility.
- Use a dark hub panel only when it clarifies hierarchy.

## SVG Starter Tokens

```css
.theme-macos-tahoe-liquid-glass {
  --glass-bg: #f7fbff;
  --glass-cyan: #d8f7ff;
  --glass-blue: #dbeafe;
  --glass-violet: #ede9fe;
  --glass-pink: #fae8ff;
  --glass-warm: #fff2e8;
  --glass-ink: #111827;
  --glass-muted: #475569;
  --glass-accent-blue: #2f7dff;
  --glass-accent-teal: #00a676;
  --glass-accent-violet: #7a3cff;
  --glass-accent-amber: #ff7a1a;
  --glass-accent-red: #ff3b4f;
  --glass-panel: rgba(255,255,255,.68);
  --glass-stroke: rgba(255,255,255,.78);
  --glass-line: #334155;
}
```

## Prompt Add-On

```markdown
Theme profile: `macos-tahoe-liquid-glass`.
Use translucent glass panels, broad spectral washes, crisp dark text, verified arrowheads,
subtle shadows, and readable Markdown-width layout. Do not copy Apple artwork or UI.
```

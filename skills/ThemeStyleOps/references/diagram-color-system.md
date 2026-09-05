# Diagram Color System

Use semantic roles first, then map them through the selected theme.

| S.No. | Semantic role | Lexvora Company | macOS Tahoe Liquid Glass |
| ---: | --- | --- | --- |
| 1 | Background | `#fbf8f3` | `#f7fbff` with broad cyan/violet/warm washes |
| 2 | Primary text | `#101820` | `#111827` |
| 3 | Secondary text | `#5c6670` | `#475569` |
| 4 | Governing/root node | `#061421` | dark glass gradient from `#172554` to `#0f172a` |
| 5 | Architecture/system node | `#102d40` | `#2f7dff` outline with pale blue glass fill |
| 6 | Decision/checkpoint node | `#b88445` | `#ff7a1a` outline with warm glass fill |
| 7 | Documentation/reconciliation node | `#d2a15f` highlight | `#00a676` or `#7a3cff` outline |
| 8 | Risk/error node | `#8a5723` on warm fill | `#ff3b4f` outline with pale red fill |
| 9 | Connector | `#102d40` at 70-85% opacity | `#334155` |
| 10 | Divider/border | `rgba(184,132,69,.28)` | `rgba(255,255,255,.78)` |
| 11 | GitHub NOTE | `#102d40` | `#2f7dff` |
| 12 | GitHub TIP | `#0f6b4f` | `#00a676` |
| 13 | GitHub IMPORTANT | `#7a3f9d` | `#7a3cff` |
| 14 | GitHub WARNING | `#b88445` | `#ff7a1a` |
| 15 | GitHub CAUTION | `#9d2f2f` | `#ff3b4f` |

## Rules

- Do not assign colors randomly. Every accent must map to a semantic role.
- Use one primary accent and at most two secondary accents in a single diagram.
- Use red only for actual risk, blocked state, destructive flow, or critical failure.
- Use green/teal for reconciliation, completed state, validation, or healthy loop.
- For numbered flows, keep sequence numbers muted and labels high contrast.
- Match GitHub callout labels to their intended severity; do not use WARNING or CAUTION for routine notes.
- Check contrast by inspection after rendering; pale tinted fills still need dark text.

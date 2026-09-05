# Banner and Badge System

Reusable, generated visual assets that give governed documentation an immediate identity on GitHub.
A reader landing on any documentation file should know within one second which area they are in and
what state each row is in, without reading a word of prose.

Every asset exists in both theme profiles: `lexvora-company` and `macos-tahoe-liquid-glass`.

## Generated, Never Hand-Edited

All banners, badges, and the gallery come from one script:

```bash
python3 skills/ThemeStyleOps/scripts/generate_theme_assets.py
```

| S.No. | Output | Path |
| ---: | --- | --- |
| 1 | Status and type chips | `assets/badges/<theme>/<slug>.svg` |
| 2 | Area banners, light and dark | `assets/banners/<theme>/<area>-<mode>.svg` |
| 3 | Rendered catalogue | `samples/theme-asset-gallery.md` |

Never hand-edit a file under `assets/`. Change `BADGES`, `BANNERS`, or the theme tables in the
script and re-run it, so the two profiles can never drift apart.

## Banners

One banner per governed documentation area, matching the structure contract in
[`../../projectops/references/support-structure.md`](../../projectops/references/support-structure.md).

| S.No. | Area | Banner slug |
| ---: | --- | --- |
| 1 | `support/support-master.md` | `support` |
| 2 | `support/rules.md` | `rules` |
| 3 | `support/context/` | `context` |
| 4 | `support/documentation/` | `documentation` |
| 5 | `support/research/` | `research` |
| 6 | `support/concept-design/` | `concept-design` |
| 7 | `support/architecture/` | `architecture` |
| 8 | `support/decisions/` | `decisions` |
| 9 | `support/plans/` | `plans` |
| 10 | `support/changelog.md` | `changelog` |
| 11 | `support/gaps-issues/` | `gaps-issues` |
| 12 | `support/worklog/` | `worklog` |
| 13 | Verification records | `verification` |
| 14 | Release records | `release` |

Place the banner as the first element of the file, above the `H1`, and always as a `<picture>` pair
so it inverts with the reader's GitHub appearance:

```markdown
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="<path>/assets/banners/lexvora/plans-dark.svg">
  <img alt="Plans" src="<path>/assets/banners/lexvora/plans-light.svg" width="100%">
</picture>
```

Keep the `alt` equal to the area name. The banner is orientation, not content: a reader with images
disabled must lose nothing but decoration.

Use the generic area banner unless the owner asks for a bespoke one. A new area means a new entry in
`BANNERS` and a re-run, not a hand-drawn one-off.

## Badges

Chips are self-contained — own fill, own border, own icon, own label — so one file reads correctly
in both light and dark appearance. They are the supported way to put colour in a table column while
the table itself stays plain Markdown.

| S.No. | Family | Covers |
| ---: | --- | --- |
| 1 | Plan status ladder | `NOT STARTED` through `VERIFIED` |
| 2 | Record status ladder | `Draft`, `Open Question`, `Active`, `Proposed`, `Confirmed`, `Planned`, `In Delivery`, `Resolved by Addition`, `Rejected`, `Superseded`, `Deprecated`, `On Hold`, `Future / Held` |
| 3 | Architecture states | `Current`, `Target`, `TBD` |
| 4 | Gap register states | `Open`, `Resolved`, `Blocked` |
| 5 | Risk, priority, estimate | `Risk Low/Medium/High`, `P1`-`P3`, `Est S`-`Est XL` |
| 6 | Record types | `Plan`, `Concept`, `Research`, `Decision`, `Rule`, `Architecture`, `Worklog`, `Gap`, `Verification` |

Each chip maps to a semantic role from [`diagram-color-system.md`](./diagram-color-system.md).
Colour is never chosen per chip; it is inherited from the role, which is why both themes stay
coherent.

```markdown
| 1 | G-01 | ![Open](<path>/assets/badges/lexvora/gap-open.svg) | ![Risk High](<path>/assets/badges/lexvora/risk-high.svg) | Register lacks a deviation entry. |
```

## Rules

- Use exactly one banner per file, at the top, before the `H1`.
- Use one theme profile per repository. Do not mix Lexvora and Tahoe assets in one document set.
- Keep chip `alt` text equal to the chip label. Colour and icon are reinforcement, never the only
  carrier of meaning.
- Do not invent a status. If a state is missing, add it to the ladder in the owning skill first,
  then add the chip.
- Do not resize a chip with `width`. Chips are drawn at their natural size and must stay consistent
  down a column.
- Keep image paths relative and case-exact; GitHub is case-sensitive.
- Re-run the generator after any theme token change, and commit the regenerated assets in the same
  commit as the token change.

## Verification

- Parse every changed SVG as XML.
- Render at least one banner and one chip sheet, and look at them.
- View the owning Markdown on github.com in both light and dark appearance.
- Confirm no chip label is truncated and no banner text is clipped at README width.

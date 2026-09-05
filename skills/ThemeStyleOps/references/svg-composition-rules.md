# SVG Composition Rules

Use these rules for documentation visuals made or themed by this skill.

## Canvas

- Prefer `1200x900`, `1200x1000`, or `1200x1200` viewBoxes for README diagrams.
- Keep at least 48 px outer padding on desktop-oriented SVGs.
- Keep text inside boxes with clear breathing room; do not rely on browser clipping.
- Use `system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif`.
- Avoid negative letter spacing and viewport-scaled font sizes.

## Connectors and Arrowheads

- Prefer direct vertical or orthogonal paths for process diagrams.
- Keep the arrowhead at the actual destination end.
- With SVG markers, set `refX` close to the visible tip and test render direction.
- If marker rendering is unreliable, draw arrowheads as explicit polygons.
- Leave at least 12 px between an arrowhead and the next box border unless the arrow is intended to touch.
- Re-render after every arrow change; arrowhead errors are easy to miss in raw XML.

## Accessibility

- Include `<title>` and `<desc>` in standalone SVGs.
- Keep reading order close to visual order in the XML.
- Use visible labels, not color alone, for state or category.
- Avoid text smaller than 13 px in README-scale graphics.

## Verification

Before closing:

1. Parse the SVG as XML.
2. Render a PNG preview.
3. Inspect the preview for blank output, clipped labels, wrong arrowheads, and overlap.
4. Confirm the Markdown embed path resolves with exact case.
5. Record the theme profile and evidence in the owning Worklog or asset README.

# Offline Markdown Viewer Compatibility Guide (G_34)

## Purpose

Provide deterministic compatibility patterns for rendering `<picture>` themed badges, banners, and SVGs across local offline Markdown editors (Obsidian, VS Code Markdown Preview Enhanced, Marked 2, Typora) and GitHub mobile/desktop viewers.

## Common Offline Viewer Behavior

| Viewer | `<picture>` / SVG Support | Recommended Compatibility Mode |
| --- | --- | --- |
| **GitHub Web (Light/Dark)** | Full native `<picture>` media query support | Default `<picture>` with `srcset` |
| **Obsidian** | Renders fallback `<img>` within `<picture>` | Add `obsidian-lexvora.css` snippet |
| **VS Code Markdown Preview** | Evaluates `<picture>`, prefers `<img>` fallback | Default standard `<picture>` |
| **Typora / Local IDEs** | Strips `<picture>` wrapper, renders `<img>` | Always provide valid `src` on fallback `<img>` |

## Obsidian CSS Snippet (`obsidian-lexvora.css`)

To ensure smooth dark/light theme switching in Obsidian:

1. Copy `skills/ThemeStyleOps/assets/styles/obsidian-lexvora.css` to your vault's `.obsidian/snippets/lexvora.css`.
2. Enable the snippet in Obsidian: **Settings $\to$ Appearance $\to$ CSS snippets $\to$ lexvora**.

```css
/* Obsidian theme adaptation for Lexvora <picture> elements */
.theme-dark picture img {
  filter: brightness(0.95) contrast(1.05);
}

.theme-light picture img {
  filter: none;
}
```

## Standard Fallback Structure

Every governed document must supply a complete fallback `<img>` inside `<picture>`:

```html
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="path/to/dark-banner.svg">
  <img alt="Area Banner" src="path/to/light-banner.svg" width="100%">
</picture>
```


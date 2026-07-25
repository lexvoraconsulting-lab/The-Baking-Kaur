# TEMPLATE_SPEC.md

**Satisfies completion condition 14.** Buildable specification for the blog templates.

Three templates total: two blog-index templates and **one** article template. Existing theme
sections are reused; nothing new is built where an Ecomus section already does the job.

---

## 1. Why one article template

`Article.templateSuffix` is set **per article** and is **not** inherited from
`Blog.templateSuffix`. Four per-silo article templates would mean hand-configuring a suffix on
every article forever, with no Shopify Flow on the Basic plan, and a silent wrong-layout render on
any miss (`DESIGN_REVIEW.md` F-04).

`Blog.templateSuffix` *does* control the index template, so per-silo **indexes** are safe and free.

| Template | File | Assigned via |
|---|---|---|
| Guides index | `templates/blog.guides.json` | `Blog.templateSuffix = "guides"` on `cake-guides` |
| City index | `templates/blog.city.json` | `Blog.templateSuffix = "city"` on `meerut` |
| Article | `templates/article.json` | default — **no per-article suffix, ever** |

---

## 2. Repairs to existing bindings

Three bindings shipped from the Ecomus demo point at objects that do not exist. All three are
repaired as part of this spec, not carried forward.

| Broken binding | Where | Repair |
|---|---|---|
| `cat_link_list: "blog-categories"` | `article.json`, `blog.list.json` sidebars | **Create** the `blog-categories` link list: Cake Guides → `/blogs/cake-guides`, Meerut → `/blogs/meerut` |
| `blog: "blog-default"` | `article.json` sidebar "Recent Post" | Rebind → `cake-guides` |
| `blog: "list"` | `blog.list.json` sidebar | Rebind → `cake-guides` |
| `comments` block enabled | `article.json` | **Remove.** The blog has `commentPolicy: CLOSED` |

`templates/blog.json` and `templates/blog.list.json` are retained as-is and unused — neither blog
is assigned to them. They are not deleted: they are Ecomus defaults and removing them risks the
theme editor recreating them with different IDs.

---

## 3. `templates/blog.guides.json` — Cake Guides index

Section `main-heading`, then `main-blog`.

**`main-heading`**
| Setting | Value |
|---|---|
| `heading` | Cake Guides |
| `heading_size` | h4 |
| subtitle block | *Choosing, sizing, flavours, cost and craft — from our Meerut kitchen.* |
| `color_scheme` | scheme-2 |

**`main-blog`**
| Setting | Value | Reason |
|---|---|---|
| `article_des` | `des_1` | grid |
| `limit` | **12** | ~160 articles → ~14 pages. v1's 9/page at 450 gave 50 |
| `col_dk / col_tb / col_mb` | 3 / 2 / 1 | |
| `show_content` | false | |
| `show_date` | **true** | freshness is a design goal; hiding the date works against it |
| `show_author` | **true** | E-E-A-T; renders Organization until the `Person` lands |
| `show_tags` | false | tag pages are `noindex`; do not invite clicks into them |
| `show_readmore` | true | |
| `image_ratio` | `-square` | |
| `pagination_type` | links | |
| sidebar | `sidebar_position: right`, `sidebar_drawer: false` | |

**Sidebar blocks** (enabled — v1's `blog.json` had all four disabled)
| Block | Setting |
|---|---|
| `blog_cate` | `cat_link_list: blog-categories`, `count: true` |
| **Subcategory module** *(new)* | Curated links to the 6 subcategory groupings in `BLOG_TAXONOMY.md` §2. This is what makes a 160-article index browsable |
| `post` | `blog: cake-guides`, `limit_post: 3` |
| `gallery` | **disabled** until original photography exists — currently bound to Ecomus demo images |

`tags` block: **disabled.** Tag pages are `noindex` and carry no equity.

---

## 4. `templates/blog.city.json` — Meerut index

Same structure, four differences:

| Setting | Value | Reason |
|---|---|---|
| `heading` | Meerut | |
| subtitle | *Delivery areas, timing, venues and the city's festive calendar.* | |
| `limit` | **12** | ~90 articles → ~8 pages |
| Sidebar extra block | **Delivery CTA** → `/pages/cake-delivery-in-meerut` | Every `meerut` article must reach a commercial destination; the index reinforces it |
| `post` | `blog: meerut` | |

---

## 5. `templates/article.json` — the single article template

Branches internally on `blog.handle`. Block order top to bottom:

| # | Block | Notes |
|---|---|---|
| 1 | `breadcrumb` | `Home > {Blog} > {Article}` — matches `tbk-schema-breadcrumb` |
| 2 | `title` | `show_title: true`, `show_author: true`, `show_date: true`, `show_blog_title: blog_current`, `content_align: start` |
| 3 | **`last_reviewed`** *(new)* | Renders `custom.last_reviewed`. **Required.** Same value as `dateModified` |
| 4 | `image` | Lead image. Rendered only if present — clusters may be text-only |
| 5 | **`answer_first`** *(new)* | Styled first block. The direct answer, ≤60 words. The passage extraction targets |
| 6 | `article_content` | Body |
| 7 | **`key_facts`** *(new)* | Optional. Renders only if the writer supplies it — recommended, not mandatory (`DESIGN_REVIEW.md` M-26) |
| 8 | **`hub_link`** *(new)* | The single up-link, from `custom.hub_url` |
| 9 | **`related_collections`** *(new)* | From `custom.about_refs`, max 3. **Must include ≥1 commercial destination** |
| 10 | **`email_capture`** *(new)* | With an occasion-date field |
| 11 | **`conversion`** *(new)* | Branches on `blog.handle`: `cake-guides` → collection CTA; `meerut` → WhatsApp + delivery page. WhatsApp href carries the `cluster_id` source token |
| 12 | `article_related` | **`limit: 4`**, filtered on matching `custom.cluster_id`. v1 inherited `limit: 8` across the whole blog — random at 160 articles |
| 13 | `tags_social` | Share buttons kept; **tag links removed** |
| 14 | ~~`comments`~~ | **Removed** |
| 15 | `sidebar-blog` | Categories, current-silo recent posts, delivery CTA on `meerut` |

**Removed from v1's plan:** the mandatory FAQ block. Per-article `FAQPage` produces no rich result
for a commercial site (`DESIGN_REVIEW.md` F-01); question-shaped subheadings inside
`article_content` serve extraction without a separate module.

---

## 6. Schema emitted per template

| Template | Snippet | Entities |
|---|---|---|
| Both indexes | **`tbk-schema-blog.liquid`** *(new)* | `Blog` + `ItemList` + `BreadcrumbList` |
| Article | `tbk-schema-article.liquid` *(amended)* | `Article` — `author`→`#person-*`, `publisher`→`#organization`, `isPartOf`→`#blog-*`, **`about`/`mentions`→Product/Collection** |
| Article | `tbk-schema-breadcrumb.liquid` | already branches on `article` — no change |
| Tag pages | none | `noindex, follow` |

### `tbk-schema-article.liquid` — required amendments

```liquid
{%- assign lr = article.metafields.custom.last_reviewed -%}
"dateModified": "{{ lr | default: article.updated_at | date: '%Y-%m-%dT%H:%M:%S+05:30' }}",
"author": { "@id": "https://thebakingkaur.com/#person-{{ article.metafields.custom.author_slug }}" },
"about": [ {%- for ref in article.metafields.custom.about_refs.value -%}
  { "@id": "{{ shop.url }}{{ ref.url }}#{{ ref.object_type }}" }{%- unless forloop.last -%},{%- endunless -%}
{%- endfor -%} ]
```

Three fixes in one edit: `dateModified` no longer falls back to `published_at`; `author` resolves
to a `Person`; and `about` creates the article↔product edge that requires **no change to the
protected product template**.

---

## 7. Tag-page handling

In the blog template, before `content_for_header` renders anything indexable:

```liquid
{%- if current_tags != blank -%}
  <meta name="robots" content="noindex,follow">
{%- endif -%}
```

Keying on `current_tags` covers both `/tagged/{a}` and `/tagged/{a}+{b}` — the surface is
combinatorial, not the 208 pages v1 estimated (`DESIGN_REVIEW.md` S-06).

No link-equity claim is made: a long-term `noindex` page is eventually treated as `nofollow`.

---

## 8. Build order and verification

1. Create the `blog-categories` link list — the templates already expect it.
2. Create the 5 article metafield definitions.
3. Create blogs `cake-guides`, `meerut`; set `Blog.templateSuffix`.
4. Build `blog.guides.json`, `blog.city.json`.
5. Amend `article.json`; remove comments; add the 6 new blocks.
6. Amend `tbk-schema-article.liquid`; add `tbk-schema-blog.liquid`.
7. Add the tag-page `noindex`.
8. Publish one test article per silo.

**Verification checklist before Gate 1** — each is a known unknown, not a formality:

- [ ] Article renders with **no** per-article `templateSuffix` set
- [ ] Sidebar categories resolve (the three broken bindings are fixed)
- [ ] `dateModified` reflects `last_reviewed`, not `published_at`
- [ ] `about` / `mentions` resolve to live Product/Collection `@id`s
- [ ] **Exactly one `FAQPage` exists site-wide**, on `/pages/faqs` — confirms the `theme.liquid:68` deletion
- [ ] `/blogs/cake-guides/tagged/x` and `/tagged/x+y` both return `noindex`
- [ ] `social-meta-tags` emits `og:type=article` — **unverified in this phase**
- [ ] Articles appear in theme search — **unverified in this phase**
- [ ] Breadcrumb correct on an article URL
- [ ] WhatsApp CTA carries the `cluster_id` token
- [ ] Rich Results Test clean

Deploy per `CLAUDE.md`: pull-and-diff first, single-file push to theme `#151307485353`, verify with
`?preview_theme_id=` and a cache-buster before concluding anything is live.

#!/usr/bin/env python3
"""Generate documentation badge and banner SVGs for every theme profile.

Assets are generated, never hand-edited. Change this script and re-run it:

    python3 scripts/generate_theme_assets.py

Output:
    assets/badges/<theme>/<slug>.svg          status, meta, and record-type chips
    assets/banners/<theme>/<area>-<mode>.svg  one banner per governed documentation area

Rules honoured (references/svg-composition-rules.md):
    - system font stack, no text below 13 px
    - <title> and <desc> on every standalone SVG
    - visible labels, never colour alone
    - reading order in the XML matches visual order
"""

import os

def esc(text):
    """XML-escape text destined for markup or an attribute value."""
    return (text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                .replace('"', "&quot;"))


FONT = "system-ui,-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif"
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# --------------------------------------------------------------------------
# Theme profiles. Roles come from references/diagram-color-system.md.
# --------------------------------------------------------------------------

THEMES = {
    "lexvora": {
        "name": "Lexvora Company",
        "roles": {
            "governing": ("#061421", "#ffffff", "#b88445"),
            "system":    ("#102d40", "#ffffff", "#b88445"),
            "decision":  ("#b88445", "#061421", "#8a5723"),
            "success":   ("#0f6b4f", "#ffffff", "#0a4f3a"),
            "risk":      ("#9d2f2f", "#ffffff", "#6f2020"),
            "muted":     ("#5c6670", "#ffffff", "#454e56"),
        },
        "banner": {
            "light": dict(bg="#fbf8f3", panel="#ffffff", ink="#061421", sub="#5c6670",
                          rule="#b88445", edge="rgba(184,132,69,.28)", chip="#061421",
                          chip_ink="#ffffff", accent="#b88445", wash=None),
            "dark":  dict(bg="#061421", panel="#0b2233", ink="#fbf8f3", sub="#9aa4ad",
                          rule="#b88445", edge="rgba(184,132,69,.36)", chip="#102d40",
                          chip_ink="#ffffff", accent="#d2a15f", wash=None),
        },
    },
    "tahoe": {
        "name": "macOS Tahoe Liquid Glass",
        "roles": {
            "governing": ("#172554", "#ffffff", "#2f7dff"),
            "system":    ("#2f7dff", "#ffffff", "#1e5fd0"),
            "decision":  ("#ff7a1a", "#111827", "#c85a08"),
            "success":   ("#00a676", "#ffffff", "#00805a"),
            "risk":      ("#ff3b4f", "#ffffff", "#c62435"),
            "muted":     ("#475569", "#ffffff", "#334155"),
        },
        "banner": {
            "light": dict(bg="#f7fbff", panel="rgba(255,255,255,.68)", ink="#111827",
                          sub="#475569", rule="#2f7dff", edge="rgba(255,255,255,.78)",
                          chip="#2f7dff", chip_ink="#ffffff", accent="#7a3cff",
                          wash=[("#d8f7ff", 0.9), ("#ede9fe", 0.9), ("#fff2e8", 0.9)]),
            "dark":  dict(bg="#0f172a", panel="rgba(148,163,184,.16)", ink="#f8fafc",
                          sub="#94a3b8", rule="#2f7dff", edge="rgba(148,163,184,.34)",
                          chip="#2f7dff", chip_ink="#ffffff", accent="#7a3cff",
                          wash=[("#1e3a8a", 0.55), ("#4c1d95", 0.5), ("#7c2d12", 0.45)]),
        },
    },
}

# --------------------------------------------------------------------------
# Badge catalogue: (slug, label, role, icon)
# --------------------------------------------------------------------------

BADGES = [
    # Plan status ladder (references/plan-authoring.md)
    ("plan-not-started",     "Not Started",     "muted",    "dot"),
    ("plan-planning",        "Planning",        "system",   "dot"),
    ("plan-structure-ready", "Structure Ready", "system",   "dot"),
    ("plan-review",          "Review",          "decision", "diamond"),
    ("plan-accepted",        "Accepted",        "success",  "check"),
    ("plan-implemented",     "Implemented",     "success",  "check"),
    ("plan-verified",        "Verified",        "success",  "check"),
    # Record status ladder (references/traceability.md)
    ("draft",                "Draft",           "muted",    "dot"),
    ("open-question",        "Open Question",   "decision", "question"),
    ("active",               "Active",          "system",   "dot"),
    ("proposed",             "Proposed",        "decision", "diamond"),
    ("confirmed",            "Confirmed",       "success",  "check"),
    ("planned",              "Planned",         "system",   "dot"),
    ("in-delivery",          "In Delivery",     "system",   "clock"),
    ("resolved-by-addition", "Resolved by Addition", "success", "check"),
    ("future-held",          "Future / Held",   "muted",    "clock"),
    ("on-hold",              "On Hold",         "muted",    "clock"),
    ("rejected",             "Rejected",        "risk",     "cross"),
    ("superseded",           "Superseded",      "muted",    "cross"),
    ("deprecated",           "Deprecated",      "risk",     "cross"),
    # Architecture states
    ("arch-current",         "Current",         "success",  "check"),
    ("arch-target",          "Target",          "system",   "diamond"),
    ("arch-tbd",             "TBD",             "muted",    "question"),
    # Gap register states
    ("gap-open",             "Open",            "decision", "alert"),
    ("gap-resolved",         "Resolved",        "success",  "check"),
    ("gap-blocked",          "Blocked",         "risk",     "alert"),
    # Meta chips
    ("question",             "Question",        "decision", "question"),
    ("risk-low",             "Risk Low",        "success",  "alert"),
    ("risk-medium",          "Risk Medium",     "decision", "alert"),
    ("risk-high",            "Risk High",       "risk",     "alert"),
    ("priority-p1",          "P1",              "risk",     "diamond"),
    ("priority-p2",          "P2",              "decision", "diamond"),
    ("priority-p3",          "P3",              "muted",    "diamond"),
    ("estimate-s",           "Est S",           "system",   "clock"),
    ("estimate-m",           "Est M",           "system",   "clock"),
    ("estimate-l",           "Est L",           "system",   "clock"),
    ("estimate-xl",          "Est XL",          "system",   "clock"),
    # Record-type chips
    ("type-plan",            "Plan",            "governing", "doc"),
    ("type-concept",         "Concept",         "governing", "doc"),
    ("type-research",        "Research",        "governing", "doc"),
    ("type-decision",        "Decision",        "governing", "doc"),
    ("type-rule",            "Rule",            "governing", "doc"),
    ("type-architecture",    "Architecture",    "governing", "doc"),
    ("type-worklog",         "Worklog",         "governing", "doc"),
    ("type-gap",             "Gap",             "governing", "doc"),
    ("type-verification",    "Verification",    "governing", "doc"),
]


def badge_icon(kind, cx, cy, ink):
    """Small mark drawn in a 13x13 box centred on (cx, cy)."""
    if kind == "check":
        return (f'<path d="M{cx-4.5} {cy} l3 3.2 l6-6.6" fill="none" stroke="{ink}" '
                f'stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>')
    if kind == "cross":
        return (f'<path d="M{cx-3.6} {cy-3.6} l7.2 7.2 M{cx+3.6} {cy-3.6} l-7.2 7.2" '
                f'fill="none" stroke="{ink}" stroke-width="2" stroke-linecap="round"/>')
    if kind == "alert":
        return (f'<path d="M{cx} {cy-5.2} l5.4 9.4 h-10.8 z" fill="none" stroke="{ink}" '
                f'stroke-width="1.6" stroke-linejoin="round"/>'
                f'<path d="M{cx} {cy-1.4} v2.6" stroke="{ink}" stroke-width="1.6" '
                f'stroke-linecap="round"/><circle cx="{cx}" cy="{cy+3}" r="0.9" fill="{ink}"/>')
    if kind == "question":
        return (f'<path d="M{cx-2.8} {cy-2.2} a2.8 2.8 0 1 1 2.8 3.1 v1.1" fill="none" '
                f'stroke="{ink}" stroke-width="1.8" stroke-linecap="round"/>'
                f'<circle cx="{cx}" cy="{cy+4.4}" r="1" fill="{ink}"/>')
    if kind == "clock":
        return (f'<circle cx="{cx}" cy="{cy}" r="5" fill="none" stroke="{ink}" '
                f'stroke-width="1.6"/><path d="M{cx} {cy-2.8} v3.1 h2.4" fill="none" '
                f'stroke="{ink}" stroke-width="1.6" stroke-linecap="round" '
                f'stroke-linejoin="round"/>')
    if kind == "diamond":
        return f'<path d="M{cx} {cy-5} l5 5 l-5 5 l-5-5 z" fill="{ink}" opacity=".92"/>'
    if kind == "doc":
        return (f'<path d="M{cx-3.8} {cy-5.2} h5.2 l2.4 2.4 v7.9 h-7.6 z" fill="none" '
                f'stroke="{ink}" stroke-width="1.5" stroke-linejoin="round"/>'
                f'<path d="M{cx-1.8} {cy+0.2} h3.4 M{cx-1.8} {cy+2.6} h3.4" stroke="{ink}" '
                f'stroke-width="1.3" stroke-linecap="round"/>')
    return f'<circle cx="{cx}" cy="{cy}" r="3.4" fill="{ink}" opacity=".92"/>'


def make_badge(label, role_colors, icon):
    bg, ink, edge = role_colors
    safe = esc(label)
    pad, icon_w, gap, h, fs = 9, 13, 6, 24, 13
    tl = round(fs * 0.56 * len(label)) + 1
    w = pad + icon_w + gap + tl + pad
    mark = badge_icon(icon, pad + icon_w / 2, h / 2, ink)
    tx = pad + icon_w + gap
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{safe}">
  <title>{safe}</title>
  <desc>Documentation status chip reading {safe}.</desc>
  <rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="5" fill="{bg}" stroke="{edge}"/>
  {mark}
  <text x="{tx}" y="{h / 2 + 4.6}" textLength="{tl}" lengthAdjust="spacingAndGlyphs" font-family="{FONT}" font-size="{fs}" font-weight="600" fill="{ink}">{safe}</text>
</svg>
'''


# --------------------------------------------------------------------------
# Banner catalogue: (slug, title, subtitle)
# --------------------------------------------------------------------------

BANNERS = [
    ("support",        "Support",            "Documentation system entry point and navigation"),
    ("rules",          "Rules",              "Binding constraints that govern how work is done"),
    ("context",        "Context",            "Current state, scope, and working assumptions"),
    ("documentation",  "Documentation",      "Ownership, structure, and documentation planning"),
    ("research",       "Research",           "Investigations, findings, and evidence"),
    ("concept-design", "Concept & Design",   "Statements, questions, and proposed direction"),
    ("architecture",   "Architecture",       "Systems, frameworks, and repository dependencies"),
    ("decisions",      "Decisions",          "Accepted direction with rationale and consequence"),
    ("plans",          "Plans",              "Committed work, tasks, milestones, and statistics"),
    ("changelog",      "Changelog",          "What changed, when, and why"),
    ("gaps-issues",    "Gaps & Issues",      "Intake register for defects, drift, and open risk"),
    ("worklog",        "Worklog",            "Execution record and multi-agent handoff"),
    ("verification",   "Verification",       "Evidence that proves the work actually holds"),
    ("release",        "Release",            "Cut, tagged, and shipped state of the work"),
]

ATTRIB = "Documentation system by Lexvora Consulting"


def banner_icon(slug, t):
    """Area mark drawn inside a 96x96 box at the origin."""
    a, ink = t["accent"], t["ink"]
    s = f'<g fill="none" stroke="{a}" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round">'
    if slug == "support":
        s += '<path d="M14 18 h30 a10 10 0 0 1 10 10 v50 a8 8 0 0 0-8-8 H14 z"/><path d="M82 18 H52 a10 10 0 0 0-10 10 v50 a8 8 0 0 1 8-8 h32 z"/>'
    elif slug == "rules":
        s += '<path d="M48 12 l30 12 v22 c0 20-13 32-30 40-17-8-30-20-30-40 V24 z"/><path d="M36 46 l8 9 l17-18"/>'
    elif slug == "context":
        s += '<circle cx="48" cy="48" r="32"/><path d="M62 34 L41 41 L34 62 L55 55 z"/>'
    elif slug == "documentation":
        s += '<path d="M24 14 h32 l18 18 v50 H24 z"/><path d="M56 14 v18 h18"/><path d="M34 50 h28 M34 62 h28"/>'
    elif slug == "research":
        s += '<circle cx="42" cy="42" r="24"/><path d="M60 60 L80 80"/>'
    elif slug == "concept-design":
        s += '<path d="M48 14 a22 22 0 0 1 13 39 v9 H35 v-9 a22 22 0 0 1 13-39 z"/><path d="M38 72 h20 M41 82 h14"/>'
    elif slug == "architecture":
        s += '<rect x="30" y="12" width="36" height="20" rx="4"/><rect x="12" y="52" width="32" height="20" rx="4"/><rect x="52" y="52" width="32" height="20" rx="4"/><path d="M48 32 v10 M28 42 h40 M28 42 v10 M68 42 v10"/>'
    elif slug == "decisions":
        s += '<path d="M48 14 v68"/><path d="M48 26 h26 l8 10 l-8 10 H48"/><path d="M48 52 H22 l-8 10 l8 10 h26"/>'
    elif slug == "plans":
        s += '<rect x="18" y="14" width="60" height="68" rx="6"/><path d="M30 34 l6 6 l12-12"/><path d="M56 36 h12"/><path d="M30 56 l6 6 l12-12"/><path d="M56 58 h12"/>'
    elif slug == "changelog":
        s += '<path d="M20 24 h56 M20 44 h40 M20 64 h48"/><circle cx="76" cy="44" r="8"/>'
    elif slug == "gaps-issues":
        s += '<path d="M48 14 l36 62 H12 z"/><path d="M48 40 v18"/><circle cx="48" cy="67" r="2.6" fill="' + a + '"/>'
    elif slug == "worklog":
        s += '<circle cx="48" cy="48" r="32"/><path d="M48 28 v22 h16"/>'
    elif slug == "verification":
        s += '<path d="M48 12 l28 12 v24 c0 18-12 28-28 36-16-8-28-18-28-36 V24 z"/><path d="M34 46 l10 11 l20-22"/>'
    elif slug == "release":
        s += '<path d="M48 12 l32 18 v36 L48 84 L16 66 V30 z"/><path d="M16 30 l32 18 l32-18 M48 48 v36"/>'
    else:
        s += '<circle cx="48" cy="48" r="30"/>'
    return s + "</g>"


def make_banner(slug, title, subtitle, theme_key, mode):
    t = THEMES[theme_key]["banner"][mode]
    title, subtitle = esc(title), esc(subtitle)
    W, H = 1200, 200
    defs, wash = "", ""
    if t["wash"]:
        stops = "".join(
            f'<stop offset="{i / (len(t["wash"]) - 1):.2f}" stop-color="{c}" stop-opacity="{o}"/>'
            for i, (c, o) in enumerate(t["wash"]))
        defs = (f'<defs><linearGradient id="w" x1="0" y1="0" x2="1" y2="1">{stops}</linearGradient>'
                f'<filter id="b" x="-30%" y="-30%" width="160%" height="160%">'
                f'<feGaussianBlur stdDeviation="34"/></filter></defs>')
        wash = (f'<g filter="url(#b)" opacity=".85"><circle cx="250" cy="60" r="120" fill="url(#w)"/>'
                f'<circle cx="880" cy="170" r="140" fill="url(#w)"/></g>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{title}">
  <title>{title}</title>
  <desc>{subtitle}. {THEMES[theme_key]["name"]} theme, {mode} appearance.</desc>
  {defs}
  <rect width="{W}" height="{H}" rx="16" fill="{t["bg"]}"/>
  {wash}
  <rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="16" fill="none" stroke="{t["edge"]}"/>
  <rect x="0" y="0" width="{W}" height="5" rx="2.5" fill="{t["rule"]}"/>
  <g transform="translate(64,52)">{banner_icon(slug, t)}</g>
  <text x="200" y="86" font-family="{FONT}" font-size="42" font-weight="700" fill="{t["ink"]}">{title}</text>
  <rect x="200" y="102" width="54" height="4" rx="2" fill="{t["rule"]}"/>
  <text x="200" y="134" font-family="{FONT}" font-size="17" fill="{t["sub"]}">{subtitle}</text>
  <text x="200" y="163" font-family="{FONT}" font-size="14" fill="{t["sub"]}" opacity=".85">{ATTRIB}</text>
</svg>
'''



# --------------------------------------------------------------------------
# Gallery page. Generated so the catalogue can never drift from the assets.
# --------------------------------------------------------------------------

FAMILIES = [
    ("Plan status ladder", "plan-", "Applied to a Plan as a whole in `plans/`."),
    ("Record status ladder", None, "Applied to concepts, research, and traceability rows."),
    ("Architecture states", "arch-", "Applied to architecture records."),
    ("Gap register states", "gap-", "Applied to rows in `gaps-issues/`."),
    ("Risk, priority, and estimate", None, "Applied to any row that carries sizing or exposure."),
    ("Record types", "type-", "Applied in navigation tables and indexes."),
]

META = {"question", "risk-low", "risk-medium", "risk-high", "priority-p1", "priority-p2",
        "priority-p3", "estimate-s", "estimate-m", "estimate-l", "estimate-xl"}
RECORD = {"draft", "open-question", "active", "proposed", "confirmed", "planned", "in-delivery",
          "resolved-by-addition", "future-held", "on-hold", "rejected", "superseded", "deprecated"}


def family_of(slug):
    for title, prefix, _ in FAMILIES:
        if prefix and slug.startswith(prefix):
            return title
    if slug in META:
        return "Risk, priority, and estimate"
    if slug in RECORD:
        return "Record status ladder"
    return "Record status ladder"


def write_gallery():
    out = ["# Theme Asset Gallery", "",
           "Every generated badge and banner, rendered as GitHub serves it. This page is written by",
           "[`../scripts/generate_theme_assets.py`](../scripts/generate_theme_assets.py); edit the",
           "script and re-run it rather than editing this file.", "",
           "## Navigation", "",
           "Parent: [`README.md`](../README.md) · Contract: [`SKILL.md`](../SKILL.md) · Rules:",
           "[`banner-and-badge-system.md`](../references/banner-and-badge-system.md) ·",
           "[`github-rendering.md`](../references/github-rendering.md)", "",
           "## Table of Contents", "",
           "- [Navigation](#navigation)", "- [Banners](#banners)", "- [Badges](#badges)",
           "- [Sample Documentation Sets](#sample-documentation-sets)",
           "- [Regenerating](#regenerating)", "",
           "## Sample Documentation Sets", "",
           "These assets applied to a complete governed documentation set, one per theme profile.",
           "Both sets carry identical content so they can be compared directly.", "",
           "| S.No. | Set | Theme |", "| ---: | --- | --- |",
           "| 1 | [`lexvora/`](./lexvora/) | Lexvora Company |",
           "| 2 | [`tahoe/`](./tahoe/) | macOS Tahoe Liquid Glass |", ""]

    out += ["## Banners", "",
            "One banner per governed documentation area, in both theme profiles. Each is a",
            "light/dark pair; the embed below switches automatically with the reader's GitHub",
            "appearance.", ""]
    for theme_key, theme in THEMES.items():
        out += [f"### {theme['name']}", ""]
        for slug, title, subtitle in BANNERS:
            out += [f"**{title}** — {subtitle}", "",
                    "<picture>",
                    f'  <source media="(prefers-color-scheme: dark)" srcset="../assets/banners/{theme_key}/{slug}-dark.svg">',
                    f'  <img alt="{title}" src="../assets/banners/{theme_key}/{slug}-light.svg" width="100%">',
                    "</picture>", ""]

    out += ["## Badges", "",
            "Chips are self-contained: each carries its own fill, border, icon, and label, so a",
            "single file reads correctly in both light and dark appearance. The label always states",
            "the meaning, so nothing is lost when images are disabled.", ""]
    for fam_title, _, note in FAMILIES:
        members = [b for b in BADGES if family_of(b[0]) == fam_title]
        if not members:
            continue
        out += [f"### {fam_title}", "", note, "",
                "| S.No. | Lexvora Company | macOS Tahoe Liquid Glass | Slug | Semantic role |",
                "| ---: | --- | --- | --- | --- |"]
        for i, (slug, label, role, _icon) in enumerate(members, 1):
            out.append(
                f"| {i} | ![{label}](../assets/badges/lexvora/{slug}.svg) "
                f"| ![{label}](../assets/badges/tahoe/{slug}.svg) | `{slug}` | `{role}` |")
        out.append("")

    out += ["## Regenerating", "",
            "```bash",
            "python3 skills/ThemeStyleOps/scripts/generate_theme_assets.py",
            "```", "",
            "Add a chip or an area by editing `BADGES` or `BANNERS` in the script, then re-run it.",
            "Assets and this gallery are rewritten together.", "",
            "## Footer Navigation", "",
            "Parent: [`README.md`](../README.md) · Rules:",
            "[`banner-and-badge-system.md`](../references/banner-and-badge-system.md)", ""]

    with open(os.path.join(HERE, "samples", "theme-asset-gallery.md"), "w") as fh:
        fh.write("\n".join(out))
    return len(BANNERS) * len(THEMES), len(BADGES) * len(THEMES)


# --------------------------------------------------------------------------
# Sample document set. One governed document per area, per theme profile.
# Content is defined once; only the theme assets differ between the sets.
#
# Cell macros:
#   {S:slug|Label}  status chip, counted in the Status Summary
#   {B:slug|Label}  supporting chip, not counted
# --------------------------------------------------------------------------

PROJECT = "Client Portal Platform"

SAMPLE_DOCS = [
    ("support", "Support", "Entry point for the {p} documentation system.", [
        ("Governed Areas", "Every area below has one master document and one banner.", [
            ["S.No.", "Area", "Type", "State", "Owner"],
            ["1", "[`context`](./context.md)", "{B:type-rule|Rule}", "{S:active|Active}", "Delivery lead"],
            ["2", "[`rules`](./rules.md)", "{B:type-rule|Rule}", "{S:confirmed|Confirmed}", "Delivery lead"],
            ["3", "[`research`](./research.md)", "{B:type-research|Research}", "{S:active|Active}", "Architect"],
            ["4", "[`concept-design`](./concept-design.md)", "{B:type-concept|Concept}", "{S:proposed|Proposed}", "Architect"],
            ["5", "[`architecture`](./architecture.md)", "{B:type-architecture|Architecture}", "{S:confirmed|Confirmed}", "Architect"],
            ["6", "[`decisions`](./decisions.md)", "{B:type-decision|Decision}", "{S:active|Active}", "Delivery lead"],
            ["7", "[`plans`](./plans.md)", "{B:type-plan|Plan}", "{S:in-delivery|In Delivery}", "Delivery lead"],
            ["8", "[`gaps-issues`](./gaps-issues.md)", "{B:type-gap|Gap}", "{S:active|Active}", "Whole team"],
            ["9", "[`worklog`](./worklog.md)", "{B:type-worklog|Worklog}", "{S:active|Active}", "Whole team"],
            ["10", "[`verification`](./verification.md)", "{B:type-verification|Verification}", "{S:planned|Planned}", "QA"],
            ["11", "[`documentation`](./documentation.md)", "{B:type-rule|Rule}", "{S:confirmed|Confirmed}", "Delivery lead"],
            ["12", "[`changelog`](./changelog.md)", "{B:type-rule|Rule}", "{S:active|Active}", "Delivery lead"],
            ["13", "[`release`](./release.md)", "{B:type-rule|Rule}", "{S:planned|Planned}", "Delivery lead"],
        ]),
    ], "Read `context` first, then `plans`. Everything else is reference."),

    ("context", "Context", "Where {p} stands right now, and what is assumed.", [
        ("Current State", "What is true today, not what is intended.", [
            ["S.No.", "Area", "State", "Note"],
            ["1", "Authentication", "{S:confirmed|Confirmed}", "Single sign-on is live for internal users."],
            ["2", "Client onboarding", "{S:in-delivery|In Delivery}", "Two of five screens are built."],
            ["3", "Reporting", "{S:draft|Draft}", "Requirements captured, not evaluated."],
            ["4", "Billing export", "{S:on-hold|On Hold}", "Waiting on the finance system upgrade."],
        ]),
        ("Working Assumptions", "Each assumption is a risk until it is confirmed.", [
            ["S.No.", "Assumption", "Risk", "Owner"],
            ["1", "The finance API stays on v2 until Q4", "{B:risk-high|Risk High}", "Architect"],
            ["2", "Client count stays under 500", "{B:risk-low|Risk Low}", "Delivery lead"],
            ["3", "No offline mode is required", "{B:risk-medium|Risk Medium}", "Product"],
        ]),
    ], "Update this file whenever reality moves. A stale context file is worse than none."),

    ("rules", "Rules", "Binding constraints for everyone working on {p}.", [
        ("Binding Rules", "These are not suggestions. Breaking one requires a Decision record.", [
            ["S.No.", "Rule", "Applies to", "State"],
            ["1", "No client data in logs, ever", "All code", "{S:confirmed|Confirmed}"],
            ["2", "Every schema change ships with a reversible migration", "Database", "{S:confirmed|Confirmed}"],
            ["3", "Every Plan task links to a source record", "Documentation", "{S:confirmed|Confirmed}"],
            ["4", "Secrets never enter process arguments", "All code", "{S:confirmed|Confirmed}"],
            ["5", "Public API changes need an accepted Decision first", "API", "{S:proposed|Proposed}"],
        ]),
    ], "A rule that quietly disappears is worse than one that never existed. Retire rules explicitly."),

    ("research", "Research", "Investigations and evidence behind {p} choices.", [
        ("Topics", "Research is intake. Delivery belongs to a Plan.", [
            ["S.No.", "Topic", "State", "Effort", "Feeds"],
            ["1", "Session storage options", "{S:confirmed|Confirmed}", "{B:estimate-m|Est M}", "`ADR-002`"],
            ["2", "Rate-limit strategies", "{S:active|Active}", "{B:estimate-l|Est L}", "`PLAN-03`"],
            ["3", "Audit-log retention law", "{S:open-question|Open Question}", "{B:estimate-s|Est S}", "Pending legal"],
            ["4", "Offline sync feasibility", "{S:rejected|Rejected}", "{B:estimate-xl|Est XL}", "Out of scope"],
        ]),
        ("Findings", "A finding is only useful when something downstream consumes it.", [
            ["S.No.", "Finding", "Confidence", "Consumed by"],
            ["1", "Token rotation must be server-side", "{B:risk-low|Risk Low}", "`ADR-002`"],
            ["2", "Per-client quotas beat global quotas", "{B:risk-medium|Risk Medium}", "`PLAN-03`"],
        ]),
    ], "Promote a confirmed topic into a Concept or a Plan; do not let it sit here."),

    ("concept-design", "Concept & Design", "Proposed direction for {p}, before it is committed.", [
        ("Concept Statements", "Every statement carries a status. No status means it is not tracked.", [
            ["S.No.", "Statement", "State", "Maps to"],
            ["1", "Clients self-serve their own API keys", "{S:planned|Planned}", "`PLAN-03`"],
            ["2", "One dashboard for all client activity", "{S:confirmed|Confirmed}", "`PLAN-01`"],
            ["3", "Usage alerts are opt-in per client", "{S:proposed|Proposed}", "Unmapped"],
            ["4", "White-label branding per client", "{S:future-held|Future / Held}", "Not scheduled"],
        ]),
        ("Open Questions", "An unanswered question blocks the concept that depends on it.", [
            ["S.No.", "Question", "State", "Blocks"],
            ["1", "Do clients need sub-accounts?", "{S:open-question|Open Question}", "Concept 1"],
            ["2", "Who owns key revocation?", "{S:open-question|Open Question}", "Concept 1"],
            ["3", "Is SSO mandatory for all tiers?", "{S:resolved-by-addition|Resolved by Addition}", "Answered in `ADR-001`"],
        ]),
    ], "A concept that stays unmapped past one cycle is either rejected or held. Decide."),

    ("architecture", "Architecture", "Systems, boundaries, and dependencies for {p}.", [
        ("Components", "Current is what runs. Target is what is agreed. Nothing else is real.", [
            ["S.No.", "Component", "State", "Owner", "Note"],
            ["1", "Edge gateway", "{S:arch-current|Current}", "Platform", "Handles auth and routing."],
            ["2", "Client service", "{S:arch-current|Current}", "Platform", "Owns client records."],
            ["3", "Quota service", "{S:arch-target|Target}", "Platform", "Agreed in `ADR-003`, not built."],
            ["4", "Reporting store", "{S:arch-tbd|TBD}", "Unassigned", "Shape not decided."],
            ["5", "Legacy billing bridge", "{S:deprecated|Deprecated}", "Finance", "Removed after the v2 cutover."],
        ]),
        ("Dependencies", "A dependency you cannot name is a dependency you cannot manage.", [
            ["S.No.", "Depends on", "Direction", "Risk"],
            ["1", "Finance API v2", "Outbound", "{B:risk-high|Risk High}"],
            ["2", "Identity provider", "Inbound", "{B:risk-medium|Risk Medium}"],
            ["3", "Object storage", "Outbound", "{B:risk-low|Risk Low}"],
        ]),
    ], "Keep this file honest about `Current` versus `Target`; that gap is the real backlog."),

    ("decisions", "Decisions", "Accepted direction for {p}, with rationale and consequence.", [
        ("Decision Register", "A decision without a consequence line is not a decision.", [
            ["S.No.", "ID", "Decision", "State", "Consequence"],
            ["1", "`ADR-001`", "SSO is mandatory for every tier", "{S:confirmed|Confirmed}", "No password login path is built."],
            ["2", "`ADR-002`", "Sessions are server-side, rotated hourly", "{S:confirmed|Confirmed}", "Needs shared session storage."],
            ["3", "`ADR-003`", "Quotas are enforced per client, not globally", "{S:proposed|Proposed}", "Adds the quota service."],
            ["4", "`ADR-004`", "Store reports in the primary database", "{S:superseded|Superseded}", "Replaced by `ADR-005`."],
            ["5", "`ADR-005`", "Reports move to a separate store", "{S:proposed|Proposed}", "Adds an export pipeline."],
        ]),
    ], "Supersede a decision with a new record. Never edit an accepted one in place."),

    ("plans", "Plans", "Committed work for {p}, with tasks, milestones, and statistics.", [
        ("Plan Register", "A Plan carries a richer status than a task, because done and proven differ.", [
            ["S.No.", "Plan", "Title", "State", "Priority"],
            ["1", "`PLAN-01`", "Client dashboard", "{S:plan-verified|Verified}", "{B:priority-p2|P2}"],
            ["2", "`PLAN-02`", "Onboarding flow", "{S:plan-implemented|Implemented}", "{B:priority-p1|P1}"],
            ["3", "`PLAN-03`", "Self-serve API keys", "{S:plan-accepted|Accepted}", "{B:priority-p1|P1}"],
            ["4", "`PLAN-04`", "Usage alerts", "{S:plan-review|Review}", "{B:priority-p3|P3}"],
            ["5", "`PLAN-05`", "Reporting export", "{S:plan-planning|Planning}", "{B:priority-p2|P2}"],
            ["6", "`PLAN-06`", "White-label branding", "{S:plan-not-started|Not Started}", "{B:priority-p3|P3}"],
        ]),
        ("01 Self-Serve API Keys tasks", "Tasks for `PLAN-03`. Every task names a source record.", [
            ["S.No.", "Task", "Estimate", "Risk", "Source"],
            ["1", "Key issue and revoke endpoints", "{B:estimate-m|Est M}", "{B:risk-medium|Risk Medium}", "`ADR-003`"],
            ["2", "Key rotation schedule", "{B:estimate-s|Est S}", "{B:risk-low|Risk Low}", "Research 1"],
            ["3", "Client-facing key screen", "{B:estimate-l|Est L}", "{B:risk-low|Risk Low}", "Concept 1"],
            ["4", "Quota enforcement hook", "{B:estimate-l|Est L}", "{B:risk-high|Risk High}", "`ADR-003`"],
        ]),
        ("Cumulative Statistics", "Counts roll up; they are never estimated by hand.", [
            ["S.No.", "Measure", "Count"],
            ["1", "Plans total", "6"],
            ["2", "Plans verified", "1"],
            ["3", "Tasks in `PLAN-03`", "4"],
            ["4", "Tasks blocked", "0"],
            ["**Total**", "**Tracked records**", "**11**"],
        ]),
    ], "`IMPLEMENTED` and `VERIFIED` require real evidence. Neither is inferred from a file existing."),

    ("gaps-issues", "Gaps & Issues", "Intake register for defects, drift, and open risk in {p}.", [
        ("Gap Register", "Intake only. Delivery belongs to a Plan.", [
            ["S.No.", "ID", "Gap", "State", "Risk"],
            ["1", "`G-01`", "No audit trail on key revocation", "{S:gap-open|Open}", "{B:risk-high|Risk High}"],
            ["2", "`G-02`", "Onboarding emails bypass the template system", "{S:gap-resolved|Resolved}", "{B:risk-low|Risk Low}"],
            ["3", "`G-03`", "Quota service has no owner", "{S:gap-blocked|Blocked}", "{B:risk-high|Risk High}"],
            ["4", "`G-04`", "Reporting store shape undecided", "{S:gap-open|Open}", "{B:risk-medium|Risk Medium}"],
            ["5", "`G-05`", "Duplicate client records from the v1 import", "{S:gap-resolved|Resolved}", "{B:risk-medium|Risk Medium}"],
        ]),
    ], "A rejected gap keeps its reasoning, so it is not raised again."),

    ("documentation", "Documentation", "Who owns which document in {p}, and how it stays true.", [
        ("Ownership", "Every governed document has exactly one owner.", [
            ["S.No.", "Document", "Owner", "Cadence", "State"],
            ["1", "`context`", "Delivery lead", "Weekly", "{S:confirmed|Confirmed}"],
            ["2", "`plans`", "Delivery lead", "Per change", "{S:confirmed|Confirmed}"],
            ["3", "`architecture`", "Architect", "Per change", "{S:active|Active}"],
            ["4", "`verification`", "QA", "Per release", "{S:planned|Planned}"],
            ["5", "`changelog`", "Delivery lead", "Per release", "{S:confirmed|Confirmed}"],
        ]),
    ], "Documentation drift is a defect. Record it in `gaps-issues`, not in a side conversation."),

    ("worklog", "Worklog", "Execution record and handoff for {p}.", [
        ("Sessions", "Written for the next person, who has none of your context.", [
            ["S.No.", "Date", "Work", "State", "Evidence"],
            ["1", "2026-08-18", "Built key issue endpoint", "{S:confirmed|Confirmed}", "Test run attached"],
            ["2", "2026-08-19", "Drafted quota hook", "{S:in-delivery|In Delivery}", "Branch open"],
            ["3", "2026-08-20", "Investigated duplicate clients", "{S:resolved-by-addition|Resolved by Addition}", "Closed `G-05`"],
            ["4", "2026-08-21", "Paused reporting export", "{S:on-hold|On Hold}", "Waiting on `ADR-005`"],
        ]),
    ], "Hand off with what is true, what is half-done, and what you would do next."),

    ("verification", "Verification", "Evidence that {p} actually holds.", [
        ("Checks", "A check without evidence is an opinion.", [
            ["S.No.", "Check", "State", "Evidence"],
            ["1", "SSO login for every tier", "{S:plan-verified|Verified}", "Manual run, 2026-08-20"],
            ["2", "Session rotates hourly", "{S:plan-verified|Verified}", "Automated test"],
            ["3", "Key revocation is audited", "{S:gap-blocked|Blocked}", "Blocked by `G-01`"],
            ["4", "Quota enforcement", "{S:planned|Planned}", "Not built"],
            ["5", "Reporting export accuracy", "{S:draft|Draft}", "No test yet"],
        ]),
    ], "No skill, plan, or claim is verified because it was written down. Only evidence verifies."),

    ("changelog", "Changelog", "What changed in {p}, when, and why.", [
        ("Releases", "Every entry names the reason, not only the change.", [
            ["S.No.", "Version", "Date", "Change", "State"],
            ["1", "`1.3.0`", "2026-08-21", "Self-serve API keys, first cut", "{S:in-delivery|In Delivery}"],
            ["2", "`1.2.0`", "2026-08-11", "Onboarding flow complete", "{S:confirmed|Confirmed}"],
            ["3", "`1.1.0`", "2026-07-30", "Client dashboard", "{S:confirmed|Confirmed}"],
            ["4", "`1.0.0`", "2026-07-02", "First client release", "{S:confirmed|Confirmed}"],
        ]),
    ], "Retire an entry explicitly. Silent removal breaks the trail."),

    ("release", "Release", "Cut, tagged, and shipped state of {p}.", [
        ("Release Readiness", "A release is ready when every gate is proven, not when the date arrives.", [
            ["S.No.", "Gate", "State", "Owner"],
            ["1", "All `P1` plans implemented", "{S:confirmed|Confirmed}", "Delivery lead"],
            ["2", "Verification checks passed", "{S:gap-blocked|Blocked}", "QA"],
            ["3", "Changelog written", "{S:confirmed|Confirmed}", "Delivery lead"],
            ["4", "Rollback rehearsed", "{S:planned|Planned}", "Platform"],
            ["5", "Client comms drafted", "{S:draft|Draft}", "Product"],
        ]),
    ], "One blocked gate blocks the release. Ship the date, not the gates, and you ship the defect."),
]

STATUS_LABELS = {}


def expand(cell, theme_key, counter):
    """Expand {S:slug|Label} and {B:slug|Label} into image references."""
    import re as _re

    def sub(m):
        kind, slug, label = m.group(1), m.group(2), m.group(3)
        if kind == "S":
            counter[label] = counter.get(label, 0) + 1
        return f"![{label}](../../assets/badges/{theme_key}/{slug}.svg)"

    return _re.sub(r"\{([SB]):([a-z0-9-]+)\|([^}]+)\}", sub, cell)


def slugify(text):
    import re as _re
    return _re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def write_sample_doc(theme_key, slug, title, purpose, sections, closing):
    counter = {}
    body = []
    for heading, intro, rows in sections:
        body += [f"## {heading}", "", intro, ""]
        header, divider = rows[0], None
        aligns = ["---: "] + ["---"] * (len(header) - 1)
        body.append("| " + " | ".join(header) + " |")
        body.append("| " + " | ".join(aligns) + " |")
        for row in rows[1:]:
            body.append("| " + " | ".join(expand(c, theme_key, counter) for c in row) + " |")
        body.append("")

    toc = ["- [Navigation](#navigation)"]
    if counter:
        toc.append("- [Status Summary](#status-summary)")
    toc += [f"- [{h}](#{slugify(h)})" for h, _, _ in sections]
    toc.append("- [Footer Navigation](#footer-navigation)")

    summary = []
    if counter:
        summary = ["## Status Summary", "",
                   "Counted from the tables below. The bold `Total` row must always sum them.", "",
                   "| S.No. | Status | Count |", "| ---: | --- | ---: |"]
        for i, (label, n) in enumerate(sorted(counter.items(), key=lambda kv: (-kv[1], kv[0])), 1):
            summary.append(f"| {i} | {label} | {n} |")
        summary += [f"| **Total** | **Tracked records** | **{sum(counter.values())}** |", ""]

    out = ["<picture>",
           f'  <source media="(prefers-color-scheme: dark)" srcset="../../assets/banners/{theme_key}/{slug}-dark.svg">',
           f'  <img alt="{title}" src="../../assets/banners/{theme_key}/{slug}-light.svg" width="100%">',
           "</picture>", "",
           f"# {title}", "",
           purpose.replace("{p}", PROJECT), "",
           "## Navigation", "",
           "Parent: [`README.md`](./README.md) · Theme:",
           f"[`{THEMES[theme_key]['name']}`](../../references/{'lexvora-company' if theme_key == 'lexvora' else 'macos-tahoe-liquid-glass'}.md) ·",
           "Rules: [`banner-and-badge-system.md`](../../references/banner-and-badge-system.md)", "",
           "## Table of Contents", ""] + toc + [""] + summary + body + [
           "> [!NOTE]", f"> {closing}", "",
           "## Footer Navigation", "",
           "Parent: [`README.md`](./README.md) · Gallery:",
           "[`theme-asset-gallery.md`](../theme-asset-gallery.md)", ""]
    return "\n".join(out)


def write_samples():
    written = 0
    for theme_key, theme in THEMES.items():
        d = os.path.join(HERE, "samples", theme_key)
        os.makedirs(d, exist_ok=True)
        index = ["<picture>",
                 f'  <source media="(prefers-color-scheme: dark)" srcset="../../assets/banners/{theme_key}/support-dark.svg">',
                 f'  <img alt="Support" src="../../assets/banners/{theme_key}/support-light.svg" width="100%">',
                 "</picture>", "",
                 f"# {theme['name']} Sample Documentation Set", "",
                 f"A complete governed documentation set for a fictional project, {PROJECT}, rendered in the",
                 f"`{theme_key}` theme. Every file shows its area banner, its status chips, and the navigation,",
                 "table-of-contents, status-summary, and `S.No.` table rules the documentation skill requires.", "",
                 "The two sample sets carry identical content. Only the theme differs, so they can be compared",
                 "side by side. Both sets are generated by",
                 "[`../../scripts/generate_theme_assets.py`](../../scripts/generate_theme_assets.py).", "",
                 "## Navigation", "",
                 "Parent: [`../../README.md`](../../README.md) · Other set:",
                 f"[`{'tahoe' if theme_key == 'lexvora' else 'lexvora'}/`](../{'tahoe' if theme_key == 'lexvora' else 'lexvora'}/) ·",
                 "Gallery: [`../theme-asset-gallery.md`](../theme-asset-gallery.md)", "",
                 "## Sample Documents", "",
                 "| S.No. | Document | Type | Shows |",
                 "| ---: | --- | --- | --- |"]
        shows = {
            "support": "Area index with record-type chips",
            "context": "Current state and assumption risk",
            "rules": "Binding constraints with confirmation state",
            "research": "Topic ladder with effort sizing",
            "concept-design": "Concept statements and open questions",
            "architecture": "Current, Target, TBD, and Deprecated states",
            "decisions": "Decision register with supersession",
            "plans": "Plan ladder, task sizing, cumulative statistics",
            "gaps-issues": "Gap register with risk chips",
            "documentation": "Document ownership and cadence",
            "worklog": "Execution record and handoff",
            "verification": "Checks bound to evidence",
            "changelog": "Release history",
            "release": "Readiness gates",
        }
        for i, (slug, title, purpose, sections, closing) in enumerate(SAMPLE_DOCS, 1):
            with open(os.path.join(d, f"{slug}.md"), "w") as fh:
                fh.write(write_sample_doc(theme_key, slug, title, purpose, sections, closing))
            written += 1
            chip = {"support": "type-rule", "context": "type-rule", "rules": "type-rule",
                    "research": "type-research", "concept-design": "type-concept",
                    "architecture": "type-architecture", "decisions": "type-decision",
                    "plans": "type-plan", "gaps-issues": "type-gap", "documentation": "type-rule",
                    "worklog": "type-worklog", "verification": "type-verification",
                    "changelog": "type-rule", "release": "type-rule"}[slug]
            index.append(f"| {i} | [`{slug}.md`](./{slug}.md) | "
                         f"![chip](../../assets/badges/{theme_key}/{chip}.svg) | {shows[slug]} |")
        index += ["", "## Footer Navigation", "",
                  "Parent: [`../../README.md`](../../README.md) · Gallery:",
                  "[`../theme-asset-gallery.md`](../theme-asset-gallery.md)", ""]
        with open(os.path.join(d, "README.md"), "w") as fh:
            fh.write("\n".join(index))
        written += 1
    return written


def main():
    counts = {"badges": 0, "banners": 0}
    for theme_key, theme in THEMES.items():
        bdir = os.path.join(HERE, "assets", "badges", theme_key)
        ndir = os.path.join(HERE, "assets", "banners", theme_key)
        os.makedirs(bdir, exist_ok=True)
        os.makedirs(ndir, exist_ok=True)
        for slug, label, role, icon in BADGES:
            with open(os.path.join(bdir, f"{slug}.svg"), "w") as fh:
                fh.write(make_badge(label, theme["roles"][role], icon))
            counts["badges"] += 1
        for slug, title, subtitle in BANNERS:
            for mode in ("light", "dark"):
                with open(os.path.join(ndir, f"{slug}-{mode}.svg"), "w") as fh:
                    fh.write(make_banner(slug, title, subtitle, theme_key, mode))
                counts["banners"] += 1
    write_gallery()
    n = write_samples()
    print(f"badges: {counts['badges']}  banners: {counts['banners']}  gallery: written  samples: {n}")


if __name__ == "__main__":
    main()

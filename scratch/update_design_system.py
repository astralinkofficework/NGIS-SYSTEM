design_system_css = """@import url('design-tokens.css');
@import url('shared-components.css');

/* ============================================================
   NGIS ERP — Master Global Design System & Visual Style
   Strict 5-Color System:
   - Navy:      #202F63 (Primary Color: main navigation, sidebar, primary headings, structural elements)
   - Burgundy:  #92243D (The ONLY Accent Color: primary action buttons, key highlights, small visual emphasis)
   - White:     #FFFFFF (Main Surface: page backgrounds, cards, panels, forms, tables, modals)
   - Black:     #000000 (Text & Contrast: body text, strong contrast, important labels, crisp icons)
   - Soft Gray: #F3F3F5 (Secondary Surface: subtle canvas, table separators, input surfaces)

   Strict Rules:
   - Primary Font: Manrope (font-weight <= 500 per AGENTS.md)
   - Continuous Canvas: var(--token-canvas) (#F3F3F5)
   - Content Surfaces: var(--token-surface) (#FFFFFF with 1px solid #E5E5E8 border & 14px radius)
   - Transparent Backgrounds for headers, navigation, filter strips, breadcrumbs
   - Strictly ZERO colored hover overlays, ZERO lifting, ZERO scaling
   ============================================================ */

/* ── 1. Universal Design Tokens ──────────────────────────────── */
:root {
  /* Typography */
  --font-primary: var(--token-font-family);
  --font-khmer: var(--token-font-khmer);
  --font-mono: var(--token-font-mono);

  /* Neutral Surface Palette */
  --ngis-canvas: var(--token-canvas);
  --ngis-surface: var(--token-surface);
  --ngis-surface-subtle: var(--token-surface-subtle);
  --ngis-surface-translucent: var(--token-surface-translucent);

  /* Borders & Outlines */
  --ngis-border: var(--token-border);
  --ngis-border-subtle: var(--token-border-subtle);
  --ngis-border-hover: var(--color-navy);

  /* Typography Colors */
  --ngis-text-primary: var(--token-text-primary);
  --ngis-text-secondary: var(--token-text-secondary);
  --ngis-text-muted: var(--token-text-muted);
  --ngis-text-faint: var(--token-text-faint);

  /* Brand Accent: Single Accent #92243D (Burgundy) */
  --ngis-brand-forest: var(--color-navy);
  --ngis-brand-teal: var(--color-navy);
  --ngis-brand-hover: var(--color-navy);

  /* Minimal Shadows */
  --ngis-shadow-card: var(--token-shadow-card);
  --ngis-shadow-float: var(--token-shadow-float);
  --ngis-shadow-none: var(--token-shadow-none);

  /* Radius */
  --ngis-radius-card: var(--token-radius-card);
  --ngis-radius-nested: var(--token-radius-md);
  --ngis-radius-btn: var(--token-radius-md);
  --ngis-radius-pill: var(--token-radius-pill);
}

html[data-theme="dark"],
[data-theme="dark"] {
  --ngis-canvas: #0D1322;
  --ngis-surface: #141D33;
  --ngis-surface-subtle: #0D1322;
  --ngis-surface-translucent: rgba(20, 29, 51, 0.94);
  --ngis-border: rgba(243, 243, 245, 0.14);
  --ngis-border-subtle: rgba(243, 243, 245, 0.08);
  --ngis-border-hover: #202F63;
  --ngis-text-primary: #FFFFFF;
  --ngis-text-secondary: #E5E5E8;
  --ngis-text-muted: #A5A5AA;
  --ngis-text-faint: #77777F;
  --ngis-shadow-card: 0 1px 3px 0 rgba(0, 0, 0, 0.35);
}

/* ── 2. Global Canvas & Typography Reset ─────────────────────── */
html, body {
  background-color: var(--ngis-canvas) !important;
  color: var(--ngis-text-primary) !important;
  font-family: var(--font-primary) !important;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

/* Strict NO BOLD constraint (AGENTS.md) */
*, h1, h2, h3, h4, h5, h6, b, strong, th, td, button, span, div, input, select, textarea {
  font-weight: 400;
}
.font-medium, .stat-val, .badge, th, h1, h2, h3, h4,
.font-bold, .font-semibold, .font-extrabold, .font-black,
[class*="font-semibold"], [class*="font-bold"], [class*="font-extrabold"], [class*="font-black"], [class*="font-medium"] {
  font-weight: 500 !important;
}

/* ── 3. Transparent Background Design ────────────────────────── */
.topbar,
.hero-topbar,
.hero:not(.hero-main):not(:has(.hero-body)),
.hero:not(.hero-main):not(:has(.hero-body)) .hero-topbar,
.hero-subpage,
.hero-transparent,
.page-header,
.main-header,
.app-header,
.filter-toolbar,
.breadcrumb-strip,
.workspace-masthead-transparent,
header.topbar,
header:not(.hero-main):not(:has(.hero-body)),
header[role="banner"],
header[class*="sticky"] {
  background: transparent !important;
  background-color: transparent !important;
  background-image: none !important;
  border: none !important;
  border-bottom: none !important;
  box-shadow: none !important;
  backdrop-filter: none !important;
  -webkit-backdrop-filter: none !important;
}

.hero:not(.hero-main):not(:has(.hero-body)) .hero-topbar::after {
  display: none !important;
  content: none !important;
}

/* ── 4. Premium Content Surfaces & Clean Cards ───────────────── */
.card,
.module-card,
.dept-card,
.hub-card,
.stat-card,
.stat,
.lesson-card,
.ann-card,
.exam-card,
.rc-filecard,
.card-hover,
.card-hover-sm,
.candidate-card,
.club-card,
.cert-card,
.portal-card,
.role-card,
.news-card,
.subj-card,
.cal-card,
.att-card,
.ql-card,
.pf-card,
.ov-profile,
.ov-upcoming,
.ov-deadlines,
.sh-card,
.sh-stat-card,
.sh-request-item,
.task-card,
.quick,
.sk-stat-card,
.box,
.panel,
.widget,
.demo-pill,
[class~="card"],
[class*="card"]:not([class*="-title"]):not([class*="-body"]):not([class*="-desc"]):not([class*="-head"]):not([class*="-footer"]):not([class*="-icon"]):not([class*="-badge"]):not([class*="-action"]):not([class*="-text"]):not([class*="-inner"]):not([class*="-content"]):not([class*="-row"]):not([class*="-chevron"]):not([class*="-top"]):not([class*="-bottom"]):not([class*="-meta"]):not([class*="-sub"]):not([class*="-pad"]):not([class*="-grid"]):not([class*="-wrap"]):not([class*="-list"]):not([class*="-name"]):not([class*="-val"]):not([class*="-label"]):not([class*="-btn"]):not([class*="-link"]) {
  background: var(--ngis-surface) !important;
  background-color: var(--ngis-surface) !important;
  border: 1px solid var(--ngis-border) !important;
  border-radius: var(--ngis-radius-card) !important;
  box-shadow: var(--ngis-shadow-card) !important;
  transition: border-color 0.15s ease !important;
}

/* ── 5. STRICT: Zero Colored Hover Overlays & No Jumps ───────── */
.card:hover,
.module-card:hover,
.dept-card:hover,
.hub-card:hover,
.stat-card:hover,
.stat:hover,
.lesson-card:hover,
.ann-card:hover,
.exam-card:hover,
.rc-filecard:hover,
.card-hover:hover,
.card-hover-sm:hover,
.candidate-card:hover,
.club-card:hover,
.cert-card:hover,
.portal-card:hover,
.role-card:hover,
.news-card:hover,
.subj-card:hover,
.cal-card:hover,
.att-card:hover,
.ql-card:hover,
.pf-card:hover,
.ov-profile:hover,
.ov-upcoming:hover,
.ov-deadlines:hover,
.sh-card:hover,
.sh-stat-card:hover,
.sh-request-item:hover,
.task-card:hover,
.quick:hover,
.sk-stat-card:hover,
.box:hover,
.panel:hover,
.widget:hover,
.demo-pill:hover,
[class~="card"]:hover,
[class*="card"]:not([class*="-title"]):not([class*="-body"]):not([class*="-desc"]):not([class*="-head"]):not([class*="-footer"]):not([class*="-icon"]):not([class*="-badge"]):not([class*="-action"]):not([class*="-text"]):not([class*="-inner"]):not([class*="-content"]):not([class*="-row"]):not([class*="-chevron"]):not([class*="-top"]):not([class*="-bottom"]):not([class*="-meta"]):not([class*="-sub"]):not([class*="-pad"]):not([class*="-grid"]):not([class*="-wrap"]):not([class*="-list"]):not([class*="-name"]):not([class*="-val"]):not([class*="-label"]):not([class*="-btn"]):not([class*="-link"]):hover {
  background: var(--ngis-surface) !important;
  background-color: var(--ngis-surface) !important;
  border-color: var(--ngis-border-hover) !important;
  box-shadow: var(--ngis-shadow-card) !important;
  transform: none !important;
  translate: none !important;
  scale: 1 !important;
}

/* Interactive clickable buttons & links: no lifting, no bouncing */
a[href]:hover,
button:not(:disabled):hover,
[role="button"]:hover,
[onclick]:hover,
.btn:hover,
.btn-primary:hover,
.btn-ghost:hover,
.btn-soft:hover,
.icon-btn:hover {
  transform: none !important;
  translate: none !important;
  scale: 1 !important;
}

/* Table rows: clean neutral background on hover */
table tbody tr:hover td,
.tbl tbody tr:hover td,
.sk-table tr:hover td,
.class-table tbody tr:hover td,
.news-tbl tr:hover td,
.req-table tbody tr:hover td {
  background-color: var(--ngis-canvas) !important;
  transform: none !important;
}

/* ── 6. Top Search Capsule & Navigation Bar ──────────────────── */
.htb-search-wrap {
  background: #FFFFFF !important;
  border: 1px solid var(--ngis-border) !important;
  border-radius: 999px !important;
  box-shadow: none !important;
  transition: border-color 0.15s ease !important;
}
.htb-search-wrap:hover {
  border-color: var(--color-navy) !important;
  background: #FFFFFF !important;
  box-shadow: none !important;
}
.htb-search-wrap:focus-within {
  border-color: var(--color-navy) !important;
  background: #FFFFFF !important;
  box-shadow: 0 0 0 2px rgba(32, 47, 99, 0.20) !important;
}

/* Absolute zero inner box / zero border for search input across all selectors */
html body .htb-search-wrap input,
html body .htb-search-wrap input[type="search"],
html body .htb-search-input,
html body #htbSearchInput,
html body [role="search"] input,
html body .htb-search-wrap input:hover,
html body .htb-search-wrap input:focus,
html body .htb-search-wrap input:active,
html body .htb-search-input:hover,
html body .htb-search-input:focus,
html body .htb-search-input:active,
html body #htbSearchInput:hover,
html body #htbSearchInput:focus,
html body #htbSearchInput:active {
  border: none !important;
  border-width: 0 !important;
  border-style: none !important;
  border-color: transparent !important;
  outline: none !important;
  box-shadow: none !important;
  background: transparent !important;
  background-color: transparent !important;
  border-radius: 0 !important;
  padding: 0 !important;
  margin: 0 !important;
  -webkit-appearance: none !important;
  appearance: none !important;
}

.hero.hero-main .htb-search-wrap,
.hero:has(.hero-body) .htb-search-wrap {
  background: rgba(255, 255, 255, 0.18) !important;
  border: 1px solid rgba(255, 255, 255, 0.3) !important;
}
.hero.hero-main .htb-search-wrap:focus-within,
.hero:has(.hero-body) .htb-search-wrap:focus-within {
  background: rgba(255, 255, 255, 0.28) !important;
  border-color: rgba(255, 255, 255, 0.6) !important;
}

/* ── 7. Transparent Containers & Continuous Flow ─────────────── */
.demo-strip {
  background: transparent !important;
  border: none !important;
  box-shadow: none !important;
  padding: 0 !important;
}
.demo-pill {
  background: #FFFFFF !important;
  border: 1px solid var(--ngis-border) !important;
  border-radius: 14px !important;
}
.demo-pill:hover {
  background: #FFFFFF !important;
  border-color: var(--color-navy) !important;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05) !important;
}

/* Modal Evaluation Drawer stacking above mobile navigation */
#scoringDrawer {
  z-index: 95 !important;
}
body:has(#scoringDrawer:not(.translate-x-full)) .mob-bottomnav {
  transform: translateX(-50%) translateY(calc(100% + 48px)) scale(0.88) !important;
  opacity: 0 !important;
  pointer-events: none !important;
}
"""

with open("assets/css/design-system.css", "w", encoding="utf-8") as f:
    f.write(design_system_css)

print("Updated assets/css/design-system.css successfully!")


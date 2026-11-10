import os

content = """@import url('design-tokens.css');
@import url('shared-components.css');

/* ============================================================
   NGIS ERP — Master Global Design System & Visual Style
   Official Forest Green + Clean White + Warm Orange Design System:
   - Forest Green: #176B45 (Primary brand color, sidebar, primary buttons, active navigation)
   - Pure White:   #FFFFFF (Main content surfaces, cards, tables, forms, modals)
   - Warm Orange:  #F28C28 (Important actions, notifications, small highlights)
   - Soft Mint:    #E8F3ED (Selected navigation backgrounds, subtle sections, icon backgrounds)
   - Off White:    #F7F9F7 (Main application workspace background)
   - Dark Charcoal:#29352E (Headings, primary text, body text)

   Supporting Structural Colors:
   - Subtle Border:#E1E9E3 (Subtle green-gray hairline borders & dividers)
   - Text Muted:   #64746A (Muted supporting descriptions & subtitles)
   - Primary Hover:#125638 (Dark forest green for button hover)

   Strict Rules:
   - Primary Font for Headings: Manrope (font-weight <= 500 per AGENTS.md, H1 exactly 28px)
   - General Interface Font: Plus Jakarta Sans (font-weight 400 or 500)
   - Continuous Canvas: var(--color-background, #F7F9F7)
   - Content Surfaces: #FFFFFF with 1px solid #E1E9E3 border & 12px radius
   - Strictly ZERO colored hover overlays, ZERO lifting, ZERO scaling
   ============================================================ */

/* ── 1. Universal Design Tokens ──────────────────────────────── */
:root {
  /* Typography */
  --font-primary: 'Plus Jakarta Sans', 'Inter', -apple-system, sans-serif;
  --font-heading: 'Manrope', 'Plus Jakarta Sans', sans-serif;
  --font-khmer:   'Kantumruy Pro', 'Manrope', sans-serif;
  --font-mono:    ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;

  /* Neutral Surface Palette */
  --ngis-canvas:              var(--color-background, #F7F9F7);
  --ngis-surface:             #FFFFFF;
  --ngis-surface-subtle:      var(--color-mint, #E8F3ED);
  --ngis-surface-translucent: rgba(255, 255, 255, 0.96);

  /* Borders & Outlines */
  --ngis-border:        var(--color-border, #E1E9E3);
  --ngis-border-subtle: #EEF4F0;
  --ngis-border-hover:  var(--color-primary, #176B45);

  /* Typography Colors */
  --ngis-text-primary:   var(--color-text, #29352E);
  --ngis-text-secondary: var(--color-text-secondary, #64746A);
  --ngis-text-muted:     var(--color-text-muted, #8FA095);
  --ngis-text-faint:     #A5B4AA;

  /* Brand Accents */
  --ngis-brand-deep:     var(--color-primary, #176B45);
  --ngis-brand-hover:    var(--color-primary-hover, #125638);
  --ngis-brand-steel:    var(--color-accent, #F28C28);
  --ngis-brand-light:    var(--color-mint, #E8F3ED);

  /* Minimal Shadows */
  --ngis-shadow-card:  0 1px 3px 0 rgba(23, 107, 69, 0.04);
  --ngis-shadow-float: 0 8px 24px -4px rgba(23, 107, 69, 0.12);
  --ngis-shadow-none:  none;

  /* Radius */
  --ngis-radius-card:   12px;
  --ngis-radius-nested: 8px;
  --ngis-radius-btn:    8px;
  --ngis-radius-pill:   9999px;
}

html[data-theme="dark"],
[data-theme="dark"] {
  --ngis-canvas:              #101713;
  --ngis-surface:             #18231D;
  --ngis-surface-subtle:      #1F2E26;
  --ngis-surface-translucent: rgba(24, 35, 29, 0.94);
  --ngis-border:              rgba(225, 233, 227, 0.15);
  --ngis-border-subtle:       rgba(225, 233, 227, 0.08);
  --ngis-border-hover:        #176B45;
  --ngis-text-primary:        #FFFFFF;
  --ngis-text-secondary:      #E8F3ED;
  --ngis-text-muted:          #8FA095;
  --ngis-text-faint:          #64746A;
  --ngis-shadow-card:         0 1px 3px 0 rgba(0, 0, 0, 0.4);
}

/* ── 2. Global Canvas & Typography Reset ─────────────────────── */
html, body {
  background-color: var(--ngis-canvas) !important;
  color: var(--ngis-text-primary) !important;
  font-family: var(--font-primary) !important;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

/* Typography Weight Rules (AGENTS.md: NO BOLD FONTS) */
*, b, strong, th, td, button, span, div, input, select, textarea, p, label, a {
  font-weight: 400;
}

/* Medium weight (500) for interactive controls, badges, table headers, labels */
.font-medium, .stat-val, .badge, th, .btn, .nav-link, .nav-group-label,
.font-semibold, .font-bold, .font-extrabold, .font-black,
[class*="font-semibold"], [class*="font-bold"], [class*="font-extrabold"], [class*="font-black"], [class*="font-medium"] {
  font-weight: 500;
}

/* Page titles: Manrope 500, H1 exactly 28px */
h1, .page-title, .dash-hero-title, [data-purpose="page-title"], .masthead-title {
  font-family: 'Manrope', sans-serif !important;
  font-weight: 500 !important;
  font-size: 28px !important;
  color: var(--color-text, #29352E) !important;
  letter-spacing: -0.02em;
}

h2, h3, .section-title, [data-purpose="section-title"] {
  font-family: 'Manrope', sans-serif !important;
  font-weight: 500 !important;
  color: var(--color-text, #29352E) !important;
}

/* Khmer Text Font */
[lang="km"], [data-lang="km"], .font-khmer, .khmer-text {
  font-family: 'Kantumruy Pro', 'Manrope', sans-serif !important;
}

/* Supporting Interface Elements */
.supporting-ui, .pill, .meta-text, .tag, .stat-lbl, .breadcrumb-item {
  font-family: 'Plus Jakarta Sans', 'Inter', sans-serif;
  color: var(--color-text-secondary, #64746A);
}

/* ── Universal Primary Button Engine (Forest Green #176B45 + White #FFFFFF) ── */
.btn-primary,
.ngis-btn-primary,
.ov-btn-main,
.tp-btn-primary,
.art-btn-primary,
.sk-blue-btn,
button.btn-primary,
a.btn-primary,
[data-role-action="primary"],
.sh-toolbar-new-btn,
.sh-new-request-btn,
#btnUploadAssignmentOrWork,
#btnAddStudent,
#btnAddClass,
#saveChangesBtn,
#openUploadBtn,
#btnPrimaryAddCourse,
#btnSubmitUpload,
#btnSubmitRequest {
  background: var(--color-primary, #176B45) !important;
  background-color: var(--color-primary, #176B45) !important;
  color: #FFFFFF !important;
  border: 1px solid var(--color-primary, #176B45) !important;
  box-shadow: 0 1px 2px 0 rgba(23, 107, 69, 0.20) !important;
  border-radius: 8px !important;
  font-weight: 500 !important;
  transition: all 0.15s ease !important;
}

.btn-primary:hover,
.ngis-btn-primary:hover,
.ov-btn-main:hover,
.tp-btn-primary:hover,
.art-btn-primary:hover,
.sk-blue-btn:hover,
button.btn-primary:hover,
a.btn-primary:hover,
[data-role-action="primary"]:hover,
.sh-toolbar-new-btn:hover,
.sh-new-request-btn:hover,
#btnUploadAssignmentOrWork:hover,
#btnAddStudent:hover,
#btnAddClass:hover,
#saveChangesBtn:hover,
#openUploadBtn:hover,
#btnPrimaryAddCourse:hover,
#btnSubmitUpload:hover,
#btnSubmitRequest:hover {
  background: var(--color-primary-hover, #125638) !important;
  background-color: var(--color-primary-hover, #125638) !important;
  border-color: var(--color-primary-hover, #125638) !important;
  color: #FFFFFF !important;
  box-shadow: 0 2px 5px 0 rgba(18, 86, 56, 0.28) !important;
  transform: none !important;
}

.btn-primary *,
.ngis-btn-primary *,
.ov-btn-main *,
.tp-btn-primary *,
.art-btn-primary *,
.sk-blue-btn *,
button.btn-primary *,
a.btn-primary *,
[data-role-action="primary"] *,
.sh-toolbar-new-btn *,
.sh-new-request-btn *,
#btnUploadAssignmentOrWork * {
  color: #FFFFFF !important;
}

/* Secondary Buttons (White with Forest Green text & subtle border) */
.btn-secondary,
.btn-neutral,
button.btn-secondary,
a.btn-secondary {
  background: #FFFFFF !important;
  background-color: #FFFFFF !important;
  color: var(--color-primary, #176B45) !important;
  border: 1px solid var(--color-border, #E1E9E3) !important;
  border-radius: 8px !important;
  font-weight: 500 !important;
  transition: all 0.15s ease !important;
}
.btn-secondary:hover,
.btn-neutral:hover,
button.btn-secondary:hover,
a.btn-secondary:hover {
  background: var(--color-mint, #E8F3ED) !important;
  border-color: var(--color-primary, #176B45) !important;
  color: var(--color-primary, #176B45) !important;
  transform: none !important;
}

/* Accent Buttons (Warm Orange #F28C28 with White #FFFFFF text) */
.btn-accent,
.ngis-btn-accent,
.btn-orange,
button.btn-accent,
a.btn-accent {
  background: var(--color-accent, #F28C28) !important;
  background-color: var(--color-accent, #F28C28) !important;
  color: #FFFFFF !important;
  border: 1px solid var(--color-accent, #F28C28) !important;
  border-radius: 8px !important;
  font-weight: 500 !important;
  transition: all 0.15s ease !important;
}
.btn-accent:hover,
.ngis-btn-accent:hover,
.btn-orange:hover,
button.btn-accent:hover,
a.btn-accent:hover {
  background: var(--color-accent-hover, #D9771A) !important;
  background-color: var(--color-accent-hover, #D9771A) !important;
  border-color: var(--color-accent-hover, #D9771A) !important;
  color: #FFFFFF !important;
  transform: none !important;
}

/* Soft Action Buttons (#E8F3ED with #176B45 text) */
.btn-soft,
.btn-accent-soft,
button.btn-soft {
  background: var(--color-mint, #E8F3ED) !important;
  background-color: var(--color-mint, #E8F3ED) !important;
  color: var(--color-primary, #176B45) !important;
  border: 1px solid transparent !important;
  border-radius: 8px !important;
  font-weight: 500 !important;
}
.btn-soft:hover,
.btn-accent-soft:hover,
button.btn-soft:hover {
  background: #D8EADF !important;
  color: var(--color-primary-hover, #125638) !important;
  transform: none !important;
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
.mgr-card,
.dash-card,
.telemetry-card {
  background: #FFFFFF !important;
  background-color: #FFFFFF !important;
  border: 1px solid var(--color-border, #E1E9E3) !important;
  border-radius: 12px !important;
  box-shadow: 0 1px 3px 0 rgba(23, 107, 69, 0.03) !important;
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
.mgr-card:hover,
.dash-card:hover,
.telemetry-card:hover {
  background: #FFFFFF !important;
  background-color: #FFFFFF !important;
  border-color: var(--color-border, #E1E9E3) !important;
  box-shadow: 0 1px 3px 0 rgba(23, 107, 69, 0.03) !important;
  transform: none !important;
  translate: none !important;
  scale: 1 !important;
}

/* Interactive clickable buttons: no lifting, no bouncing */
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

/* Table rows styling */
table, .tbl, .sk-table, .class-table, .classes-table, .mgr-table {
  background-color: #FFFFFF !important;
  border-collapse: separate !important;
  border-spacing: 0 !important;
  border: 1px solid var(--color-border, #E1E9E3) !important;
  border-radius: 12px !important;
  overflow: hidden !important;
}

thead tr, thead th {
  background-color: var(--color-mint, #E8F3ED) !important;
  color: var(--color-text, #29352E) !important;
  border-bottom: 1px solid var(--color-border, #E1E9E3) !important;
  font-weight: 500 !important;
  font-size: 11px !important;
  text-transform: uppercase !important;
  letter-spacing: 0.04em !important;
}

tbody tr td {
  border-bottom: 1px solid var(--color-border, #E1E9E3) !important;
  color: var(--color-text, #29352E) !important;
}

tbody tr:last-child td {
  border-bottom: none !important;
}

tbody tr:hover td {
  background-color: #FAFDFB !important;
}

/* Form Inputs & Controls */
input:not([type="checkbox"]):not([type="radio"]):not([type="hidden"]),
select,
textarea {
  background-color: #FFFFFF !important;
  border: 1px solid var(--color-border, #E1E9E3) !important;
  color: var(--color-text, #29352E) !important;
  border-radius: 8px !important;
}

input:focus,
select:focus,
textarea:focus {
  border-color: var(--color-primary, #176B45) !important;
  outline: none !important;
  box-shadow: 0 0 0 2px rgba(23, 107, 69, 0.18) !important;
}

input::placeholder,
select::placeholder,
textarea::placeholder {
  color: #8FA095 !important;
}

/* ── 6. Mobile Hamburger Menu Button ─────────────────────────── */
@media (min-width: 1025px) {
  .hamburger-btn,
  .mobile-hamburger-btn,
  .htb-hamburger,
  #htbHamburger,
  .menu-btn,
  #menuBtn,
  [data-action="toggle-sidebar"]:not(#sidebarCollapseBtn):not(#sidebarExpandBtn) {
    display: none !important;
    visibility: hidden !important;
    opacity: 0 !important;
    pointer-events: none !important;
  }
}

@media (max-width: 1024px) {
  .hamburger-btn,
  .mobile-hamburger-btn,
  .htb-hamburger,
  #htbHamburger,
  .menu-btn,
  #menuBtn,
  [data-action="toggle-sidebar"]:not(#sidebarCollapseBtn):not(#sidebarExpandBtn) {
    display: inline-flex !important;
    visibility: visible !important;
    opacity: 1 !important;
    order: -9999 !important;
  }
}

/* ── 7. Golden Reference Telemetry Card ──────────────────────── */
.telemetry-card {
  background-color: #FFFFFF !important;
  border: 1px solid var(--color-border, #E1E9E3) !important;
  border-radius: 12px !important;
  padding: 1.25rem !important;
  display: flex !important;
  flex-direction: column !important;
  justify-content: space-between !important;
  box-shadow: 0 1px 3px rgba(23, 107, 69, 0.03) !important;
  transform: none !important;
  transition: none !important;
  position: relative;
}

.telemetry-card:hover {
  background-color: #FFFFFF !important;
  box-shadow: 0 1px 3px rgba(23, 107, 69, 0.03) !important;
  transform: none !important;
}

/* Telemetry Card Typography & Accents */
.telemetry-card .stat-val,
.telemetry-card [id^="kpi"] {
  color: var(--color-text, #29352E) !important;
  font-family: 'Manrope', sans-serif !important;
  font-weight: 500 !important;
}

.telemetry-card span.uppercase {
  color: var(--color-text-secondary, #64746A) !important;
}

/* Icon containers in telemetry cards */
.telemetry-card .w-10.h-10 {
  background-color: var(--color-mint, #E8F3ED) !important;
  color: var(--color-primary, #176B45) !important;
  border-radius: 10px !important;
}

.telemetry-pill {
  padding: 0.5rem 0.625rem !important;
  background-color: var(--color-mint, #E8F3ED) !important;
  border: 1px solid var(--color-border, #E1E9E3) !important;
  border-radius: 8px !important;
  display: flex !important;
  align-items: center !important;
  gap: 0.5rem !important;
  font-size: 0.75rem !important;
  line-height: 1rem !important;
  color: var(--color-text-secondary, #64746A) !important;
}

.telemetry-pill .material-symbols-outlined {
  color: var(--color-primary, #176B45) !important;
}

/* ── 8. Universal Search & Filter Input Padding ───────────────── */
.search-input-with-icon,
[data-purpose="filtering-controls"] input[type="text"],
[data-purpose="filtering-controls"] input[type="search"],
.filter-bar input[type="text"],
.filter-bar input[type="search"],
.classes-search-input {
  padding-left: 44px !important;
}

[data-purpose="filtering-controls"] select,
.filter-bar select,
.filter-select,
.select-filter {
  width: auto !important;
  max-width: 100% !important;
  display: inline-block !important;
}
"""

with open('assets/css/design-system.css', 'w', encoding='utf-8') as f:
    f.write(content)
print('Successfully written assets/css/design-system.css')


# Master Prompt: Build NGIS School Management System with Tabler UI Kit (All Elements)

> **Customized for:** NGIS School Management System (Next Generation Information System)  
> **Theme:** Light Mode Only (Dark mode removed)  
> **Design Skills Applied:** `ui-ux-pro-max`, `ux-skill`, `motion-design`, and `AGENTS.md` (Strict "NO BOLD FONTS" & Mandatory Mobile Hamburger Navigation)

---

## The Prompt

You are a senior front-end engineer and UI/UX designer. Build the MVP of **NGIS (Next Generation Information System)**: an institutional, enterprise-grade K-12 school management, academic governance, and student analytics platform for **Principals, Academic Deans, Teachers, Registrars, Students, and Parents** using the Tabler admin UI kit (Bootstrap 5 based, version 1.7.1) customized to the NGIS design system.

### Screens to build (MVP only):
1. **Executive Principal Governance & Telemetry Dashboard** (`pages/principal/principal.html`) — High-level academic KPI telemetry, pending grade authorizations, student attendance rate, faculty load, real-time activity stream, and quick-action modals.
2. **Academic Verification & Attendance Roster Directory** (`pages/principal/principal-attendance.html` / `teacher-roster.html`) — Dense, responsive data table with sticky student name columns, status badges, attendance audit trails, and **SVG icon-only row action buttons**.
3. **Curriculum, Department & Timetable Configuration** (`pages/principal/principal-departments.html` / `principal-timetables.html`) — Department division cards, syllabi breakdown, weekly timetable matrix editor with period configuration forms and OCR scan review.
4. **Institutional Single Sign-On & Identity Authentication Gate** (`login.html` / `student-id.html`) — Role-based institutional sign-in with clean card layout, password visibility toggle, student/faculty badge barcode display, and credential validation feedback.

**Source of truth:** Reproduce the markup patterns, class names, and responsive behavior of the Tabler "All Elements" page for every component below, customized strictly for NGIS. Build reusable components or partials for each, and use them on every screen. Replace all demo text with realistic NGIS academic content.

---

### 1. Setup and Assets
- **Tabler Assets**: Install `@tabler/core` (v1.7.1) and load `tabler.min.css`, followed by `tabler-vendors.min.css` where required.
- **LIGHT MODE ENFORCEMENT**: **DO NOT load `tabler-theme.min.js` or any dark-mode stylesheets.** The application is strictly locked to crisp, institutional light mode (`data-bs-theme="light"` on `<html>`).
- **Load Scripts**: Load `tabler.min.js` with `defer` at the end of `<body>`.
- **Plugins**: 
  - `Tom Select` (`tom-select.complete.min.js` & CSS) for cohort/course multi-select dropdowns.
  - `noUiSlider` (`nouislider.min.js` & CSS) for grade range and GPA filter sliders.
  - `star-rating.js` for teacher peer reviews and service ratings.
  Load plugin CSS and JS only on pages that use them.
- **Icons**: Inline SVG icons (Tabler Icons or Phosphor Icons): `20px` to `24px`, `stroke="currentColor"`, `stroke-width="1.8"`, round caps and joins, class="icon", with `aria-hidden="true"` and `focusable="false"`.
- **Typography & Font Pairing**:
  - Primary font: **Plus Jakarta Sans** (headings, UI elements, navigation).
  - Secondary font: **Inter** (body text, descriptions, table data).
  - Monospace font: **JetBrains Mono** (student IDs, timestamps, room numbers, course codes).
  - **CRITICAL REPOSITORY RULE (NO BOLD FONTS)**: Do **NOT** use bold, extrabold, or black font weights (`font-bold`, `font-extrabold`, `font-black`, `font-weight: 700`, `font-weight: 800`). Headings, titles, badges, and numbers must use `font-medium` (`font-weight: 500`) or `font-normal` (`font-weight: 400`). Keep `<b>` and `<strong>` subtle at maximum `500` weight.
- **Required Head Tags**: UTF-8 charset, viewport with `viewport-fit=cover`, title, description, favicon.
- **Skip Link**: Include `<a href="#content" class="visually-hidden-focusable skip-link">Skip to main content</a>` as the first element inside `<body>`.

---

### 2. App Shell and Layout
Structure: `.page > navigation > .page-wrapper > main#content > .page-header + .page-body > .container-xl > .row.row-cards > footer.footer`.

#### A. Vertical Sidebar (`aside.navbar.navbar-vertical.navbar-expand-lg`)
- **CRITICAL RULE (MANDATORY MOBILE HAMBURGER MENU)**:
  - Every mobile responsive view (screen width $\le 1024\text{px}$) MUST include an accessible, visible hamburger button:
    `<button type="button" class="hamburger-btn" data-action="toggle-sidebar" aria-label="Open menu" aria-expanded="false" title="Open navigation"><i class="ph ph-list text-xl"></i></button>`.
  - Minimum touch target: `44×44px` with smooth active touch feedback (`active:scale-95`).
- **Brand Logo**: NGIS institutional crest / wordmark SVG with theme variable `--primary` (`#176B45` Forest Green).
- **Navigation Sections (`nav-section-title`)**:
  - *Academic Governance*: Overview, Classes & Cohorts, Academic Departments, Master Timetables.
  - *Faculty & Students*: Teacher Profiles, Student Dossiers, Attendance & Verification, Grade Release.
  - *Institutional Services*: Facilities & Maintenance, Lost & Found, Campus News & Alerts.
- **Sidebar Footer User Card**: Avatar, Name ("Dr. Aris Thorne"), Role ("Principal · Admin"), live indicator badge ("Active AY 2024-25"), and Customize trigger button.

#### B. Top Header Navbar (`header.navbar.navbar-expand-md`)
- Mobile hamburger toggler, NGIS Brand logo, primary action button (`+ New Academic Entry`), notifications dropdown, language selector (`EN` / `KM`), and user menu.
- **NO DARK MODE TOGGLE**: Do not include moon/sun buttons or dark mode theme selectors.

#### C. User Menu
- Avatar with initials/photo, Name, and Role.
- Dropdown items: Profile Settings, Academic Governance Dossier, Security & Audit Logs, divider, Institutional Help, Sign Out.

#### D. Notifications Dropdown
- Bell SVG icon with red unread counter badge.
- Header card with "Academic Alerts" and unread count.
- Hoverable list group: animated status pulse dot for unread, title, timestamp, truncated details (e.g. *"Grade 11B Attendance anomaly flagged"*, *"Term 2 Grade Release awaiting sign-off"*).
- Footer with "Mark all as read" and "View all notifications".

#### E. Institutional Apps Menu
- Grid SVG icon opening a 3-column quick-switch drawer:
  1. Student Hub
  2. Teacher Gradebook
  3. Principal Governance
  4. Registrar Admin
  5. Timetable Engine
  6. Campus Facilities

#### F. Language Selector
- `EN` (English) and `KM` (Khmer / ភាសាខ្មែរ) with `data-lang` attributes, wired to interface strings.

#### G. Page Header & Breadcrumbs
- Standard header pattern on every page:
  `.page-header.d-print-none > .container-xl > .row.g-2.align-items-center`.
  - Left column: breadcrumb navigation, followed by `h1.page-title` (weight: `500`), and single-line description `div.text-secondary.mt-1`.
  - Right column (`col-auto ms-auto`): primary action button or secondary documentation link with external-link icon.

#### H. Layout Variants Supported:
- Boxed (`layout-boxed`), Fluid (`layout-fluid`), Vertical sidebar (default attached), Folded compact sidebar (`navbar-vertical-folded`), and RTL mode.

---

### 3. Theme & Customization Panel (Light Mode Only)
Build the "Customize Interface" offcanvas (`offcanvas-start offcanvas-floating`) with an institutional header, floating brush button, and Save/Reset buttons:
- **Appearance (Light Palettes Only — No Dark Mode)**:
  - Base Tone: Pure Institutional White, Slate Neutral (`#F8FAFC`), Soft Mist (`#F1F5F9`), Warm Stone (`#FAFAF9`).
  - Accent Color: NGIS Forest Green (`#176B45` - Default), Royal Emerald (`#059669`), Scholastic Azure (`#0284C7`), Deep Indigo (`#4338CA`), Amber Gold (`#D97706`).
  - Corner Radius Scale: `0` (Sharp), `0.375rem` (6px - Compact), `0.5rem` (8px - Default), `0.75rem` (12px - Modern).
- **Layout Configuration**:
  - Navigation Position: Sidebar or Top Navbar.
  - Container Width: Default (`container-xl`), Fluid (`container-fluid`), or Boxed.
  - Sidebar Behavior: Expanded, Folded, or Fold on Hover.
- **Persistence Rules**:
  - Settings stored in `localStorage` under `ngis-<key>` and reflected on `<html>` as `data-bs-<key>` attributes.
  - Settings mirrored to URL search parameters for link sharing; Reset button clears stored settings and dispatches `window.dispatchEvent(new Event('resize'))`.

---

### 4. Component Library (Complete NGIS Design Specification)

#### A. Typography (Strict No-Bold Constraint)
- Headings: `h1` (`24px`), `h2` (`20px`), `h3` (`16px`), `h4` (`14px`), `h5` (`12px`), `h6` (`11px`) — all using `font-weight: 500` or `400`. Never `700` or `800`.
- Body copy: `14px` (line-height: `1.5`), muted captions: `12px` (`text-slate-500`), code/IDs: `font-mono` (`JetBrains Mono`).

#### B. Buttons & **CRITICAL Table Row Action Icons**
- Button variants: Primary (`#176B45`), Secondary (neutral slate outline), Success (`#10B981`), Warning (`#F59E0B`), Danger (`#EF4444`).
- Sizes: Small (`btn-sm`), Default, Large (`btn-lg`).
- **CRITICAL RULE (TABLE ROW ACTIONS ARE SVG ICONS ONLY)**:
  - Action buttons inside table rows must be **SVG ICONS ONLY**.
  - **Zero visible text words** inside row action buttons (NO words like `Authorize`, `Review`, `Return`, `Edit`, `Delete`, `Approve`, `View`).
  - Standard `.action-icon-btn` format: 34×34px compact icon button with subtle border, smooth hover/focus state, and mandatory `title="..."` and `aria-label="..."`.
  - Standard icon assignments:
    - Approve / Authorize $\rightarrow$ Check SVG icon (`action-icon-btn primary`).
    - View / Review / Inspect $\rightarrow$ Eye SVG icon (`action-icon-btn`).
    - Return / Undo / Revise $\rightarrow$ Return arrow SVG icon (`action-icon-btn danger`).
    - Edit / Modify $\rightarrow$ Pencil SVG icon (`action-icon-btn`).
    - Delete / Purge $\rightarrow$ Trash can SVG icon (`action-icon-btn danger`).
    - Contact / Phone $\rightarrow$ Phone SVG icon (`action-icon-btn danger`).

#### C. Cards & Metrics
- Metric Cards: KPI title (`text-slate-500 text-xs font-medium`), large metric value (`text-2xl font-medium text-slate-900`), change indicator badge (`+3.2% vs Q1`), and mini sparkline.
- Container Card: `card` with `card-header` (containing `card-title` and `card-actions`), `card-body`, and `card-footer`.

#### D. Alerts (All 4 Semantic Types, Fully Reusable)
Variants in Success (`#10B981`), Info (`#0284C7`), Warning (`#F59E0B`), and Danger (`#EF4444`):
1. **Basic**: Alert icon + concise notification message.
2. **With Action**: Alert message + actionable inline button link (e.g. *"Resolve Conflict"*).
3. **Dismissible**: Alert message + `<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>`.
4. **With Description**: Alert heading (`h3.alert-heading font-medium`), descriptive paragraph, and bulleted guideline list.
5. **Minor**: Subdued inline callout for contextual notes inside forms and sidebars.

#### E. Badges, Status Dots & Ribbons
- Soft Pill Badges: `bg-primary-lt`, `bg-success-lt`, `bg-warning-lt`, `bg-danger-lt` (maximum `font-medium`).
- Status Dots: Green (`Active` / `Present`), Yellow (`Late` / `Pending Review`), Red (`Absent` / `Suspended`), with animated pulse ring on live items. Screen-reader hidden text included.

#### F. Forms & Academic Inputs
- Inputs: Text, Email, Password (with toggleable show/hide eye icon), Datepicker.
- Tom Select: Multi-select tags for student cohorts, class assignees, and subject tags.
- Range Slider: `noUiSlider` for score ranges (0–100%) and GPA filters (0.0–4.0).
- Toggle switch, inline radio groups, character-counter textareas, and field-level validation error messages (`is-invalid` with `invalid-feedback`).

#### G. Data Tables (High-Density Academic Roster)
- Structure: `.table-responsive` wrapping `table.table.table-vcenter.card-table`.
- Sticky Freeze Column: Leftmost student name/ID column remains fixed during horizontal table scrolling.
- Compact cell padding (`py-2.5 px-3`), zebra striping or subtle borders (`border-slate-100`), sortable column headers with SVG arrow indicators.
- Rightmost Actions Column (`th.text-end` / `td.table-actions`): houses the standardized **SVG icon-only action group**.

#### H. Modals & Overlays
- `modal-blur fade` dialogs: Confirmation modal, Attendance Correction audit modal with reason input, Document preview lightbox, and toast alerts (`toast` with `role="status"`).

#### I. Navigation & Segments
- Segmented control (`nav-segmented`): 4-state switchers (e.g. Day / Week / Month / Term).
- Breadcrumbs with home icon and `aria-current="page"`.
- Clean numbered pagination with Previous/Next icon controls.

#### J. Empty States
- `.empty` container featuring an institutional SVG illustration, `p.empty-title` (`font-medium`), `p.empty-subtitle`, and primary action button (e.g. *"Create First Cohort"*).

---

### 5. Accessibility & UX Intelligence Guidelines (`ui-ux-pro-max` & `ux-skill`)
- **Contrast**: Maintain minimum 4.5:1 contrast for normal text and 3:1 for large headings (WCAG 2.1 AA compliant).
- **Touch Ergonomics**: All interactive elements (buttons, inputs, tabs, hamburger toggles) must meet minimum `44×44px` touch target bounding boxes on mobile screens.
- **Zero Horizontal Blowout**: No element shall cause horizontal page-body scroll on mobile viewports (`360px`, `390px`, `414px`). Wide tables must scroll within their own dedicated `.table-responsive` container.
- **Screen Reader Support**: All icon-only buttons require `aria-label` or `title`; decorative SVGs must carry `aria-hidden="true"`.
- **Anti-AI-Slop Rules**:
  - No generic centered marketing hero banners on internal administrative pages.
  - No purple neon gradient blobs or low-contrast gray-on-gray body text.
  - No heavy 700/800 font weights anywhere in the interface.

---

### 6. What Not to Include
- **DO NOT include Dark Mode**, dark theme classes, dark nav stylesheets, or theme toggle switches.
- **DO NOT include third-party tracking/analytics scripts** (e.g. PostHog, Google Analytics tags).
- **DO NOT include dummy Latin filler** (`Lorem Ipsum`). Use realistic academic and institutional terms (e.g., *"Grade 11-A Advanced Mathematics"*, *"Dean of Academic Affairs"*, *"Quarterly Cumulative GPA"*).
- **DO NOT use text labels in table row action buttons**. Keep them strictly SVG icon-only.

---

### 7. Design System Tokens (CSS Variables)

```css
:root {
  /* Brand Institutional Palette (Light Mode) */
  --tblr-primary: #176B45;            /* NGIS Forest Green */
  --tblr-primary-rgb: 23, 107, 69;
  --tblr-primary-fg: #FFFFFF;
  --tblr-primary-lt: #E8F5E9;
  
  --tblr-secondary: #475569;          /* Slate 600 */
  --tblr-body-bg: #F8FAFC;            /* Slate 50 */
  --tblr-body-color: #0F172A;         /* Slate 900 */
  --tblr-card-bg: #FFFFFF;
  --tblr-border-color: #E2E8F0;       /* Slate 200 */
  
  --tblr-success: #10B981;            /* Emerald */
  --tblr-warning: #F59E0B;            /* Amber */
  --tblr-danger: #EF4444;             /* Rose Red */
  --tblr-info: #0284C7;               /* Azure Blue */

  /* Typography Weights (Enforce No Bold) */
  --tblr-font-weight-normal: 400;
  --tblr-font-weight-medium: 500;
  --tblr-font-weight-bold: 500;       /* Locked to medium - NO 700/800 */
  --tblr-font-sans-serif: 'Plus Jakarta Sans', 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  --tblr-font-monospace: 'JetBrains Mono', monospace;

  /* Border Radius */
  --tblr-border-radius: 8px;
  --tblr-border-radius-sm: 6px;
  --tblr-border-radius-lg: 12px;
}
```

---

### Build Order
1. **Foundation & Assets**: Set up assets, lock light mode theme, load Plus Jakarta Sans / Inter / JetBrains Mono fonts, and configure the NGIS CSS token variables.
2. **App Shell**: Implement vertical sidebar navigation with the **mandatory mobile hamburger menu button**, top navbar (without dark mode toggle), and footer.
3. **Component Library & `/ui-kit` Page**: Build the living design system page featuring all buttons, alerts, form controls, tables, badges, and modals.
4. **The 4 MVP Screens**: Build the Principal Dashboard, Attendance Roster Table, Curriculum/Department Settings, and Sign-In Gate.
5. **Quality Verification**: Execute accessibility audit, verify icon-only table actions, test mobile responsiveness ($\le 390\text{px}$), and confirm zero font weights above 500.

---

### Acceptance Checklist
- [ ] The app shell functions seamlessly as a vertical sidebar on desktop and collapses into a drawer accessed via the **mandatory mobile hamburger button** (`data-action="toggle-sidebar"`) on mobile.
- [ ] **Dark mode is completely removed**; the interface renders purely in crisp, institutional light mode.
- [ ] **NO BOLD FONTS**: Every heading, title, badge, and label strictly uses `font-weight: 500` or `400`. Zero `700` or `800` weights.
- [ ] **Table row actions are strictly SVG icons only**; no visible words (`Authorize`, `Review`, `Edit`, `Delete`) appear in action columns.
- [ ] Every action button has an accessible `title` and `aria-label`.
- [ ] All 4 Alert variants (basic, with action, dismissible, with description) function in all 4 semantic colors.
- [ ] All form fields have linked labels, clear validation states, and responsive touch targets ($\ge 44\text{px}$).
- [ ] The living `/ui-kit` page showcases every element and passes WCAG 2.1 AA contrast checks.
- [ ] **5 Psychological UX Laws Enforced**:
  - *Jakob's Law:* Conventional authentication layout (Email $\rightarrow$ Password $\rightarrow$ subtle "Forgot password?" link $\rightarrow$ primary "Sign In" button) and standard navigation.
  - *Miller's Law:* Identifiers and codes chunked into $\le 7$ digestible segments (`STU-2024-001`, `+855 12 345 678`).
  - *Peak-End Rule:* Delightful, rewarding confirmation states with green checkmark badges and clear next steps instead of raw receipts.
  - *Aesthetic-Usability Effect:* Polished white cards (`#FFFFFF`), subtle hairline borders (`#E1E9E3`), and high-contrast typography.
  - *Occam's Razor:* Minimal form fields and frictionless single-step actions.


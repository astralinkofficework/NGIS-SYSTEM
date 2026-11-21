# NGIS System Guidelines & Project Rules

## Mobile Responsive Navigation Requirements
> **CRITICAL RULE**: All mobile responsive views and layouts MUST have a hamburger menu button to open the navigation sidebar.

### 1. Mandatory Hamburger Menu on Mobile
- Every mobile view (`*-mobile-view`, mobile app bar, or screen width <= 768px/1024px) across all portals (**Student**, **Teacher**, **Parent**, **Principal**, **Admin**, and **Shared**) MUST include an accessible, visible hamburger menu button.
- When clicked/tapped, this button opens the mobile sidebar drawer.

### 2. Standard Attributes & Selectors
To integrate seamlessly with `assets/js/layout.js`, always include:
- `data-action="toggle-sidebar"`
- Class `hamburger-btn` and/or `mobile-hamburger-btn` (or `htb-hamburger`)
- `aria-label="Open menu"`
- `aria-expanded="false"`
- `title="Open navigation"`

### 3. Iconography & Styling
- **Preferred (system standard)**: Bootstrap Icons list glyph via the shared engine: `<span data-ngis-icon="menu"></span>` (renders official `bi-list`; hydrate with `assets/js/action-icons.js`).
- Equally acceptable (legacy fallbacks): Phosphor `<i class="ph ph-list text-xl"></i>` (or `<i class="ph-bold ph-list text-xl"></i>`) or Material Symbols `<span class="material-symbols-outlined">menu</span>`.
- Ensure a minimum touch target size of 38-44px.
- Use smooth interaction feedback (`active:scale-95` / transition) and ensure theme support (`[data-theme="dark"]`).

## Icon System Requirements
> **STANDARD**: All functional UI icons use **official Bootstrap Icons** (bootstrap-icons v1.13.2, bundled in `node_modules/bootstrap-icons`, baked as SVGs in `assets/js/action-icons.js`).

- Render icons through the shared engine: `NGIS.icon(name)` in JS templates, or `<span data-ngis-icon="name"></span>` in HTML.
- Legacy Material Symbols / Phosphor glyphs may remain as graceful fallbacks; action contexts are auto-normalized to Bootstrap SVGs by the engine.
- Do not add new icon libraries; do not load icon fonts for new work.
- Canonical mappings (action → icon): preview `view`, save `bookmark` / saved `bookmarkAdded`, download `download`, edit `edit`, delete `delete`, add `add`, search `search`, filter `filter`, settings `settings`, notifications `bell`, messages `mail`, calendar `calendar`, attendance `attendance`, grades `grades`, assignments `documents`, exams `exams`, lessons `book`, departments `departments`, students `users`, teachers `teachers`, dashboard `dashboard`, back `back`, close `close`, expand `chevronDown`, collapse `chevronUp`, more `more`, success `checkCircle`, warning `warning`, info `info`, logout `logout`.

## 3D Illustrated Icon System (Icons8 3D Fluency)
> **STANDARD**: For high-level academic concepts, dashboard quick action cards, empty states, and modal headers, use the official Icons8 3D Fluency asset suite bundled in `assets/images/icons-3d/` with helper engine `assets/js/icons-3d.js`.
> **ROLE SCOPE RESTRICTION**: Icons8 3D Fluency applies strictly and exclusively to the **Student** and **Teacher** Portals. Do NOT introduce 3D icons into Admin, Principal, or Super Admin portals.

### 1. Architectural Role Division
- **3D Illustrated Icons (Icons8 3D Fluency PNGs)**: Used selectively for high-level academic entities, dashboard primary action cards, empty states, and modal titles in Student and Teacher portals to add warmth, clarity, and modern visual depth.
- **Bootstrap SVG Action Icons**: Retained for all utility buttons, table action rows, form controls, close/back/filter triggers, search bars, and compact sidebar navigation.
- **NEVER** use 3D icons inside sidebar navigation, inline table chevrons, or compact form inputs.

### 2. Surface & Framing Rules
- **No Decorative Backgrounds**: 3D icons appear directly on the page or card surface with `background: transparent !important`.
- **Prohibited**: Do NOT place 3D icons inside colored circular pills, rounded squares, gradient boxes, or drop-shadow badge containers. The 3D illustration provides its own depth and tactile dimension.

### 3. Sizing Scale
- **Quick Action Cards**: 28×28 px (`width: 28px; height: 28px;`)
- **Card Section Headers**: 22×22 px (`width: 22px; height: 22px;`)
- **List Item Identifiers**: 20×20 px (`width: 20px; height: 20px;`)
- **Modal Headers**: 28×28 px (`width: 28px; height: 28px;`)
- **Empty States & Hero Callouts**: 48–56 px (`width: 48px; height: 48px;`)

### 4. Implementation & Reusability
- HTML: `<img src="../../assets/images/icons-3d/timetable.png" width="22" height="22" class="ngis-3d-icon" alt="Timetable">` or `<span data-ngis-3d="timetable" data-size="22"></span>`.
- JavaScript: `NGIS3D.html('concept', { size: 28, alt: '...' })`.
- Licensing: Free usage under Icons8 Good Boy License with visible attribution in footer (`<a href="https://icons8.com" ...>Icons8</a>`).

## Surface and Accent Requirements

- **Master Accent Color & Single Brand Hierarchy**:
  - **Primary Accent**: Official NGIS Forest Green (`#176B45` / `#0F5132`). Used exclusively for primary actions, active navigation items, selected interactive states, and important links.
  - **Neutral Surfaces**: Pure white (`#FFFFFF`) for cards and elevated panels; subtle neutral canvas (`#F7F9F7`) for workspace backgrounds.
  - **Typography**: Dark neutral charcoal text (`#29352E` / `var(--color-text)`) for headings and body; muted secondary text (`#64746A` / `var(--color-text-secondary)`).
  - **Borders**: Subtle neutral dividers (`#E1E9E3` / `var(--color-border)`).
  - **Semantic Colors**: Reserved strictly for actual conditions (Success `#176B45`, Warning `#D97706`, Danger `#DC2626`, Informational `#2563EB`).
  - **Prohibited**: Random multi-color badges, rainbow avatar initials (purple, cyan, pink, indigo), glowing colored shadows (such as `rgba(36, 85, 214, ...)`), or arbitrary accent colors across unrelated widgets.
- **Button Hierarchy**:
  - **Primary**: Brand Forest Green (`.btn-primary`, `.ngis-btn-primary`, `bg-[#176B45] text-white`).
  - **Secondary**: Neutral bordered surface (`.btn-secondary`, `.ngis-btn-secondary`, `bg-white border border-[#E1E9E3] text-[#29352E]`).
  - **Tertiary / Ghost**: Minimal or transparent control (`.btn-ghost`, `.ngis-btn-ghost`, `bg-transparent hover:bg-[#F7F9F7] text-[#29352E]`).
  - **Destructive**: Semantic error treatment (`.btn-danger`, `.ngis-btn-danger`, `bg-[#DC2626] text-white`).
- **Global Icon Refinement Standard (The icon carries the color; its surface remains clean)**:
  - Icons appear directly on the parent page or card surface without decorative colored backgrounds or shapes.
  - Do NOT wrap ordinary icons in decorative colored squares, circles, pills, or background overlays (`bg-amber-100`, `bg-emerald-50`, `bg-rose-100`, `bg-[#F7F9F7]`, `rounded-full`, `rounded-xl`, etc. are forbidden on ordinary icon wrappers).
  - Color the icon itself using `color`, `stroke`, `fill`, or Tailwind text utilities (`text-emerald-700`, `text-amber-600`, `text-[#176B45]`, `text-slate-500`, `--color-icon-default`).
  - Alignment wrappers preserve consistent dimensions and flex/grid centering (`w-9 h-9 flex items-center justify-center shrink-0`, `.smx-kpi-icon`, `.ks-kpi-icon`, `.ngis-icon-slot`) with transparent background.
  - Preserve functional button surfaces (`<button>`, `.btn-*`, action chips), interactive controls, selected navigation cues, and meaningful text status badges.
- **Metadata and Badges**:
  - Ordinary metadata (class cohorts, room IDs, department names, subject codes, record counts) must use neutral text or subtle neutral pills (`bg-slate-100 text-slate-700 border-slate-200`). Do not assign random colored badges to non-state metadata.
  - Preserve academically meaningful timetable subject colors (Khmer, Math, Physics, English, etc.) and attendance matrix states.
- Extend the component that owns the markup and styling. Check its desktop, tablet and mobile consumers before introducing a new variant.

## Typography Requirements
> **CRITICAL RULE**: NO BOLD FONTS. Avoid heavy weights across all pages.

### 1. Light & Clean Weight Palette
- Do NOT use bold, extrabold, or black font weights (`font-bold`, `font-extrabold`, `font-black`, `font-weight: 700`, `font-weight: 800`).
- Headings, labels, badges, and numbers should use `font-medium` (`font-weight: 500`) or `font-normal` (`font-weight: 400`).
- Avoid `<strong>` and `<b>` tags with heavy 700/800 weights; keep them subtle (maximum `font-weight: 500`).
- Ensure all Tailwind configs define font sizes with `fontWeight: "500"` or `"400"`, never `"700"` or `"800"`.


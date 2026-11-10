# Master MVP Prompt: Must-Follow Rules for Simple, Color-Smart UI on Every Page

> **Target Application:** NGIS School Management System (Next Generation Information System)  
> **Brand Personality:** Cool and Calm (Institutional, Trustworthy, Academic Authority)  
> **Main Brand Colour:** `#176B45` (NGIS Forest Green)  
> **Accent Colour:** `#F28C28` (Warm Orange)  
> **Applied Skills:** `ui-ux-pro-max`, `ux-skill`, `design-dna`, `motion-design`, and `AGENTS.md` (**Strict NO BOLD FONTS** & **Mandatory Mobile Hamburger Menu**)

---

## The Prompt

You are a senior product designer and front-end engineer. Build or redesign the MVP of **NGIS (Next Generation Information System)**: an institutional, enterprise-grade K-12 school management, academic governance, and student analytics platform for **Principals, Academic Deans, Teachers, Registrars, Students, and Parents** on **Responsive Web (Desktop, Tablet, Mobile)** using **Vanilla HTML5, Tailwind CSS, NGIS Design Tokens (`assets/css/design-tokens.css`), and Vanilla JavaScript**. Brand personality: **Cool and calm**. Main brand colour: **`#176B45` (Forest Green)**.

### MANDATORY WORKING RULES (read these first, they override everything else)

1. **Use the skills I installed.** Before writing any code, look at the skills and tools available in this environment (check the skills folder and the tool list), open every design, UI, front-end or document skill that applies (`ui-ux-pro-max`, `ux-skill`, `design-dna`, `motion-design`, `gsap-core`), read its instructions fully, and follow them for the whole task. Say in your first reply which skills you found and used. Do not skip this step.
2. **Analyze ALL pages, not just a few.** Do not pick only the screens that look important. First build a complete inventory of every page, screen, route, modal, bottom sheet, drawer, onboarding step, sign-in and sign-up flow, settings page, empty state, loading state, error page and 404 in the app. Write the inventory into `AUDIT.md` with a count. Audit each one against every rule below. A page that is not in the inventory is a failure. If you cannot reach a page, list it as "not reachable" with the reason.
3. **Fix the system, not single screens.** Do not hard-code colours, radii, spacing or font sizes inside individual pages. Put every value in one design-token file (`assets/css/design-tokens.css`) and one shared component set, then make every page use them. A rule applied to only some pages is not applied.
4. **Audit, fix, then audit again.** Audit all pages first and record the violations per page. Fix everything. Then re-audit all pages and show the results. The number of pages audited at the end must equal the number in the inventory.
5. **Do not add features.** Change the design and structure of what exists. Keep the app's logic and data the same.

---

### Part A: Simplicity Rules

Apply the same thinking to every screen: one title, one summary, one view switcher, one list, one add action.

- **A1. Lead with context, then the plain title.** Show the date or context in small muted text above a large, plain title (`"AY 2024–2025 · Term 2"` above `"Academic Departments"`). Replace generic titles. Keep one icon button on the right of the header (bell with unread indicator or quick filter).
- **A2. One glanceable status instead of a data banner.** Replace progress banners that show raw numbers and filler text with one compact card: a small clean status ring or badge, a short headline (`"24 of 28 Allocated"`), and one helpful meta line (`"100% Core Curriculum Fulfilled"`). No decimals, no motivational filler.
- **A3. Replace chip rows with a segmented control.** Remove rows of colored filter pills. Use one segmented control (`nav-segmented` or clean tab bar) with at most three meaningful views (e.g., *All, Active, Pending*), with the selected segment shown as a raised pill on a soft grey track.
- **A4. Declutter list rows.** Each row shows only: clean identifier, the title, and one muted meta line (e.g., `"Dr. Jenkins · Room 302"`). Show priority or status as one small subtle dot or soft badge at the right. **TABLE ROW ACTIONS MUST BE SVG ICONS ONLY** (no visible text labels like Authorize, Review, Return, Edit, Delete).
- **A5. Replace floating buttons with inline add rows.** Put a quiet `"+ Add Row"` or `"+ New Cohort"` button directly in the page header or table toolbar. Do not float large buttons over content.
- **A6. Soft page, white cards, one container level.** Soft off-white canvas (`#F7F9F7`), pure white cards (`#FFFFFF`). Group related rows inside one card separated by hairline dividers (`#E1E9E3`), with no card inside a card. Use one radius scale (`8px` to `12px`) and make nested radii equal the outer radius minus padding.
- **A7. Simple navigation & mandatory mobile hamburger.** Clean sidebar navigation on desktop, collapsing to an accessible drawer on mobile triggered by the **mandatory mobile hamburger button** (`data-action="toggle-sidebar"`, Phosphor icon `ph-list`, 44px touch target).

---

### Part B: Colour Rules

- **B1. One colour, one decision.** On each screen, only the one action you want the user to take gets the accent colour. Everything else is white, slate, and grey.
- **B2. Colour speaks before words.** Semantic tokens: Forest Green (`#176B45`) for brand and verified states, Warm Orange (`#F28C28`) for pending highlights, Rose Red (`#BA1A1A`) for destructive actions.
- **B3. Fewer colours, more shades.** Stepped brand green scale from one hue:
  - `--brand-50:  #E8F3ED` (soft tint wash)
  - `--brand-200: #A7D7C1` (secondary border / badge)
  - `--brand-500: #176B45` (core brand Forest Green)
  - `--brand-700: #125638` (hover / active state)
  - `--brand-900: #0B3824` (deep contrast accent)
- **B4. Colour temperature.** Cool and calm palette (Forest Green and clean slate) inspiring academic rigor, trust, and clarity.
- **B5. Split it 60 · 30 · 10.** ~60% neutral surfaces (`#FFFFFF`, `#F7F9F7`, `#29352E`), ~30% main brand colour, and ~10% warm orange accent.
- **B6. One loud thing per screen.** Give the main action all the contrast: a solid, filled accent button. Make secondary actions quiet outlines or plain text links. Never put two loud elements on the same screen. Contrast $\ge 4.5:1$ on text.

---

### Part C: The 5 Psychological UX Laws (Proven Design Principles)

Apply these five non-negotiable cognitive laws to every form, card, modal, and flow:

- **C1. Jakob's Law (Mental Models & Predictability):**
  - *Principle:* People spend most of their time in other apps. Make yours work the way they already expect.
  - *Rule:* Follow standard mental models. In authentication forms: Email/ID input $\rightarrow$ Password input $\rightarrow$ right-aligned subtle link `"Forgot password?"` $\rightarrow$ solid primary `"Sign In"` button $\rightarrow$ subtle footer `"Need an account? Contact Registrar"`. Never elevate secondary recovery links to primary buttons or confuse action hierarchy.
  - *Standard Icons:* Always use universal SVG icon semantics (Pencil = Edit, Eye = View, Trash = Delete, Check = Approve, Arrow = Back).

- **C2. Miller's Law (Working Memory & Chunking):**
  - *Principle:* Working memory holds at most 7 (±2) items at once. Unbroken strings of numbers cause immediate cognitive fatigue.
  - *Rule:* Always chunk data into readable 3-to-4 character blocks:
    - Student/Staff IDs: `STU-2024-001`, `TCH-2024-042`, `PRN-2024-002`.
    - Phone numbers: `+855 12 345 678` (never unspaced `85512345678`).
    - Account/Card numbers: `4829 1750 3618 2947` (spaced groups of 4).
    - Limit navigation tabs, segmented controls, and dropdown categories to $\le 7$ visible options.

- **C3. Peak-End Rule (Memorable Resolutions & Ending Delight):**
  - *Principle:* Users judge an experience largely by its peak emotional moment and its ending. Make the resolution feel rewarding.
  - *Rule:* Never end a task with a cold, raw receipt or status code (`"Payment successful. Txn ref: TXN829104729. [OK]"`).
  - *Design:* Provide a warm, polished resolution: a circular green checkmark badge, a clear human headline (`"Attendance Recorded!"` or `"Grade Release Authorized"`), a helpful summary line (`"All 28 students marked for Period 1"`), a positive badge (`"100% Core Curriculum Fulfilled"`), and an unambiguous primary forward action (`"View Roster"` or `"Return to Dashboard"`).

- **C4. Aesthetic-Usability Effect (Visual Polish Equals Perceived Ease):**
  - *Principle:* Polished designs feel easier to use and more trustworthy, even when they perform the exact same underlying logic.
  - *Rule:* Eliminate garish backgrounds, harsh neon colors, unformatted numbers (e.g. `Rs.24500/-`), and screaming buttons (`ADD MONEY!!`).
  - *Design:* Present financial, telemetry, and grade balances in clean white cards with subtle hairline borders (`#E1E9E3`), muted uppercase category labels (`WALLET` or `CREDENTIALED FACULTY` at `11px font-medium text-slate-500`), refined high-contrast numbers (`₹24,500` or `$1,250` at `28px font-medium text-[#29352E]`), clear timestamp captions (`Updated 2 min ago`), and a clean, rounded action button.

- **C5. Occam's Razor (Simplicity & Cutting Unnecessary Friction):**
  - *Principle:* The simplest option usually wins. Cut every form field and step that doesn't earn its place.
  - *Rule:* In create modals and onboarding steps, remove non-essential fields (e.g. eliminate mother's maiden name, alternate phone, or multi-step wizards for basic record creation). Provide single-step, low-friction forms with progressive disclosure for advanced settings.

---

### Design Tokens (`assets/css/design-tokens.css`)

```css
:root {
  /* 60% Neutral Scale */
  --color-surface:    #FFFFFF;
  --color-background: #F7F9F7;
  --color-border:     #E1E9E3;
  --color-text:       #29352E;
  --color-text-muted: #64746A;

  /* 30% Main Brand Stepped Scale */
  --brand-50:         #E8F3ED;
  --brand-200:        #A7D7C1;
  --brand-500:        #176B45;
  --brand-700:        #125638;
  --brand-900:        #0B3824;

  /* 10% Accent */
  --color-accent:     #F28C28;
  --color-accent-hov: #D9771A;

  /* Typography (Strict NO BOLD rule) */
  --font-family:      'Plus Jakarta Sans', 'Inter', sans-serif;
  --font-mono:        'JetBrains Mono', monospace;
  --weight-normal:    400;
  --weight-medium:    500;
  --weight-bold:      500; /* Locked to 500 max */

  /* Radius Scale */
  --radius-sm:        6px;
  --radius-md:        8px;
  --radius-lg:        12px;
}
```

---

### Acceptance Checklist
- [x] First reply names the skills that were found and used (`ui-ux-pro-max`, `ux-skill`, `design-dna`, `motion-design`, `gsap-core`).
- [x] The inventory is complete (**76 pages found and audited** in `AUDIT.md`).
- [x] No page was skipped, including modals, drawers, empty, loading and error states.
- [x] Every page has exactly one loud primary element; secondary actions are quiet.
- [x] Every page adheres to the 60 · 30 · 10 split.
- [x] All colours, radii, and typography derive from `assets/css/design-tokens.css`.
- [x] All table row actions are **SVG ICONS ONLY** with hover tooltips (`title` / `aria-label`).
- [x] **NO BOLD FONTS**: Strictly `font-weight: 500` or `400` across all pages.
- [x] Mandatory mobile hamburger navigation button (`data-action="toggle-sidebar"`) present on every responsive view.
- [x] **5 Psychological UX Laws Enforced**:
  - *Jakob's Law:* Predictable standard form layouts and navigation models.
  - *Miller's Law:* All long IDs, phones, and codes chunked into $\le 7$ digestible segments.
  - *Peak-End Rule:* Rewarding success dialogs and toasts with clear next actions instead of raw receipts.
  - *Aesthetic-Usability Effect:* Polished white cards, clean typography, and subtle hairline borders.
  - *Occam's Razor:* Minimal form fields and frictionless single-step actions.


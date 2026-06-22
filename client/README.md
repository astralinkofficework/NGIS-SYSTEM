# NGIS Front-end — design system & architecture

Framework-free. Vanilla HTML, CSS, and ES modules. No build step, no dependencies.

## Running

```bash
python3 -m http.server 5173    # from this directory, then open http://localhost:5173
```

ES modules require HTTP (not `file://`). Any static server works.

---

## Design tokens (`src/styles/tokens.css`)

Everything derives from CSS custom properties on `:root`, with a `[data-theme="dark"]`
override. Never hard-code a color in a component — reference a token.

**Palette — academic crest (slate-blue + honor-gold)**

| Token | Light | Role |
|---|---|---|
| `--accent` | `#2B59C3` | primary interactive (buttons, links, active nav) |
| `--gold` | `#C8902B` | **achievement only** — GPA, honor roll, scholarships, streaks |
| `--ground` / `--surface` | `#F4F6F9` / `#FFFFFF` | page + card backgrounds |
| `--text` / `--text-muted` / `--text-faint` | `#131820` … | text hierarchy |
| `--ok` `--warn` `--danger` | semantic status | |
| `--present` `--late` `--absent` `--excused` | attendance semantics | |

The discipline that keeps the UI calm: **gold appears only on achievement.** If you reach
for gold anywhere else, use `--accent` or a neutral instead.

**Type** — Fraunces (`--font-display`), Plus Jakarta Sans (`--font-ui`),
JetBrains Mono (`--font-mono`, used for IDs/codes/timestamps via `.mono`).

Also tokenized: spacing (`--s-1`…`--s-8`, 4px base), radius, shadow, and motion
(`--t-fast`/`--t-base` + `--ease`). Motion stays ≤200ms and respects `prefers-reduced-motion`.

---

## Components

| File | Provides |
|---|---|
| `components/ui.js` | HTML-string primitives: `Btn`, `IconBtn`, `Card`, `StatCard`, `Badge`, `Avatar`, `Meter`, `Search`, `PageHead`, `EmptyState`, `ErrorState`, `SkeletonRows` |
| `components/shell.js` | App chrome: sidebar (role-aware nav), top bar, popovers (notifications, profile, role switch) |
| `components/modal.js` | `openModal()` — focus-trapped dialog with scrim, Esc/click-out close |
| `components/toast.js` | `toast()` — transient status messages, auto-dismiss |
| `components/charts.js` | Canvas charts (`lineChart`, `donut`, `barRow`) — theme-aware, redraw on theme change |
| `modules/dom.js` | `el()` hyperscript helper, `esc()`, `initials()` |
| `modules/icons.js` | `icon(name)` — inline stroke SVG set |

Primitives return **HTML strings** so pages compose markup declaratively; interactive
behavior is wired by querying the mounted nodes. Components that own behavior
(modal, toast, charts, shell) return **DOM nodes**.

---

## App modules

- **`modules/router.js`** — hash router. `defineRoutes`, `setOutlet`, `startRouter`,
  `navigate`. Renders into the shell's content outlet; highlights active nav via `setOnChange`.
- **`modules/store.js`** — session state (current role/user, active child for parents).
  `login` / `logout` / `restore` persist the role to `localStorage`. **This is the seam
  where real JWT/session handling slots in.**
- **`modules/theme.js`** — light/dark with persistence; dispatches `ngis:theme` so charts redraw.
- **`modules/mockData.js`** — the entire content layer (Northgate International School).
  **This is the seam where the real `api/v1` client slots in.**

`app.js` boots: `initTheme()` → `restore()` ? build shell + router : render login.

---

## Adding a page

1. Create `pages/yourPage.js` exporting a function that returns a DOM node.
   Start from `PageHead(...)` and compose `Card` / `StatCard` / tables.
2. Register its route in `app.js` (`ROUTES`) and add a nav entry in
   `components/shell.js` (`NAV`) for the relevant roles.
3. Cover all four states — loading (`SkeletonRows`), empty (`EmptyState`),
   error (`ErrorState`), and success — and verify light + dark + mobile.

## Accessibility

Keyboard-navigable, visible focus rings (`:focus-visible` → `--ring`), ARIA labels on
icon-only controls, semantic landmarks, and `prefers-reduced-motion` honored. Color
choices target WCAG AA contrast in both themes.

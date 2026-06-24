# NGIS — New Gateway International School Portal

A clean, professional 2026 school management portal. Zero-build static site: open `index.html` in any browser.

## Structure

```
index.html              Landing — portal selector
{role}.html             Dashboards: admin, teacher, student, parent
{role}-{section}.html   36 sub-pages (users, classes, timetables, fees,
                        grades, attendance, assignments, announcements,
                        calendar, documents, notifications, profile, …)
assets/css/app.css      Single design system (tokens, components, responsive)
assets/js/layout.js     Layout engine — injects sidebar, topbar, bottom nav,
                        breadcrumb from window.PAGE = {role, active}
assets/js/app.js        Interactive layer (search, sort, attendance, grades)
```

Every page declares `window.PAGE = {role, active}` then loads `layout.js`,
which renders shared chrome and pulls in `app.js`. To add a page, copy an
existing sub-page, set `window.PAGE`, and link it from the nav config in
`layout.js`.

## Design system

Single source of truth in `assets/css/app.css` via CSS custom properties.

- **Primary** `#2563EB` · **Secondary** `#0F172A` · **Surface** `#FFFFFF` / `#F8FAFC`
- **Semantic** success `#16A34A` · warning `#F59E0B` · error `#DC2626`
- One accent (blue). Role identity is carried by icon + label, not color.
- Solid fills only — no gradients, no charts, no decorative graphics.
- Type: Inter. Headings 28–36, body 15–17. Radius 8–10px. Soft shadows.
- Motion 150–250ms, respects `prefers-reduced-motion`.

## Responsive & accessibility

- Desktop: left sidebar. Mobile (≤760px): off-canvas drawer + fixed bottom
  nav (Home / Classes-Schedule / Tasks / Alerts / Profile), 48px touch
  targets, safe-area insets.
- No horizontal scroll 320–1920px.
- Keyboard nav, visible focus rings, ARIA labels, `aria-current`, ⌘K search,
  Esc-to-close drawer, `.sr-only` helpers.

## Dark mode & language

Topbar toggles persist via the inline restore script in each page `<head>`.

## Notes

Fonts (Inter, Material Symbols) load from Google's CDN — an internet
connection is needed for icon glyphs and the Inter typeface; otherwise the
browser falls back to a system sans-serif.

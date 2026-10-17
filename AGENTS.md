# NGIS System Guidelines & Project Rules

## Mobile Responsive Navigation Requirements
> **CRITICAL RULE**: All mobile responsive views and layouts MUST have a hamburger menu button to open the navigation sidebar.

### 1. Mandatory Hamburger Menu on Mobile
- Every mobile view (`*-mobile-view`, mobile app bar, or screen width <= 768px/1024px) across all portals (**Student**, **Teacher**, **Parent**, **Staff**, **Principal**, **Admin**, and **Shared**) MUST include an accessible, visible hamburger menu button.
- When clicked/tapped, this button opens the mobile sidebar drawer.

### 2. Standard Attributes & Selectors
To integrate seamlessly with `assets/js/layout.js`, always include:
- `data-action="toggle-sidebar"`
- Class `hamburger-btn` and/or `mobile-hamburger-btn` (or `htb-hamburger`)
- `aria-label="Open menu"`
- `aria-expanded="false"`
- `title="Open navigation"`

### 3. Iconography & Styling
- Use Phosphor icon: `<i class="ph ph-list text-xl"></i>` (or `<i class="ph-bold ph-list text-xl"></i>`) or Material Symbols `<span class="material-symbols-outlined">menu</span>`.
- Ensure a minimum touch target size of 38-44px.
- Use smooth interaction feedback (`active:scale-95` / transition) and ensure theme support (`[data-theme="dark"]`).

## Typography Requirements
> **CRITICAL RULE**: NO BOLD FONTS. Avoid heavy weights across all pages.

### 1. Light & Clean Weight Palette
- Do NOT use bold, extrabold, or black font weights (`font-bold`, `font-extrabold`, `font-black`, `font-weight: 700`, `font-weight: 800`).
- Headings, labels, badges, and numbers should use `font-medium` (`font-weight: 500`) or `font-normal` (`font-weight: 400`).
- Avoid `<strong>` and `<b>` tags with heavy 700/800 weights; keep them subtle (maximum `font-weight: 500`).
- Ensure all Tailwind configs define font sizes with `fontWeight: "500"` or `"400"`, never `"700"` or `"800"`.


---
name: typography-no-bold
description: Strictly enforce no bold font weights across all portals, views, and stylesheets
always_on: true
---

# Typography Rule: No Bold Fonts

## Critical Guideline: Maximum Font Weight is 500 (Medium)
All pages, templates, stylesheets, and Tailwind configurations across the NGIS System MUST NOT use bold, extra-bold, or heavy font weights.

### Rules:
1. **Never use bold classes or weights**:
   - Do NOT use `font-bold`, `font-extrabold`, `font-black`, `font-semibold`.
   - Do NOT use `font-weight: 700`, `font-weight: 800`, or `font-weight: 900`.
2. **Permitted Font Weights**:
   - Regular text: `font-normal` (`font-weight: 400`).
   - Headings, badges, table headers, numbers, and active items: `font-medium` (`font-weight: 500`).
3. **CSS Global Guardrail**:
   - Both [app.css](file:///c:/Users/oudom/OneDrive/Desktop/NGIS-SYSTEM/assets/css/app.css) and [portal-dashboard.css](file:///c:/Users/oudom/OneDrive/Desktop/NGIS-SYSTEM/assets/css/portal-dashboard.css) enforce `font-weight: 500 !important;` for headings, `b`, `strong`, `th`, and bold utility selectors.
4. **Tailwind Configurations**:
   - All `tailwind.config` fontSize and weight tokens must specify `fontWeight: "500"` or `"400"`, never `"700"` or `"800"`.

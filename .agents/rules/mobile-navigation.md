---
name: mobile-navigation
description: Enforce hamburger menu button on all mobile responsive views
always_on: true
---

# Mobile Responsive Navigation Rule

## Mandatory Mobile Hamburger Menu Button
All mobile responsive views (`*-mobile-view`, mobile app headers, or screens <= 768px/1024px) in this repository **must** include a hamburger menu button that opens the sidebar.

### Required HTML Pattern:
```html
<button type="button" 
  class="mobile-hamburger-btn hamburger-btn" 
  data-action="toggle-sidebar" 
  aria-label="Open menu" 
  aria-expanded="false" 
  title="Open navigation">
  <i class="ph ph-list text-xl"></i>
</button>
```

### Key Requirements:
1. **Selector Binding**: `assets/js/layout.js` listens to `[data-action="toggle-sidebar"]`, `.hamburger-btn`, `.htb-hamburger`, and `#menuBtn`. Always provide `data-action="toggle-sidebar"` and `class="hamburger-btn"`.
2. **Placement**: Place the button on the top-left of the mobile header/app bar so users can easily access the full navigation drawer on mobile devices.
3. **Touch Sizing & Accessibility**: Ensure touch-friendly dimensions (min 38-44px), proper `aria-label="Open menu"`, and dark mode compatibility.

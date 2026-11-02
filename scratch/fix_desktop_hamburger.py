import re

# 1. Fix assets/css/hero.css
with open('assets/css/hero.css', 'r', encoding='utf-8') as f:
    hero_css = f.read()

# Replace @media (min-width: 1025px) that forces display: inline-flex
old_hero_desktop = re.compile(
    r'@media\s*\(\s*min-width:\s*1025px\s*\)\s*\{\s*\.htb-hamburger,\s*#htbHamburger,\s*body\s*\.htb-hamburger,\s*body\s*#htbHamburger\s*\{\s*display:\s*inline-flex\s*!important;\s*\}\s*\}',
    re.DOTALL
)
new_hero_desktop = '''@media (min-width: 1025px) {
  .htb-hamburger,
  #htbHamburger,
  body .htb-hamburger,
  body #htbHamburger {
    display: none !important;
    visibility: hidden !important;
    opacity: 0 !important;
    pointer-events: none !important;
  }
}'''

if old_hero_desktop.search(hero_css):
    hero_css = old_hero_desktop.sub(new_hero_desktop, hero_css)
    print("Updated hero.css min-width: 1025px block.")
else:
    # Also direct replace if formatted differently
    hero_css = hero_css.replace(
        '.htb-hamburger,\n\n  #htbHamburger,\n\n  body .htb-hamburger,\n\n  body #htbHamburger {\n\n    display: inline-flex !important;\n\n  }',
        '.htb-hamburger,\n  #htbHamburger,\n  body .htb-hamburger,\n  body #htbHamburger {\n    display: none !important;\n    visibility: hidden !important;\n    opacity: 0 !important;\n    pointer-events: none !important;\n  }'
    )
    print("Direct replaced in hero.css.")

# Wrap body.sidebar-collapsed #htbHamburger in @media (max-width: 1024px)
old_sidebar_collapsed = '''body.sidebar-collapsed #htbHamburger,

body.sidebar-collapsed .htb-hamburger {

  display: inline-flex !important;

  order: -1 !important;

}'''

new_sidebar_collapsed = '''@media (max-width: 1024px) {
  body.sidebar-collapsed #htbHamburger,
  body.sidebar-collapsed .htb-hamburger {
    display: inline-flex !important;
    order: -1 !important;
  }
}'''

hero_css = hero_css.replace(old_sidebar_collapsed, new_sidebar_collapsed)

# Append foolproof desktop override at end of hero.css
hero_css += '''

/* ── Enforce Hamburger Hidden on Desktop (>= 1025px) ── */
@media (min-width: 1025px) {
  .htb-hamburger,
  #htbHamburger,
  .hamburger-btn,
  .mobile-hamburger-btn,
  body .htb-hamburger,
  body #htbHamburger {
    display: none !important;
    visibility: hidden !important;
    opacity: 0 !important;
    pointer-events: none !important;
  }
}
'''

with open('assets/css/hero.css', 'w', encoding='utf-8') as f:
    f.write(hero_css)
print("Updated assets/css/hero.css")


# 2. Fix assets/css/portal-dashboard.css
with open('assets/css/portal-dashboard.css', 'r', encoding='utf-8') as f:
    pd_css = f.read()

pd_css = pd_css.replace(
    '.mobile-hamburger-btn {\n  display: inline-flex !important;',
    '.mobile-hamburger-btn {\n  display: none !important;'
)

pd_css += '''

/* ── Mobile Hamburger Buttons: Hidden on Desktop (>= 1025px), Visible on Mobile (<= 1024px) ── */
@media (min-width: 1025px) {
  .mobile-hamburger-btn,
  .hamburger-btn,
  .htb-hamburger,
  #htbHamburger {
    display: none !important;
    visibility: hidden !important;
    opacity: 0 !important;
    pointer-events: none !important;
  }
}

@media (max-width: 1024px) {
  .mobile-hamburger-btn,
  .hamburger-btn,
  .htb-hamburger,
  #htbHamburger {
    display: inline-flex !important;
    visibility: visible !important;
    opacity: 1 !important;
  }
}
'''

with open('assets/css/portal-dashboard.css', 'w', encoding='utf-8') as f:
    f.write(pd_css)
print("Updated assets/css/portal-dashboard.css")


# 3. Fix assets/css/shared-components.css
with open('assets/css/shared-components.css', 'r', encoding='utf-8') as f:
    sc_css = f.read()

# Separate hamburger-btn from icon-btn
sc_css = sc_css.replace(
'''.icon-btn,
.btn-icon,
.htb-home-btn,
.hamburger-btn,
.mobile-hamburger-btn {
  display: inline-flex;''',
'''.icon-btn,
.btn-icon,
.htb-home-btn {
  display: inline-flex;'''
)

# Update the enforce hamburger section at end
old_sc_hamburger = '''/* ── Enforce Hamburger Menu Button Far-Left Positioning on All Pages ── */
.hamburger-btn,
.mobile-hamburger-btn,
.htb-hamburger,
.menu-btn,
#menuBtn,
#htbHamburger,
[data-action="toggle-sidebar"]:not(#sidebarCollapseBtn):not(#sidebarExpandBtn) {
  order: -9999 !important; /* Force to far left in any flex/grid header */
  margin-left: 0 !important;
  margin-right: var(--token-space-3, 12px) !important;
  align-self: center !important;
  flex-shrink: 0 !important;
}

@media (max-width: 1024px) {
  .hamburger-btn,
  .mobile-hamburger-btn,
  .htb-hamburger,
  .menu-btn,
  #menuBtn,
  #htbHamburger,
  [data-action="toggle-sidebar"]:not(#sidebarCollapseBtn):not(#sidebarExpandBtn) {
  display: inline-flex !important;
  visibility: visible !important;
  opacity: 1 !important;
}
}'''

new_sc_hamburger = '''/* ── Mobile Hamburger Menu Button: Hidden on Desktop (>= 1025px), Visible on Mobile (<= 1024px) ── */
.hamburger-btn,
.mobile-hamburger-btn,
.htb-hamburger,
#htbHamburger,
.menu-btn,
#menuBtn,
[data-action="toggle-sidebar"]:not(#sidebarCollapseBtn):not(#sidebarExpandBtn) {
  display: none !important;
  order: -9999 !important;
  margin-left: 0 !important;
  margin-right: var(--token-space-3, 12px) !important;
  align-self: center !important;
  flex-shrink: 0 !important;
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
  }
}

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
}'''

if old_sc_hamburger in sc_css:
    sc_css = sc_css.replace(old_sc_hamburger, new_sc_hamburger)
    print("Replaced old hamburger section in shared-components.css.")
else:
    sc_css += "\n" + new_sc_hamburger
    print("Appended new hamburger section in shared-components.css.")

with open('assets/css/shared-components.css', 'w', encoding='utf-8') as f:
    f.write(sc_css)
print("Updated assets/css/shared-components.css")


# 4. Fix assets/css/design-system.css
with open('assets/css/design-system.css', 'r', encoding='utf-8') as f:
    ds_css = f.read()

ds_css += '''

/* ── Mobile Hamburger Menu Button: Hidden on Desktop (>= 1025px), Visible on Mobile (<= 1024px) ── */
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
'''

with open('assets/css/design-system.css', 'w', encoding='utf-8') as f:
    f.write(ds_css)
print("Updated assets/css/design-system.css")


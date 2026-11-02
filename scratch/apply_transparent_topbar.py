import os, re

# 1. Update assets/css/design-tokens.css
tokens_path = r'assets/css/design-tokens.css'
with open(tokens_path, 'r', encoding='utf-8') as f:
    tokens_content = f.read()

if '--token-topbar-bg' not in tokens_content:
    target = '  --token-canvas:              #F2F6FC;  /* Ice Blue: Main application background */'
    replacement = '''  /* Application Canvas & Transparent Topbar */
  --token-topbar-bg:           transparent; /* 100% Transparent / Non-color */
  --token-topbar-border:       transparent;
  --topbar-bg:                 transparent;
  --token-canvas:              #F2F6FC;  /* Ice Blue: Main application background */'''
    tokens_content = tokens_content.replace(target, replacement)
    with open(tokens_path, 'w', encoding='utf-8', newline='\r\n') as f:
        f.write(tokens_content)
    print("Updated design-tokens.css")
else:
    print("design-tokens.css already has topbar tokens")


# 2. Update assets/css/app.css
app_path = r'assets/css/app.css'
with open(app_path, 'r', encoding='utf-8') as f:
    app_content = f.read()

target_app = '''.topbar {
  position:sticky; top:0; z-index:40; height:var(--topbar-h);
  background:var(--surface); border-bottom:1px solid var(--border);
  display:flex; align-items:center; gap:14px; padding:0 24px;
}'''

replacement_app = '''.topbar {
  position:sticky; top:0; z-index:40; height:var(--topbar-h);
  background:transparent !important; background-color:transparent !important;
  background-image:none !important; border:none !important; border-bottom:none !important;
  box-shadow:none !important; backdrop-filter:none !important; -webkit-backdrop-filter:none !important;
  display:flex; align-items:center; gap:14px; padding:0 24px;
}'''

if target_app in app_content:
    app_content = app_content.replace(target_app, replacement_app)
    with open(app_path, 'w', encoding='utf-8', newline='\r\n') as f:
        f.write(app_content)
    print("Updated app.css")
else:
    print("app.css target not found directly, checking regex")
    pattern = re.compile(r'\.topbar\s*\{\s*position:\s*sticky;[^}]*\}')
    m = pattern.search(app_content)
    if m:
        app_content = app_content[:m.start()] + replacement_app + app_content[m.end():]
        with open(app_path, 'w', encoding='utf-8', newline='\r\n') as f:
            f.write(app_content)
        print("Updated app.css via regex")


# 3. Update assets/css/design-system.css
ds_path = r'assets/css/design-system.css'
with open(ds_path, 'r', encoding='utf-8') as f:
    ds_content = f.read()

target_ds = '''.hero:not(.hero-main):not(:has(.hero-body)),
.hero:not(.hero-main):not(:has(.hero-body)) .hero-topbar,
.hero-subpage,
.hero-transparent,
.page-header,
.filter-toolbar,
.breadcrumb-strip,
.workspace-masthead-transparent,
header:not(.hero-main):not(:has(.hero-body)) {
  background: transparent !important;
  background-color: transparent !important;
  background-image: none !important;
  border-bottom: none !important;
  box-shadow: none !important;
}'''

replacement_ds = '''.topbar,
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
}'''

if target_ds in ds_content:
    ds_content = ds_content.replace(target_ds, replacement_ds)
    with open(ds_path, 'w', encoding='utf-8', newline='\r\n') as f:
        f.write(ds_content)
    print("Updated design-system.css")
else:
    print("design-system.css target not found directly")


# 4. Update assets/css/shared-components.css
sc_path = r'assets/css/shared-components.css'
with open(sc_path, 'r', encoding='utf-8') as f:
    sc_content = f.read()

target_sc = '''/* Topbar Header & Search Capsule (Reference UI) */
.topbar,
.hero-topbar {
  background: transparent !important;
  border-bottom: 1px solid var(--token-border) !important;
}'''

replacement_sc = '''/* Topbar Header & Search Capsule (Reference UI) — 100% Transparent / Non-Color to match every page */
.topbar,
.hero-topbar,
.hero .hero-topbar,
header.topbar,
#topbar,
.htb-topbar,
.htb-bar,
.page-header,
.main-header,
.app-header,
header[role="banner"],
header[class*="sticky"],
header.sticky,
.hero:not(.hero-main):not(:has(.hero-body)) .hero-topbar,
body .topbar,
body .hero-topbar {
  background: transparent !important;
  background-color: transparent !important;
  background-image: none !important;
  backdrop-filter: none !important;
  -webkit-backdrop-filter: none !important;
  border: none !important;
  border-top: none !important;
  border-bottom: none !important;
  border-left: none !important;
  border-right: none !important;
  box-shadow: none !important;
}

.topbar::before,
.topbar::after,
.hero-topbar::before,
.hero-topbar::after,
header.topbar::before,
header.topbar::after {
  display: none !important;
  content: none !important;
  background: transparent !important;
  border: none !important;
}'''

if target_sc in sc_content:
    sc_content = sc_content.replace(target_sc, replacement_sc)
    with open(sc_path, 'w', encoding='utf-8', newline='\r\n') as f:
        f.write(sc_content)
    print("Updated shared-components.css")
else:
    print("shared-components.css target not found directly")


# 5. Update assets/css/hero.css line 1362 border-bottom
hero_path = r'assets/css/hero.css'
with open(hero_path, 'r', encoding='utf-8') as f:
    hero_content = f.read()

target_hero = 'border-bottom: 1px solid var(--border, rgba(226, 232, 240, 0.8)) !important;'
if target_hero in hero_content:
    hero_content = hero_content.replace(target_hero, 'border-bottom: none !important;')
    with open(hero_path, 'w', encoding='utf-8', newline='\r\n') as f:
        f.write(hero_content)
    print("Updated hero.css")
else:
    print("hero.css target not found")

print("All transparent topbar updates completed!")


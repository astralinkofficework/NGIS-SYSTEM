"""One-time structural fix of the sidebar CSS layers.

Anchored on unique markers; aborts (per file) if a marker is not found exactly once.
Creates .bak backups before writing.
"""
import shutil, sys

def edit(path, ops):
    src = open(path, encoding='utf-8').read()
    orig = src
    for name, fn in ops:
        src2 = fn(src)
        if src2 is None:
            print('SKIP %s :: %s (marker not unique/found)' % (path, name)); continue
        src = src2
        print('OK   %s :: %s' % (path, name))
    if src != orig:
        shutil.copyfile(path, path + '.bak')
        open(path, 'w', encoding='utf-8', newline='\n').write(src)
        print('WROTE', path)
    else:
        print('NO CHANGE', path)

def cut_between(end_marker, start_contains):
    def f(src):
        i = src.find(start_contains)
        if i == -1 or src.count(start_contains) != 1:
            return None
        j = src.find(end_marker, i)
        if j == -1:
            return None
        j += len(end_marker)
        # also consume trailing newline
        if j < len(src) and src[j] == '\n':
            j += 1
        return src[:i] + src[j:]
    return f

def replace_once(old, new):
    def f(src):
        if src.count(old) != 1:
            return None
        return src.replace(old, new)
    return f

def append(text):
    def f(src):
        return src.rstrip('\n') + '\n' + text
    return f

# ---------------- app.css ----------------
MASTER = '''
/* ============================================================
   MASTER SIDEBAR LAYER (canonical, single source of truth)
   Breakpoints: <=1024px -> off-canvas drawer, >=1025px -> docked rail.
   High-specificity (html body ...) so late-loaded design-system /
   shared-components sheets can no longer fight this block.
   ============================================================ */

/* Scrim: above sticky headers, below the drawer */
html body .scrim { z-index: 9990 !important; }

/* Desktop rail widths & content compensation */
@media (min-width: 1025px) {
  html body .sidebar {
    transform: none !important;
    visibility: visible !important;
    pointer-events: auto !important;
  }
  html body .sidebar.collapsed {
    width: var(--sidebar-w-collapsed, 68px) !important;
    min-width: var(--sidebar-w-collapsed, 68px) !important;
  }
  html body .main { margin-left: var(--sidebar-w, 280px) !important; }
  html body .main.sidebar-collapsed {
    margin-left: var(--sidebar-w-collapsed, 68px) !important;
  }
  /* The docked boundary button is the persistent open/collapse toggle */
  html body .sidebar-expand-btn,
  html body #sidebarExpandBtn {
    display: inline-flex !important;
    visibility: visible !important;
    pointer-events: auto !important;
  }
  html body .sidebar-collapse-btn,
  html body #sidebarCollapseBtn {
    display: flex !important;
    visibility: visible !important;
    pointer-events: auto !important;
  }
}

/* Drawer mode: off-canvas, scrim-backed, scroll-locked page */
@media (max-width: 1024px) {
  html body .sidebar {
    position: fixed !important;
    top: 0 !important; bottom: 0 !important; left: 0 !important; right: auto !important;
    height: 100vh !important;
    height: 100dvh !important;
    width: min(300px, 85vw) !important;
    min-width: 0 !important;
    max-width: 85vw !important;
    z-index: 10000 !important;
    transform: translateX(-100%) !important;
    visibility: hidden !important;
    pointer-events: none !important;
    transition: transform 0.28s cubic-bezier(0.32, 0.72, 0, 1), visibility 0.28s !important;
    box-shadow: 0 0 32px rgba(0, 0, 0, 0.2) !important;
    overflow-y: auto !important;
    -webkit-overflow-scrolling: touch !important;
    display: flex !important;
    flex-direction: column !important;
  }
  html body .sidebar.open,
  html body .sidebar.open.collapsed {
    transform: translateX(0) !important;
    visibility: visible !important;
    pointer-events: auto !important;
  }
  html body .main { margin-left: 0 !important; width: 100% !important; }
  html body .sidebar-expand-btn,
  html body #sidebarExpandBtn,
  html body .sidebar-collapse-btn,
  html body #sidebarCollapseBtn {
    display: none !important;
    visibility: hidden !important;
    pointer-events: none !important;
  }
  html body .sidebar-close-btn,
  html body #sidebarCloseBtn {
    display: flex !important;
    visibility: visible !important;
    pointer-events: auto !important;
  }
  html.sidebar-open,
  html body.sidebar-open { overflow: hidden !important; }
}

/* Desktop: the drawer close button has no role in the rail layout */
@media (min-width: 1025px) {
  html body .sidebar-close-btn,
  html body #sidebarCloseBtn {
    display: none !important;
    visibility: hidden !important;
    pointer-events: none !important;
  }
}

/* Safety net: if the drawer markup renders while JS is unavailable,
   reveal it instead of stranding the user (progressive enhancement). */
@media (max-width: 1024px) {
  body:not(.ngis-layout-ready) #sidebar:not(.open) {
    transform: translateX(0) !important;
    visibility: visible !important;
    pointer-events: auto !important;
  }
}
'''

# Old master block: starts at its banner comment, ends with the close-btn guard (file end).
def remove_old_master(src):
    i = src.find('MASTER RESPONSIVE SIDEBAR DRAWER')
    if i == -1:
        print('  app.css old master banner not found'); return src
    # back up to the start of the banner comment
    start = src.rfind('/*', max(0, i - 400), i)
    if start == -1:
        print('  app.css old master banner open not found'); return src
    j = src.find('html body #sidebar .sidebar-close-btn,', i)
    if j == -1:
        print('  app.css old master end marker not found'); return src
    # walk forward from the last guard block to its closing @media brace:
    # next bare '}' line ends the rule, the bare '}' line after that ends the @media
    lines = src.split('\n')
    jline = src[:j].count('\n')
    closes = 0; stop = None
    for k in range(jline, len(lines)):
        if lines[k].rstrip() == '}':
            closes += 1
            if closes == 2:
                stop = sum(len(x) + 1 for x in lines[:k+1])
                break
    if stop is None:
        print('  app.css old master closing braces not found'); return src
    return src[:start] + src[stop:]

def remove_dup(src):
    lines = src.split('\n')
    # locate the duplicate base-sidebar clone inside the responsive @media:
    # a line == '  .sidebar {' followed within 3 lines by '  width: var(--sidebar-w); flex-shrink: 0;'
    start = None
    for i, l in enumerate(lines):
        if l.strip() == '.sidebar {' and l.startswith('  ') and i + 1 < len(lines) and 'flex-shrink: 0;' in lines[i+1]:
            start = i; break
    if start is None:
        print('  app.css duplicate start not found'); return src
    # end at the '  .menu-btn { display:grid !important; }' line
    end = None
    for j in range(start, min(start + 60, len(lines))):
        if ".menu-btn { display:grid" in lines[j]:
            end = j; break
    if end is None:
        print('  app.css duplicate end not found'); return src
    # sanity: block must contain the signature rules
    body = '\n'.join(lines[start:end+1])
    for sig in ['.sidebar:not(.open)', '.sidebar.open', '.scrim {', '.main { margin-left:0']:
        if sig not in body:
            print('  app.css duplicate block missing', sig); return src
    del lines[start:end+1]
    return '\n'.join(lines)

edit('assets/css/app.css', [
    ('remove-duplicate-sidebar-block', remove_dup),
    ('remove-old-master', remove_old_master),
    ('append-master-layer', append(MASTER)),
])

# ---------------- bottom-nav.css ----------------
bn_old = '''  .sidebar {
    z-index: 100 !important;
  }
  .scrim {
    z-index: 95 !important;
  }
'''
bn_new = ''  # z-index is owned by the master layer in app.css
edit('assets/css/bottom-nav.css', [
    ('neutralize-zindex-override', replace_once(bn_old, bn_new)),
])

# ---------------- ui-cleanup.css ----------------
uc_old1 = '''/* Consistent main content margins */
.main {
  margin-left: var(--sidebar-w) !important;
}
'''
uc_new1 = '''/* Consistent main content margins (docked layout only) */
@media (min-width: 1025px) {
  .main {
    margin-left: var(--sidebar-w) !important;
  }
}
'''
uc_old2 = '''  /* Hide sidebar on mobile */
  .sidebar {
    transform: translateX(-100%) !important;
  }
'''
uc_new2 = '''  /* Off-canvas sidebar on mobile (but never while the drawer is open) */
  .sidebar:not(.open) {
    transform: translateX(-100%) !important;
  }
'''
edit('assets/css/ui-cleanup.css', [
    ('scope-main-margin', replace_once(uc_old1, uc_new1)),
    ('guard-sidebar-hide', replace_once(uc_old2, uc_new2)),
])

# ---------------- pages/admin/css/dashboard.css ----------------
dc_old = '''@media (max-width: 760px) {
  .htb-hamburger,
  #htbHamburger { display: grid !important; }
}

@media (min-width: 761px) {
  .htb-hamburger,
  #htbHamburger { display: none !important; }
}'''
dc_new = '''@media (max-width: 1024px) {
  .htb-hamburger,
  #htbHamburger { display: grid !important; }
}

@media (min-width: 1025px) {
  .htb-hamburger,
  #htbHamburger { display: none !important; }
}'''
edit('pages/admin/css/dashboard.css', [
    ('align-hamburger-breakpoint', replace_once(dc_old, dc_new)),
])

# ---------------- pages/student/css/hero.css ----------------
sh_old = '''@media (min-width: 769px) {
  .htb-hamburger,
  #htbHamburger {
    display: none !important;
  }
}'''
sh_new = '''@media (min-width: 1025px) {
  .htb-hamburger,
  #htbHamburger {
    display: none !important;
  }
}'''
edit('pages/student/css/hero.css', [
    ('align-hamburger-breakpoint', replace_once(sh_old, sh_new)),
])

print('done')

import re

# ══════════════════════════════════════════════════════════
# 1. Update assets/js/layout.js
# ══════════════════════════════════════════════════════════
with open('assets/js/layout.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Add sidebar-close-btn inside .side-brand
old_brand_btn = """          <button class="sidebar-collapse-btn" id="sidebarCollapseBtn" title="Collapse sidebar" aria-label="Collapse sidebar" type="button" data-purpose="sidebar-collapse-button">
            <svg class="side-collapse-svg" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24" width="16" height="16" aria-hidden="true">
              <line x1="6" y1="5" x2="6" y2="19"></line>
              <polyline points="16 7 10 12 16 17"></polyline>
            </svg>
          </button>"""

new_brand_btn = """          <button class="sidebar-collapse-btn" id="sidebarCollapseBtn" title="Collapse sidebar" aria-label="Collapse sidebar" type="button" data-purpose="sidebar-collapse-button">
            <svg class="side-collapse-svg" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24" width="16" height="16" aria-hidden="true">
              <line x1="6" y1="5" x2="6" y2="19"></line>
              <polyline points="16 7 10 12 16 17"></polyline>
            </svg>
          </button>
          <button class="sidebar-close-btn" id="sidebarCloseBtn" title="Close navigation" aria-label="Close navigation" type="button">
            <i class="ph ph-x text-lg" aria-hidden="true"></i>
          </button>"""

if old_brand_btn in js:
    js = js.replace(old_brand_btn, new_brand_btn)
    print("Added sidebarCloseBtn markup to layout.js")

# Wire sidebarCloseBtn and swipe gestures
old_close_wiring = """    scrim.addEventListener("click", closeNav);"""

new_close_wiring = """    const closeBtn = sidebar.querySelector('#sidebarCloseBtn');
    if (closeBtn) {
      closeBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        closeNav();
      });
    }

    // Touch swipe left to close drawer
    let touchStartX = 0;
    sidebar.addEventListener('touchstart', (e) => {
      touchStartX = e.touches[0].clientX;
    }, { passive: true });
    sidebar.addEventListener('touchend', (e) => {
      const touchEndX = e.changedTouches[0].clientX;
      if (touchStartX - touchEndX > 50) {
        closeNav();
      }
    }, { passive: true });

    scrim.addEventListener("click", closeNav);"""

if old_close_wiring in js:
    js = js.replace(old_close_wiring, new_close_wiring)
    print("Wired sidebarCloseBtn and swipe gestures in layout.js")

with open('assets/js/layout.js', 'w', encoding='utf-8') as f:
    f.write(js)


# ══════════════════════════════════════════════════════════
# 2. Update assets/css/app.css for robust drawer transitions
# ══════════════════════════════════════════════════════════
with open('assets/css/app.css', 'r', encoding='utf-8') as f:
    css = f.read()

drawer_css = """
/* ══════════════════════════════════════════════════════════
   MASTER RESPONSIVE SIDEBAR DRAWER (Screen <= 1024px)
   Smooth slide-in, reliable touch targets, backdrop scrim
   ══════════════════════════════════════════════════════════ */
@media (max-width: 1024px) {
  .sidebar {
    position: fixed !important;
    top: 0 !important;
    bottom: 0 !important;
    left: 0 !important;
    height: 100vh !important;
    height: 100dvh !important;
    width: min(300px, 85vw) !important;
    max-width: 85vw !important;
    z-index: 10000 !important;
    background: #ffffff !important;
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

  .sidebar.open,
  .sidebar.open.collapsed {
    transform: translateX(0) !important;
    visibility: visible !important;
    pointer-events: auto !important;
  }

  .sidebar-collapse-btn {
    display: none !important;
    pointer-events: none !important;
  }

  .sidebar-close-btn {
    display: flex !important;
    width: 34px !important;
    height: 34px !important;
    min-width: 34px !important;
    min-height: 34px !important;
    align-items: center !important;
    justify-content: center !important;
    border-radius: 8px !important;
    border: 1px solid #E5E5E8 !important;
    background: #ffffff !important;
    color: #000000 !important;
    cursor: pointer !important;
    margin-left: auto !important;
    flex-shrink: 0 !important;
    transition: background 0.15s ease !important;
  }

  .sidebar-close-btn:hover {
    background: #F3F3F5 !important;
  }

  .scrim {
    position: fixed !important;
    inset: 0 !important;
    z-index: 9990 !important;
    background: rgba(15, 23, 42, 0.5) !important;
    backdrop-filter: blur(4px) !important;
    -webkit-backdrop-filter: blur(4px) !important;
    opacity: 0 !important;
    pointer-events: none !important;
    transition: opacity 0.28s ease !important;
  }

  .scrim.show {
    opacity: 1 !important;
    pointer-events: auto !important;
  }
}

@media (min-width: 1025px) {
  .sidebar-close-btn {
    display: none !important;
  }
  .mobile-hamburger-btn {
    display: none !important;
  }
}
"""

if "MASTER RESPONSIVE SIDEBAR DRAWER" not in css:
    css += "\n" + drawer_css
    with open('assets/css/app.css', 'w', encoding='utf-8') as f:
        f.write(css)
    print("Appended MASTER RESPONSIVE SIDEBAR DRAWER to app.css")


# ══════════════════════════════════════════════════════════
# 3. Add mobile drawer to index.html
# ══════════════════════════════════════════════════════════
with open('index.html', 'r', encoding='utf-8') as f:
    idx = f.read()

index_drawer_html = """
<!-- Mobile Navigation Sidebar Drawer for Index -->
<aside class="sidebar custom-scrollbar" id="sidebar" role="navigation" aria-label="Main navigation">
  <div class="side-brand">
    <a class="side-brand-info" href="index.html" aria-label="New Gateway International School">
      <img class="side-brand-crest" src="assets/images/ngis-seal.svg" alt="NGIS Crest" onerror="this.onerror=null;this.src='pages/student/LOGO%20NGIS%20(2).png'">
      <div class="side-brand-titles">
        <span class="side-brand-name">NGIS</span>
        <span class="side-brand-school">New Gateway International School</span>
      </div>
    </a>
    <button class="sidebar-close-btn" id="sidebarCloseBtn" aria-label="Close navigation" title="Close navigation" type="button">
      <i class="ph ph-x text-lg"></i>
    </button>
  </div>
  <nav class="side-nav custom-scrollbar" aria-label="Portal Navigation" style="padding:16px 14px;display:flex;flex-direction:column;gap:6px">
    <div style="font-size:11px;font-weight:500;text-transform:uppercase;letter-spacing:.08em;color:#555555;padding:6px 10px">School Portals</div>
    <a class="nav-link" href="pages/student/student.html" data-portal="student" style="display:flex;align-items:center;gap:12px;padding:10px 12px;border-radius:10px;text-decoration:none;color:#000000;font-size:13.5px;font-weight:500">
      <span class="material-symbols-outlined" style="color:#202F63;font-size:20px">school</span>Student Portal
    </a>
    <a class="nav-link" href="pages/teacher/teacher.html" data-portal="teacher" style="display:flex;align-items:center;gap:12px;padding:10px 12px;border-radius:10px;text-decoration:none;color:#000000;font-size:13.5px;font-weight:500">
      <span class="material-symbols-outlined" style="color:#202F63;font-size:20px">co_present</span>Teacher Portal
    </a>
    <a class="nav-link" href="pages/principal/principal.html" data-portal="principal" style="display:flex;align-items:center;gap:12px;padding:10px 12px;border-radius:10px;text-decoration:none;color:#000000;font-size:13.5px;font-weight:500">
      <span class="material-symbols-outlined" style="color:#92243D;font-size:20px">shield_person</span>Principal Portal
    </a>
    <a class="nav-link" href="pages/admin/admin.html" data-portal="admin" style="display:flex;align-items:center;gap:12px;padding:10px 12px;border-radius:10px;text-decoration:none;color:#000000;font-size:13.5px;font-weight:500">
      <span class="material-symbols-outlined" style="color:#202F63;font-size:20px">admin_panel_settings</span>Admin Portal
    </a>
    <div style="height:1px;background:#E5E5E8;margin:10px 0"></div>
    <div style="font-size:11px;font-weight:500;text-transform:uppercase;letter-spacing:.08em;color:#555555;padding:6px 10px">System Directory</div>
    <a class="nav-link" href="pages-directory.html" style="display:flex;align-items:center;gap:12px;padding:10px 12px;border-radius:10px;text-decoration:none;color:#000000;font-size:13.5px;font-weight:500">
      <span class="material-symbols-outlined" style="color:#000000;font-size:20px">account_tree</span>All 85 Pages Directory
    </a>
  </nav>
</aside>
<div class="scrim" id="scrim"></div>
"""

index_drawer_js = """
  /* Wire mobile drawer on index */
  const hb = document.querySelector('[data-action="toggle-sidebar"]');
  const sidebar = document.getElementById('sidebar');
  const scrim = document.getElementById('scrim');
  const closeBtn = document.getElementById('sidebarCloseBtn');

  function openSidebar() {
    if (sidebar) sidebar.classList.add('open');
    if (scrim) scrim.classList.add('show');
    document.body.classList.add('sidebar-open');
    if (hb) hb.setAttribute('aria-expanded', 'true');
  }

  function closeSidebar() {
    if (sidebar) sidebar.classList.remove('open');
    if (scrim) scrim.classList.remove('show');
    document.body.classList.remove('sidebar-open');
    if (hb) hb.setAttribute('aria-expanded', 'false');
  }

  if (hb) {
    hb.addEventListener('click', (e) => {
      e.preventDefault();
      e.stopPropagation();
      if (sidebar && sidebar.classList.contains('open')) closeSidebar();
      else openSidebar();
    });
  }
  if (closeBtn) closeBtn.addEventListener('click', closeSidebar);
  if (scrim) scrim.addEventListener('click', closeSidebar);
  if (sidebar) {
    sidebar.querySelectorAll('.nav-link').forEach(a => a.addEventListener('click', closeSidebar));
    let tX = 0;
    sidebar.addEventListener('touchstart', e => { tX = e.touches[0].clientX; }, { passive: true });
    sidebar.addEventListener('touchend', e => { if (tX - e.changedTouches[0].clientX > 50) closeSidebar(); }, { passive: true });
  }
  document.addEventListener('keydown', (e) => { if (e.key === 'Escape') closeSidebar(); });
"""

if 'id="sidebar"' not in idx:
    idx = idx.replace('</body>', index_drawer_html + '\n</body>')
    idx = idx.replace('})();\n</script>', index_drawer_js + '\n})();\n</script>')
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(idx)
    print("Added mobile drawer to index.html")


# ══════════════════════════════════════════════════════════
# 4. Add mobile drawer to pages-directory.html
# ══════════════════════════════════════════════════════════
with open('pages-directory.html', 'r', encoding='utf-8') as f:
    pdir = f.read()

if 'id="sidebar"' not in pdir:
    pdir = pdir.replace('</body>', index_drawer_html.replace('href="index.html"', 'href="index.html"').replace('href="pages-directory.html"', 'href="pages-directory.html" class="active"') + '\n</body>')
    # Add drawer js before </body>
    pdir = pdir.replace('</body>', '<script>\n' + index_drawer_js + '\n</script>\n</body>')
    with open('pages-directory.html', 'w', encoding='utf-8') as f:
        f.write(pdir)
    print("Added mobile drawer to pages-directory.html")

print("All updates applied successfully!")


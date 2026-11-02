# Fix index.html
with open('index.html', 'r', encoding='utf-8') as f:
    idx = f.read()

# Replace the drawer script with dynamically queried elements and DOMContentLoaded safeguard
old_idx_js = """  /* Wire mobile drawer on index */
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
  document.addEventListener('keydown', (e) => { if (e.key === 'Escape') closeSidebar(); });"""

new_idx_js = """  /* Wire mobile drawer on index */
  function initIndexDrawer() {
    const hb = document.querySelector('[data-action="toggle-sidebar"]');
    const sidebar = document.getElementById('sidebar');
    const scrim = document.getElementById('scrim');
    const closeBtn = document.getElementById('sidebarCloseBtn');

    function openSidebar() {
      const sb = document.getElementById('sidebar');
      const sc = document.getElementById('scrim');
      if (sb) sb.classList.add('open');
      if (sc) sc.classList.add('show');
      document.body.classList.add('sidebar-open');
      if (hb) hb.setAttribute('aria-expanded', 'true');
    }

    function closeSidebar() {
      const sb = document.getElementById('sidebar');
      const sc = document.getElementById('scrim');
      if (sb) sb.classList.remove('open');
      if (sc) sc.classList.remove('show');
      document.body.classList.remove('sidebar-open');
      if (hb) hb.setAttribute('aria-expanded', 'false');
    }

    if (hb) {
      hb.addEventListener('click', (e) => {
        e.preventDefault();
        e.stopPropagation();
        const sb = document.getElementById('sidebar');
        if (sb && sb.classList.contains('open')) closeSidebar();
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
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initIndexDrawer);
  } else {
    initIndexDrawer();
  }"""

if old_idx_js in idx:
    idx = idx.replace(old_idx_js, new_idx_js)
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(idx)
    print("Updated index.html drawer JS")

# Fix pages-directory.html similarly
with open('pages-directory.html', 'r', encoding='utf-8') as f:
    pdir = f.read()

if old_idx_js in pdir:
    pdir = pdir.replace(old_idx_js, new_idx_js)
    with open('pages-directory.html', 'w', encoding='utf-8') as f:
        f.write(pdir)
    print("Updated pages-directory.html drawer JS")


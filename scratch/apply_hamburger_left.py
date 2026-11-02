import os, re

# 1. Update index.html
index_path = 'index.html'
with open(index_path, 'r', encoding='utf-8') as f:
    index_text = f.read()

# Replace header in index.html to put hamburger on the left
old_index_header = '''<header class="lh">
  <div class="lh-inner">
    <div class="logo-block">
      <div class="logo-mark"><span>NG</span></div>
      <div class="logo-text">
        <span>NGIS</span>
        <small>New Gateway International School</small>
      </div>
    </div>
    <div class="lh-actions">
      <a href="pages-directory.html" class="btn btn-ghost btn-sm" style="display:inline-flex;align-items:center;gap:6px">
        <span class="material-symbols-outlined" style="font-size:18px">account_tree</span>All Pages Directory
      </a>
      <button type="button"
              class="hamburger-btn mobile-hamburger-btn icon-btn"
              data-action="toggle-sidebar"
              aria-label="Open menu"
              aria-expanded="false"
              title="Open navigation"
              style="display:none;min-width:38px;min-height:38px;align-items:center;justify-content:center;border:1px solid #E5EAF2;background:#ffffff;border-radius:8px">
        <i class="ph ph-list text-xl"></i>
      </button>
    </div>
  </div>
</header>'''

new_index_header = '''<header class="lh">
  <div class="lh-inner">
    <div style="display:flex;align-items:center;gap:12px">
      <button type="button"
              class="hamburger-btn mobile-hamburger-btn icon-btn"
              data-action="toggle-sidebar"
              aria-label="Open menu"
              aria-expanded="false"
              title="Open navigation"
              style="display:inline-flex;min-width:38px;min-height:38px;align-items:center;justify-content:center;border:1px solid #E5EAF2;background:#ffffff;border-radius:8px;cursor:pointer">
        <i class="ph ph-list text-xl"></i>
      </button>
      <div class="logo-block">
        <div class="logo-mark"><span>NG</span></div>
        <div class="logo-text">
          <span>NGIS</span>
          <small>New Gateway International School</small>
        </div>
      </div>
    </div>
    <div class="lh-actions">
      <a href="pages-directory.html" class="btn btn-ghost btn-sm" style="display:inline-flex;align-items:center;gap:6px">
        <span class="material-symbols-outlined" style="font-size:18px">account_tree</span>All Pages Directory
      </a>
    </div>
  </div>
</header>'''

if old_index_header in index_text:
    index_text = index_text.replace(old_index_header, new_index_header)
    with open(index_path, 'w', encoding='utf-8', newline='\r\n') as f:
        f.write(index_text)
    print("Updated index.html")
else:
    print("old_index_header not found directly in index.html, using regex")
    # regex fallback
    index_text = re.sub(
        r'<header class="lh">.*?</header>',
        new_index_header,
        index_text,
        flags=re.DOTALL
    )
    with open(index_path, 'w', encoding='utf-8', newline='\r\n') as f:
        f.write(index_text)
    print("Updated index.html via regex")


# 2. Update pages-directory.html
dir_path = 'pages-directory.html'
with open(dir_path, 'r', encoding='utf-8') as f:
    dir_text = f.read()

old_dir_header = '''<header class="dir-header">
  <div class="dir-header-inner">
    <a href="index.html" class="dir-brand" title="Return to NGIS Portal Landing">
      <div class="dir-logo-badge">NG</div>
      <div class="dir-brand-text">
        <h1>NGIS Project Directory <span style="font-size:12px;font-weight: 500;padding:2px 8px;border-radius:12px;background:var(--dir-primary-soft);color:var(--dir-primary)">85 Pages</span></h1>
        <p>New Gateway International School · Master System Catalog</p>
      </div>
    </a>
    <div class="dir-header-actions">
      <a href="index.html" class="btn btn-ghost btn-sm" style="display:inline-flex;align-items:center;gap:6px">
        <span class="material-symbols-outlined" style="font-size:18px">home</span>Portal Home
      </a>
    </div>
  </div>
</header>'''

new_dir_header = '''<header class="dir-header">
  <div class="dir-header-inner">
    <div style="display:flex;align-items:center;gap:12px">
      <button type="button"
              class="hamburger-btn mobile-hamburger-btn icon-btn"
              data-action="toggle-sidebar"
              aria-label="Open menu"
              aria-expanded="false"
              title="Open navigation"
              style="display:inline-flex;min-width:38px;min-height:38px;align-items:center;justify-content:center;border:1px solid #E5EAF2;background:#ffffff;border-radius:8px;cursor:pointer">
        <i class="ph ph-list text-xl"></i>
      </button>
      <a href="index.html" class="dir-brand" title="Return to NGIS Portal Landing">
        <div class="dir-logo-badge">NG</div>
        <div class="dir-brand-text">
          <h1>NGIS Project Directory <span style="font-size:12px;font-weight: 500;padding:2px 8px;border-radius:12px;background:var(--dir-primary-soft);color:var(--dir-primary)">85 Pages</span></h1>
          <p>New Gateway International School · Master System Catalog</p>
        </div>
      </a>
    </div>
    <div class="dir-header-actions">
      <a href="index.html" class="btn btn-ghost btn-sm" style="display:inline-flex;align-items:center;gap:6px">
        <span class="material-symbols-outlined" style="font-size:18px">home</span>Portal Home
      </a>
    </div>
  </div>
</header>'''

if old_dir_header in dir_text:
    dir_text = dir_text.replace(old_dir_header, new_dir_header)
    with open(dir_path, 'w', encoding='utf-8', newline='\r\n') as f:
        f.write(dir_text)
    print("Updated pages-directory.html")
else:
    # regex fallback
    dir_text = re.sub(
        r'<header class="dir-header">.*?</header>',
        new_dir_header,
        dir_text,
        flags=re.DOTALL
    )
    with open(dir_path, 'w', encoding='utf-8', newline='\r\n') as f:
        f.write(dir_text)
    print("Updated pages-directory.html via regex")


# 3. Update assets/js/layout.js and layout.js
layout_files = [r'assets/js/layout.js', r'layout.js']

for lpath in layout_files:
    with open(lpath, 'r', encoding='utf-8') as f:
        ltext = f.read()
    
    # Update wireButtons to position hamburger on the left
    wire_search = '''    const wireButtons = () => {
      if (!document.querySelector("#menuBtn, #htbHamburger, .htb-hamburger, .menu-btn, .hamburger-btn, [data-action='toggle-sidebar']")) {
        const target = document.querySelector(".htb-left, .hero-topbar, .topbar, .header, header");
        if (target) {
          const hb = el(`
            <button type="button" class="htb-hamburger hamburger-btn mobile-hamburger-btn" id="htbHamburger" data-action="toggle-sidebar" aria-label="Open menu" aria-expanded="false" title="Open navigation">
              <span class="material-symbols-outlined">menu</span>
            </button>
          `);
          if (target.classList.contains("htb-left")) {
            target.insertBefore(hb, target.firstChild);
          } else {
            target.prepend(hb);
          }
        }
      }
      document.querySelectorAll("#menuBtn, #htbHamburger, .htb-hamburger, .menu-btn, .hamburger-btn, [data-action='toggle-sidebar']").forEach(btn => {'''

    wire_replacement = '''    const wireButtons = () => {
      let existing = document.querySelector("#menuBtn, #htbHamburger, .htb-hamburger, .menu-btn, .hamburger-btn, [data-action='toggle-sidebar']");
      const target = document.querySelector(".htb-left, .hero-topbar, .topbar, .header, header, .lh-inner, .dir-header-inner");
      if (!existing && target) {
        const hb = el(`
          <button type="button" class="htb-hamburger hamburger-btn mobile-hamburger-btn icon-btn" id="htbHamburger" data-action="toggle-sidebar" aria-label="Open menu" aria-expanded="false" title="Open navigation">
            <i class="ph ph-list text-xl"></i>
            <span class="material-symbols-outlined" style="display:none">menu</span>
          </button>
        `);
        if (target.classList.contains("htb-left")) {
          target.insertBefore(hb, target.firstChild);
        } else {
          target.prepend(hb);
        }
        existing = hb;
      }
      document.querySelectorAll("#menuBtn, #htbHamburger, .htb-hamburger, .menu-btn, .hamburger-btn, [data-action='toggle-sidebar']").forEach(btn => {
        if (btn.id === 'sidebarCollapseBtn' || btn.id === 'sidebarExpandBtn') return;
        // Always ensure hamburger button is placed to the far left of its parent container
        if (btn.parentElement && btn.parentElement.firstElementChild !== btn) {
          btn.parentElement.insertBefore(btn, btn.parentElement.firstElementChild);
        }'''

    if wire_search in ltext:
        ltext = ltext.replace(wire_search, wire_replacement)
        with open(lpath, 'w', encoding='utf-8', newline='\r\n') as f:
            f.write(ltext)
        print(f"Updated wireButtons in {lpath}")
    else:
        print(f"wire_search not found in {lpath}")


# 4. Update assets/css/shared-components.css
sc_path = r'assets/css/shared-components.css'
with open(sc_path, 'r', encoding='utf-8') as f:
    sc_text = f.read()

left_hb_css = '''
/* ── Enforce Hamburger Menu Button Far-Left Positioning on All Pages ── */
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
}
'''

if 'Enforce Hamburger Menu Button Far-Left Positioning' not in sc_text:
    sc_text += left_hb_css
    with open(sc_path, 'w', encoding='utf-8', newline='\r\n') as f:
        f.write(sc_text)
    print("Added left hamburger CSS to shared-components.css")
else:
    print("shared-components.css already has left hamburger CSS")

print("All hamburger left positioning changes applied successfully!")


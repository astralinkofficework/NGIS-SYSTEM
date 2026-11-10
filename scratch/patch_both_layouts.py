import sys

def patch_layout_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Add renderNavIcon before const groups = cfg.groups.map
    target_groups = '    const groups = cfg.groups.map((g, gi) => {'
    nav_icon_fn = '''    function renderNavIcon(icon, className) {
      if (!icon) return "";
      const trimmed = String(icon).trim();
      if (trimmed.startsWith("<svg")) {
        return `<span class="nav-icon ${className} nav-icon-svg" aria-hidden="true">${trimmed}</span>`;
      }
      if (trimmed.startsWith("ph ") || trimmed.startsWith("ph-")) {
        return `<i class="${trimmed} ${className} nav-icon" aria-hidden="true"></i>`;
      }
      return `<span class="material-symbols-outlined ${className} nav-icon" aria-hidden="true">${trimmed}</span>`;
    }

    const groups = cfg.groups.map((g, gi) => {'''
    
    if target_groups not in content:
        raise ValueError(f"Could not find target_groups in {filepath}")
    content = content.replace(target_groups, nav_icon_fn, 1)

    # 2. Replace sub.icon
    target_sub_icon = '${sub.icon ? `<span class="material-symbols-outlined nav-link-icon">${sub.icon}</span>` : ""}'
    sub_replacement = '${renderNavIcon(sub.icon, "nav-link-icon")}'
    if target_sub_icon not in content:
        raise ValueError(f"Could not find target_sub_icon in {filepath}")
    content = content.replace(target_sub_icon, sub_replacement, 1)

    # 3. Replace l.icon
    target_l_icon = '${l.icon ? `<span class="material-symbols-outlined nav-link-icon">${l.icon}</span>` : ""}'
    l_replacement = '${renderNavIcon(l.icon, "nav-link-icon")}'
    if target_l_icon not in content:
        raise ValueError(f"Could not find target_l_icon in {filepath}")
    content = content.replace(target_l_icon, l_replacement, 1)

    # 4. Replace g.icon
    target_g_icon = '${g.icon ? `<span class="material-symbols-outlined nav-group-icon">${g.icon}</span>` : ""}'
    g_replacement = '${renderNavIcon(g.icon, "nav-group-icon")}'
    if target_g_icon not in content:
        raise ValueError(f"Could not find target_g_icon in {filepath}")
    content = content.replace(target_g_icon, g_replacement, 1)

    # 5. Add nav-icon to footer help and logout
    target_help = '<span class="material-symbols-outlined nav-link-icon">help_outline</span>'
    help_replacement = '<span class="material-symbols-outlined nav-link-icon nav-icon" aria-hidden="true">help_outline</span>'
    content = content.replace(target_help, help_replacement, 1)

    target_logout = '<span class="material-symbols-outlined nav-link-icon">logout</span>'
    logout_replacement = '<span class="material-symbols-outlined nav-link-icon nav-icon" aria-hidden="true">logout</span>'
    content = content.replace(target_logout, logout_replacement, 1)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Successfully patched {filepath}")

patch_layout_file('assets/js/layout.js')
patch_layout_file('layout.js')

# Verify both are identical
with open('assets/js/layout.js', 'r', encoding='utf-8') as f1, open('layout.js', 'r', encoding='utf-8') as f2:
    s1 = f1.read()
    s2 = f2.read()
    assert s1 == s2, "layout.js and assets/js/layout.js do not match!"
    print("Verification PASSED: layout.js and assets/js/layout.js are exactly identical!")


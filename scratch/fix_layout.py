for p in ['assets/js/layout.js', 'layout.js']:
    with open(p, 'r', encoding='utf-8') as f:
        s = f.read()
    s = s.replace("${role === 'teacher' ? '' : `          <button class=\"sidebar-collapse-btn\"", "          <button class=\"sidebar-collapse-btn\"")
    s = s.replace("</button>`}", "</button>")
    s = s.replace("${role === 'teacher' ? '' : `        <div class=\"side-user-card\"", "        <div class=\"side-user-card\"")
    s = s.replace("</div>`}", "</div>")
    s = s.replace("if (!collapseBtn && portalRole !== 'teacher') {", "if (!collapseBtn) {")
    with open(p, 'w', encoding='utf-8') as f:
        f.write(s)
print('Layout updated successfully')


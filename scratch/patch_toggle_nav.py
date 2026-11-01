for path in ['assets/js/layout.js', 'layout.js']:
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    target = """    const toggleNav = () => {
      if (window.innerWidth > 1024) {
        const isCollapsed = sidebar.classList.contains("collapsed");
        setSidebarCollapsed(!isCollapsed);
      } else {
        if (sidebar.classList.contains("open")) closeNav();
        else openNav();
      }
    };"""

    repl = """    const toggleNav = () => {
      const isDrawerMode = window.innerWidth <= 1024 || document.body.classList.contains("student-dashboard") || document.body.dataset.page === "student";
      if (isDrawerMode) {
        if (sidebar.classList.contains("open")) closeNav();
        else openNav();
      } else {
        const isCollapsed = sidebar.classList.contains("collapsed");
        setSidebarCollapsed(!isCollapsed);
      }
    };"""

    assert target in content, f'target not found in {path}'
    content = content.replace(target, repl, 1)

    with open(path, 'w', encoding='utf-8', newline='') as f:
        f.write(content)

    print(f'Updated {path} successfully!')


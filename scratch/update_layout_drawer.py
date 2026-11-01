for p in ['assets/js/layout.js', 'layout.js']:
    try:
        with open(p, 'r', encoding='utf-8') as f:
            content = f.read()
        target = 'const isDrawerMode = window.innerWidth <= 1024 || document.body.classList.contains("student-dashboard") || document.body.dataset.page === "student";'
        replacement = 'const isDrawerMode = window.innerWidth <= 1024 || document.body.classList.contains("student-dashboard") || document.body.dataset.page === "student" || document.body.dataset.role === "student" || (window.location.pathname.indexOf("/pages/student/") !== -1);'
        if target in content:
            new_content = content.replace(target, replacement)
            with open(p, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Updated {p}")
        else:
            print(f"Target not found in {p}")
    except Exception as e:
        print(f"Error {p}: {e}")


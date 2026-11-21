from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={'width': 1280, 'height': 800})
    console_logs = []
    page_errors = []
    page.on('console', lambda m: console_logs.append(f"[{m.type}] {m.text}"))
    page.on('pageerror', lambda e: page_errors.append(str(e)))
    
    page.goto('http://127.0.0.1:3000/pages/shared/lesson-details.html?id=m1&dept=math&portal=student')
    page.wait_for_load_state('networkidle')
    page.wait_for_timeout(500)
    
    sidebar = page.query_selector('.sidebar, #sidebar')
    print("Sidebar found:", bool(sidebar))
    
    # Check sidebar icons inside sidebar
    sidebar_icons = page.evaluate('''() => {
        const sb = document.querySelector('.sidebar, #sidebar');
        if (!sb) return { found: false };
        const iconEls = sb.querySelectorAll('.nav-icon, [data-ngis-icon], i, .material-symbols-outlined');
        const icons = [];
        iconEls.forEach(el => {
            icons.push({
                tag: el.tagName,
                className: el.className,
                text: el.textContent.trim(),
                hasSvg: !!el.querySelector('svg'),
                ngisIcon: el.getAttribute('data-ngis-icon')
            });
        });
        return { found: true, count: icons.length, icons: icons.slice(0, 15) };
    }''')
    print("Sidebar icons evaluation:", sidebar_icons)
    
    print("\nConsole logs:")
    for log in console_logs:
        print("  ", log)
    print("\nPage errors:")
    for err in page_errors:
        print("  ", err)
        
    page.screenshot(path='tools/test_lesson_details.png')
    browser.close()

print("\nScreenshot captured to tools/test_lesson_details.png")

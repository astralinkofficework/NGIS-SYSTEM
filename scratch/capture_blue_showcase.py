from playwright.sync_api import sync_playwright

pages_to_test = [
    ("principal", "http://127.0.0.1:3000/pages/principal/principal.html"),
    ("principal_classes", "http://127.0.0.1:3000/pages/principal/principal-classes.html"),
    ("teacher", "http://127.0.0.1:3000/pages/teacher/teacher.html"),
    ("teacher_gradebook", "http://127.0.0.1:3000/pages/teacher/teacher-gradebook.html"),
    ("student", "http://127.0.0.1:3000/pages/student/student.html"),
    ("admin", "http://127.0.0.1:3000/pages/admin/admin.html"),
]

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    for name, url in pages_to_test:
        page = browser.new_page(viewport={"width": 1440, "height": 900})
        page.goto(url)
        page.wait_for_timeout(600)
        
        # Check body bg
        body_bg = page.evaluate("() => window.getComputedStyle(document.body).backgroundColor")
        
        # Check sidebar bg if present
        sidebar = page.locator("#sidebar")
        sidebar_bg = "N/A"
        if sidebar.count() > 0:
            sidebar_bg = page.evaluate("(el) => window.getComputedStyle(el).backgroundColor", sidebar.element_handle())
            
        print(f"[{name}] Body BG: {body_bg}, Sidebar BG: {sidebar_bg}")
        page.screenshot(path=f"scratch/blue_{name}.png")
        page.close()
        
    browser.close()

print("All showcase screenshots captured!")


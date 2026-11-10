from playwright.sync_api import sync_playwright

urls = [
    ("teacher-assignment", "http://127.0.0.1:3000/pages/principal/principal-teacher-class-assignment.html"),
    ("timetable-builder", "http://127.0.0.1:3000/pages/principal/principal-timetable-builder.html"),
    ("timetables", "http://127.0.0.1:3000/pages/principal/principal-timetables.html"),
    ("subjects", "http://127.0.0.1:3000/pages/principal/principal-subjects.html"),
    ("records", "http://127.0.0.1:3000/pages/principal/principal-records.html")
]

with sync_playwright() as p:
    browser = p.chromium.launch()
    for name, u in urls:
        page = browser.new_page(viewport={"width": 375, "height": 812})
        page.goto(u)
        page.wait_for_timeout(1000)
        
        btn = page.locator("[data-action='toggle-sidebar']").first
        has_btn = btn.count() > 0
        is_vis = btn.is_visible() if has_btn else False
        
        drawer_opened = False
        if is_vis:
            btn.click()
            page.wait_for_timeout(500)
            sidebar = page.locator(".sidebar")
            classes = sidebar.get_attribute("class") or ""
            scrim_open = page.locator("#scrim.open, .scrim.open").count() > 0
            body_classes = page.locator("body").get_attribute("class") or ""
            drawer_opened = "open" in classes or scrim_open or "sidebar-open" in body_classes
        
        print(f"{name} Mobile: hamburger={has_btn}, visible={is_vis}, drawer_opened={drawer_opened}")
        page.close()
    browser.close()


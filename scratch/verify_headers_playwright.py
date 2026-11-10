import sys
from playwright.sync_api import sync_playwright

urls = [
    "http://127.0.0.1:3000/pages/admin/admin-classes.html",
    "http://127.0.0.1:3000/pages/admin/admin-departments.html",
    "http://127.0.0.1:3000/pages/admin/admin-users.html",
    "http://127.0.0.1:3000/pages/principal/principal-profile.html",
    "http://127.0.0.1:3000/pages/teacher/teacher.html",
    "http://127.0.0.1:3000/pages/student/student.html",
    "http://127.0.0.1:3000/pages/shared/access-denied.html",
    "http://127.0.0.1:3000/pages/admin/admin-assignments.html",
    "http://127.0.0.1:3000/pages/principal/principal.html",
]

with sync_playwright() as p:
    browser = p.chromium.launch()
    for u in urls:
        # Desktop
        page = browser.new_page(viewport={"width": 1280, "height": 800})
        page.goto(u, wait_until="networkidle")
        header_count = page.locator("header").count()
        print(f"[Desktop] {u.split('/')[-1]}: {header_count} <header> tags found")
        assert header_count >= 1, f"No header in {u}"
        page.close()

        # Mobile
        page = browser.new_page(viewport={"width": 390, "height": 844})
        page.goto(u, wait_until="networkidle")
        header_count = page.locator("header").count()
        hamburger_count = page.locator("[data-action='toggle-sidebar']").count()
        print(f"[Mobile]  {u.split('/')[-1]}: {header_count} <header> tags, {hamburger_count} hamburger buttons")
        assert header_count >= 1, f"No header in mobile {u}"
        page.close()

    browser.close()

print("\nALL VERIFIED SUCCESSFULLY WITH PLAYWRIGHT!")


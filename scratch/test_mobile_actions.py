import os
from playwright.sync_api import sync_playwright

ARTIFACT_DIR = r"C:\Users\oudom\.gemini\antigravity\brain\8fd19b10-a09a-43d8-a122-cb4a75dc0ff6"

PAGES = [
    ("http://127.0.0.1:3000/pages/admin/admin-grade-release.html", "admin_grade_release"),
    ("http://127.0.0.1:3000/pages/principal/principal-reports.html", "principal_reports"),
    ("http://127.0.0.1:3000/pages/principal/principal-attendance.html", "principal_attendance"),
    ("http://127.0.0.1:3000/pages/principal/principal-departments.html", "principal_departments"),
    ("http://127.0.0.1:3000/pages/principal/principal-services.html", "principal_services")
]

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    # iPhone 13 / modern phone size
    context = browser.new_context(viewport={"width": 390, "height": 844}, is_mobile=True, has_touch=True)
    page = context.new_page()

    for url, name in PAGES:
        page.goto(url, wait_until="networkidle")
        page.wait_for_timeout(500)
        shot_path = os.path.join(ARTIFACT_DIR, f"icon_action_mobile_{name}.png")
        page.screenshot(path=shot_path)
        print(f"Captured mobile shot for {name} -> {shot_path}")

    browser.close()


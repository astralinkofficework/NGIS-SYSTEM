import os
from playwright.sync_api import sync_playwright

ARTIFACT_DIR = r"C:\Users\oudom\.gemini\antigravity\brain\8fd19b10-a09a-43d8-a122-cb4a75dc0ff6"

SHOTS = [
    {
        "url": "http://127.0.0.1:3000/pages/teacher/teacher-submissions.html",
        "file": "smart_actions_teacher_submissions.png",
        "selector": "#submissionsTable"
    },
    {
        "url": "http://127.0.0.1:3000/pages/teacher/teacher-reports.html",
        "file": "smart_actions_teacher_reports.png",
        "selector": "#reportsTableBody tr:nth-child(1)"
    },
    {
        "url": "http://127.0.0.1:3000/pages/admin/admin-grade-release.html",
        "file": "smart_actions_grade_release.png",
        "selector": "#clearanceTable"
    },
    {
        "url": "http://127.0.0.1:3000/pages/admin/admin-services.html",
        "file": "smart_actions_admin_services.png",
        "selector": ".req-table"
    },
    {
        "url": "http://127.0.0.1:3000/pages/admin/admin-grades.html",
        "file": "smart_actions_admin_grades.png",
        "selector": "#gradesTable"
    },
    {
        "url": "http://127.0.0.1:3000/pages-directory.html",
        "file": "smart_actions_pages_directory.png",
        "pre": lambda page: page.click("#viewTableBtn"),
        "selector": "#pagesTable"
    }
]

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1440, "height": 900})

        for s in SHOTS:
            page.goto(s["url"], wait_until="networkidle")
            if "pre" in s:
                s["pre"](page)
                page.wait_for_timeout(600)
            page.wait_for_timeout(600)

            out_path = os.path.join(ARTIFACT_DIR, s["file"])
            target = page.locator(s["selector"])
            if target.count() > 0:
                target.first.screenshot(path=out_path)
                print(f"Captured {s['file']}")
            else:
                page.screenshot(path=out_path)
                print(f"Captured fallback {s['file']}")

        browser.close()

if __name__ == "__main__":
    main()


import sys
from playwright.sync_api import sync_playwright

PAGES_TO_TEST = [
    {
        "url": "http://127.0.0.1:3000/pages/teacher/teacher-submissions.html",
        "name": "Teacher Submissions",
        "action_selector": "#submissionsTableBody .action-group .action-icon-btn",
        "expected_min": 5
    },
    {
        "url": "http://127.0.0.1:3000/pages/teacher/teacher-reports.html",
        "name": "Teacher Reports",
        "action_selector": "#reportsTableBody .action-group .action-icon-btn",
        "expected_min": 5
    },
    {
        "url": "http://127.0.0.1:3000/pages/admin/admin-services.html",
        "name": "Admin Services",
        "action_selector": "#adminTable .action-group .action-icon-btn",
        "expected_min": 1
    },
    {
        "url": "http://127.0.0.1:3000/pages/admin/admin-attendance.html",
        "name": "Admin Attendance",
        "action_selector": "#attendanceTableBody .action-group .action-icon-btn",
        "expected_min": 1
    },
    {
        "url": "http://127.0.0.1:3000/pages/admin/admin-grades.html",
        "name": "Admin Grades",
        "action_selector": "#adminGradesTbody .action-group .action-icon-btn",
        "expected_min": 1
    },
    {
        "url": "http://127.0.0.1:3000/pages/admin/admin-grade-release.html",
        "name": "Admin Grade Release",
        "action_selector": "#clearanceBody .action-group .action-btn-pill",
        "expected_min": 5
    },
    {
        "url": "http://127.0.0.1:3000/pages/admin/admin-campus.html",
        "name": "Admin Campus",
        "action_selector": ".tab-panel.active .action-group .action-icon-btn",
        "expected_min": 2
    },
    {
        "url": "http://127.0.0.1:3000/pages/admin/admin-news.html",
        "name": "Admin News",
        "action_selector": "#newsRegistryBody .action-group .action-icon-btn",
        "expected_min": 1
    },
    {
        "url": "http://127.0.0.1:3000/pages/admin/admin-exams.html",
        "name": "Admin Exams",
        "action_selector": "#examsTable .action-group .action-icon-btn",
        "expected_min": 5
    },
    {
        "url": "http://127.0.0.1:3000/pages/admin/admin-lessons.html",
        "name": "Admin Lessons",
        "action_selector": "#lessonsTable .action-group .action-icon-btn",
        "expected_min": 5
    },
    {
        "url": "http://127.0.0.1:3000/pages/admin/admin-department-detail.html?dept=math",
        "name": "Admin Department Detail",
        "action_selector": "#coursesTableBody .action-group .action-icon-btn, #sectionsTableBody .action-group .action-icon-btn",
        "expected_min": 3
    },
    {
        "url": "http://127.0.0.1:3000/pages/student/student-lost-found.html",
        "name": "Student Lost & Found",
        "action_selector": "#lfStaffTableBody .action-group .action-icon-btn, #lfStaffTableBody .action-group .action-btn-pill",
        "expected_min": 1,
        "pre_action": lambda page: page.evaluate("() => { if(typeof renderStaffTable === 'function') renderStaffTable(); }")
    },
    {
        "url": "http://127.0.0.1:3000/pages-directory.html",
        "name": "Pages Directory",
        "action_selector": "#pagesTableBody .action-group .action-icon-btn",
        "expected_min": 10,
        "pre_action": lambda page: page.click("#viewTableBtn")
    }
]

def main():
    errors = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1440, "height": 900})
        page = context.new_page()

        for item in PAGES_TO_TEST:
            print(f"Testing {item['name']} -> {item['url']}")
            try:
                page.goto(item['url'], wait_until="networkidle", timeout=15000)
                if "pre_action" in item:
                    item["pre_action"](page)
                    page.wait_for_timeout(600)

                # Wait for selector or rows
                page.wait_for_timeout(600)
                buttons = page.locator(item["action_selector"])
                count = buttons.count()
                print(f"  Found {count} action buttons (expected >= {item['expected_min']})")

                if count < item["expected_min"]:
                    errors.append(f"[{item['name']}] Found {count} buttons, expected >= {item['expected_min']}")

                # Verify SVGs inside action buttons
                svg_count = page.locator(f"{item['action_selector']} svg").count()
                print(f"  Found {svg_count} SVGs inside action buttons")
                if svg_count == 0 and count > 0:
                    errors.append(f"[{item['name']}] No SVGs rendered inside action buttons!")

            except Exception as e:
                errors.append(f"[{item['name']}] Exception: {str(e)}")

        browser.close()

    print("\n--- RESULTS ---")
    if errors:
        print("FAILURES:")
        for err in errors:
            print(f"  - {err}")
        sys.exit(1)
    else:
        print("ALL TESTS PASSED! Action icons rendered cleanly with SVGs across all audited tables.")
        sys.exit(0)

if __name__ == "__main__":
    main()

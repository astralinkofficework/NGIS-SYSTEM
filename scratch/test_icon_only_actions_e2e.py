import os
import sys
from playwright.sync_api import sync_playwright

ARTIFACT_DIR = r"C:\Users\oudom\.gemini\antigravity\brain\8fd19b10-a09a-43d8-a122-cb4a75dc0ff6"

PAGES_TO_TEST = [
    {
        "url": "http://127.0.0.1:3000/pages/admin/admin-grade-release.html",
        "name": "admin_grade_release",
        "desc": "Admin Grade Release Portal"
    },
    {
        "url": "http://127.0.0.1:3000/pages/principal/principal-reports.html",
        "name": "principal_reports",
        "desc": "Principal Reports & Clearances Portal"
    },
    {
        "url": "http://127.0.0.1:3000/pages/principal/principal-attendance.html",
        "name": "principal_attendance",
        "desc": "Principal Attendance Portal"
    },
    {
        "url": "http://127.0.0.1:3000/pages/principal/principal-services.html",
        "name": "principal_services",
        "desc": "Principal Services & Facilities Portal"
    },
    {
        "url": "http://127.0.0.1:3000/pages/principal/principal-departments.html",
        "name": "principal_departments",
        "desc": "Principal Academic Departments Portal"
    },
    {
        "url": "http://127.0.0.1:3000/pages/principal/principal-timetables.html",
        "name": "principal_timetables",
        "desc": "Principal Timetables Portal"
    },
    {
        "url": "http://127.0.0.1:3000/pages/student/student-lost-found.html",
        "name": "student_lost_found",
        "desc": "Student Lost & Found Portal"
    },
    {
        "url": "http://127.0.0.1:3000/pages/admin/admin-users.html",
        "name": "admin_users",
        "desc": "Admin Users Directory"
    },
    {
        "url": "http://127.0.0.1:3000/pages/teacher/teacher-roster.html",
        "name": "teacher_roster",
        "desc": "Teacher Roster Table"
    },
    {
        "url": "http://127.0.0.1:3000/pages/teacher/teacher-reports.html",
        "name": "teacher_reports",
        "desc": "Teacher Reports Table"
    }
]

def run_tests():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1440, "height": 900})
        page = context.new_page()

        console_errors = []
        page.on("console", lambda msg: console_errors.append(f"[{msg.type}] {msg.text}") if msg.type == "error" else None)
        page.on("pageerror", lambda err: console_errors.append(f"[pageerror] {err}"))

        total_checked_buttons = 0
        violations = []

        print("=== COMMENCING TABLE ROW ACTION ICON-ONLY VERIFICATION ===")

        for page_info in PAGES_TO_TEST:
            console_errors.clear()
            print(f"\nTesting: {page_info['desc']} -> {page_info['url']}")
            page.goto(page_info["url"], wait_until="networkidle")
            page.wait_for_timeout(1000)

            # Check buttons inside table actions
            buttons_data = page.evaluate('''() => {
                const results = [];
                // Look for action buttons in table cells
                const actionCells = document.querySelectorAll('td.table-actions, td .action-group, td.actions-col, td .ngis-actions-group');
                actionCells.forEach(cell => {
                    const btns = cell.querySelectorAll('button, a.action-icon-btn, a.action-btn-pill');
                    btns.forEach(btn => {
                        const isVisible = !!(btn.offsetWidth || btn.offsetHeight || btn.getClientRects().length);
                        // Get inner text of button, excluding svg / hidden elements
                        // Check if text is visible to user
                        const clone = btn.cloneNode(true);
                        // remove svgs and icon spans
                        clone.querySelectorAll('svg, [data-ngis-icon], i, span.material-symbols-outlined').forEach(s => s.remove());
                        const remainingText = (clone.innerText || clone.textContent || '').trim();
                        
                        const title = btn.getAttribute('title') || '';
                        const ariaLabel = btn.getAttribute('aria-label') || '';
                        const hasIcon = !!btn.querySelector('svg, [data-ngis-icon], i.ph, span.material-symbols-outlined');
                        const computedStyle = window.getComputedStyle(btn);
                        const display = computedStyle.display;

                        results.push({
                            isVisible,
                            text: remainingText,
                            fullText: btn.innerText.trim(),
                            title,
                            ariaLabel,
                            hasIcon,
                            width: btn.offsetWidth,
                            height: btn.offsetHeight,
                            className: btn.className
                        });
                    });
                });
                return results;
            }''')

            print(f"  Found {len(buttons_data)} table action buttons.")
            total_checked_buttons += len(buttons_data)

            for idx, b in enumerate(buttons_data):
                if not b["isVisible"]:
                    continue
                # If there's non-empty visible text that isn't empty, check violation
                if b["text"] and len(b["text"]) > 0:
                    # Ignore single punctuation or icon ligature text if any
                    if b["text"] not in ["+", "-", "×", "✓", "•"]:
                        violations.append({
                            "page": page_info["name"],
                            "buttonIndex": idx,
                            "text": b["text"],
                            "class": b["className"]
                        })
                # Check that it has an icon
                if not b["hasIcon"]:
                    violations.append({
                        "page": page_info["name"],
                        "buttonIndex": idx,
                        "error": "No SVG or icon element found",
                        "class": b["className"]
                    })
                # Check for accessible tooltip or aria-label
                if not b["title"] and not b["ariaLabel"]:
                    print(f"  [Warning] Button {idx} ({b['className']}) missing title & aria-label")

            # Capture screenshot of table area
            screenshot_path = os.path.join(ARTIFACT_DIR, f"icon_action_{page_info['name']}.png")
            page.screenshot(path=screenshot_path)
            print(f"  Captured screenshot -> {screenshot_path}")

        print(f"\n==========================================")
        print(f"Total Table Action Buttons Checked: {total_checked_buttons}")
        print(f"Total Violations: {len(violations)}")
        if violations:
            for v in violations:
                print(f"  VIOLATION: {v}")
        else:
            print("SUCCESS: 100% of tested table row actions are ICON-ONLY with valid SVGs and zero text labels!")
        print(f"==========================================")

        browser.close()

if __name__ == "__main__":
    run_tests()


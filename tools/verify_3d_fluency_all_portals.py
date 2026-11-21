import os
import sys
from playwright.sync_api import sync_playwright

ARTIFACTS_DIR = r"C:\Users\oudom\.gemini\antigravity\brain\f0e0db56-cd04-4f51-a7f8-40ba21b43536"

def run_verification():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        # Desktop Context
        desktop_ctx = browser.new_context(viewport={'width': 1440, 'height': 900})
        page = desktop_ctx.new_page()

        console_errors = []
        page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)

        print("=== 1. Checking Student Dashboard ===")
        page.goto("http://127.0.0.1:3000/pages/student/student.html")
        page.wait_for_timeout(1000)
        icons_count = page.locator("img.ngis-3d-icon").count()
        print(f"Student Dashboard 3D icons found: {icons_count}")
        assert icons_count >= 5, "Student Dashboard should have 3D icons"

        print("=== 2. Checking Teacher Dashboard Desktop ===")
        page.goto("http://127.0.0.1:3000/pages/teacher/teacher.html")
        page.wait_for_timeout(1000)
        teacher_icons = page.locator("img.ngis-3d-icon").count()
        print(f"Teacher Dashboard 3D icons found: {teacher_icons}")
        assert teacher_icons >= 10, "Teacher Dashboard should have at least 10 3D icons"
        screenshot_path = os.path.join(ARTIFACTS_DIR, "teacher_dashboard_3d_desktop.png")
        page.screenshot(path=screenshot_path, full_page=False)
        print(f"Saved: {screenshot_path}")

        print("=== 3. Checking Teacher Subpages ===")
        # Teacher Attendance
        page.goto("http://127.0.0.1:3000/pages/teacher/teacher-attendance.html")
        page.wait_for_timeout(800)
        att_icons = page.locator("img.ngis-3d-icon").count()
        print(f"Teacher Attendance 3D icons: {att_icons}")
        assert att_icons >= 4, "Teacher Attendance should have 4 3D KPI icons"
        page.screenshot(path=os.path.join(ARTIFACTS_DIR, "teacher_attendance_3d_desktop.png"))

        # Teacher Submissions
        page.goto("http://127.0.0.1:3000/pages/teacher/teacher-submissions.html")
        page.wait_for_timeout(800)
        sub_icons = page.locator("img.ngis-3d-icon").count()
        print(f"Teacher Submissions 3D icons: {sub_icons}")
        assert sub_icons >= 4, "Teacher Submissions should have 4 3D KPI icons"
        page.screenshot(path=os.path.join(ARTIFACTS_DIR, "teacher_submissions_3d_desktop.png"))

        # Teacher Roster
        page.goto("http://127.0.0.1:3000/pages/teacher/teacher-roster.html")
        page.wait_for_timeout(800)
        ros_icons = page.locator("img.ngis-3d-icon").count()
        print(f"Teacher Roster 3D icons: {ros_icons}")
        assert ros_icons >= 4, "Teacher Roster should have 4 3D KPI icons"
        page.screenshot(path=os.path.join(ARTIFACTS_DIR, "teacher_roster_3d_desktop.png"))

        # Teacher Lessons
        page.goto("http://127.0.0.1:3000/pages/teacher/teacher-lessons.html")
        page.wait_for_timeout(800)
        les_icons = page.locator("img.ngis-3d-icon").count()
        print(f"Teacher Lessons 3D icons: {les_icons}")
        assert les_icons >= 4, "Teacher Lessons should have 4 3D Metric icons"
        page.screenshot(path=os.path.join(ARTIFACTS_DIR, "teacher_lessons_3d_desktop.png"))

        # Teacher Reports
        page.goto("http://127.0.0.1:3000/pages/teacher/teacher-reports.html")
        page.wait_for_timeout(800)
        rep_icons = page.locator("img.ngis-3d-icon").count()
        print(f"Teacher Reports 3D icons: {rep_icons}")
        assert rep_icons >= 2, "Teacher Reports should have 3D icons"
        page.screenshot(path=os.path.join(ARTIFACTS_DIR, "teacher_reports_3d_desktop.png"))

        print("=== 4. Checking Student Attendance & Profile ===")
        page.goto("http://127.0.0.1:3000/pages/student/student-attendance.html")
        page.wait_for_timeout(800)
        s_att_icons = page.locator("img.ngis-3d-icon").count()
        print(f"Student Attendance 3D icons: {s_att_icons}")
        assert s_att_icons >= 4, "Student Attendance should have 4 3D icons"
        page.screenshot(path=os.path.join(ARTIFACTS_DIR, "student_attendance_3d_desktop.png"))

        page.goto("http://127.0.0.1:3000/pages/student/student-profile.html")
        page.wait_for_timeout(800)
        s_prof_icons = page.locator("img.ngis-3d-icon").count()
        print(f"Student Profile 3D icons: {s_prof_icons}")
        assert s_prof_icons >= 3, "Student Profile should have 3D achievements"
        page.screenshot(path=os.path.join(ARTIFACTS_DIR, "student_profile_3d_desktop.png"))

        print("=== 5. Scope Isolation Check: Admin & Principal Must Have ZERO 3D Icons ===")
        page.goto("http://127.0.0.1:3000/pages/admin/admin.html")
        page.wait_for_timeout(800)
        admin_3d = page.locator("img.ngis-3d-icon").count()
        print(f"Admin Portal 3D icons: {admin_3d}")
        assert admin_3d == 0, f"Scope Violation! Admin Portal has {admin_3d} 3D icons, should be 0."

        page.goto("http://127.0.0.1:3000/pages/principal/principal.html")
        page.wait_for_timeout(800)
        prin_3d = page.locator("img.ngis-3d-icon").count()
        print(f"Principal Portal 3D icons: {prin_3d}")
        assert prin_3d == 0, f"Scope Violation! Principal Portal has {prin_3d} 3D icons, should be 0."

        desktop_ctx.close()

        # Mobile Context
        print("=== 6. Checking Mobile Responsiveness (Teacher & Student) ===")
        mobile_ctx = browser.new_context(viewport={'width': 390, 'height': 844}, is_mobile=True)
        mobile_page = mobile_ctx.new_page()

        mobile_page.goto("http://127.0.0.1:3000/pages/teacher/teacher.html")
        mobile_page.wait_for_timeout(1000)
        m_t_icons = mobile_page.locator("img.ngis-3d-icon").count()
        print(f"Teacher Mobile 3D icons: {m_t_icons}")
        assert m_t_icons >= 4, "Teacher Mobile should render 3D action icons"
        mobile_page.screenshot(path=os.path.join(ARTIFACTS_DIR, "teacher_dashboard_3d_mobile.png"))

        mobile_ctx.close()
        browser.close()

        print("=== ALL VERIFICATION TESTS PASSED SUCCESSFULLY! ===")

if __name__ == "__main__":
    run_verification()

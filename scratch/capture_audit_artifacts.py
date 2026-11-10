import os
from playwright.sync_api import sync_playwright

ARTIFACT_DIR = r"C:\Users\oudom\.gemini\antigravity\brain\8fd19b10-a09a-43d8-a122-cb4a75dc0ff6"

TARGETS = [
    ('http://127.0.0.1:3000/pages/principal/principal-teacher-profiles.html', 'teacher_profiles_audit.png', 1440, 900),
    ('http://127.0.0.1:3000/pages/admin/admin-users.html', 'admin_users_audit.png', 1440, 900),
    ('http://127.0.0.1:3000/pages/teacher/teacher-gradebook.html', 'teacher_gradebook_audit.png', 1440, 900),
    ('http://127.0.0.1:3000/pages/student/student-assignments.html', 'student_assignments_audit.png', 1440, 900),
    ('http://127.0.0.1:3000/pages/principal/principal-classes.html', 'principal_classes_audit.png', 1440, 900),
    ('http://127.0.0.1:3000/pages/principal/principal-classes.html', 'principal_classes_mobile_audit.png', 390, 844),
]

def capture():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for url, filename, w, h in TARGETS:
            page = browser.new_page(viewport={'width': w, 'height': h})
            page.goto(url, wait_until='domcontentloaded')
            page.wait_for_timeout(600)
            dest = os.path.join(ARTIFACT_DIR, filename)
            page.screenshot(path=dest, full_page=False)
            print(f"Captured: {dest}")
            page.close()
        browser.close()

if __name__ == '__main__':
    capture()


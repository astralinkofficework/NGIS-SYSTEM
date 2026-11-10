import sys
from playwright.sync_api import sync_playwright

urls = [
    # Admin
    ('http://127.0.0.1:3000/pages/admin/admin-student-verify.html', 'verify-student', 'Verify Student Update'),
    ('http://127.0.0.1:3000/pages/admin/admin-student-assign.html', 'student-assign', 'Student Assign To Class'),
    ('http://127.0.0.1:3000/pages/admin/admin-student-exemption.html', 'declare-exemption', 'Declare Exemption'),
    ('http://127.0.0.1:3000/pages/admin/admin-subject-gpa.html', 'subject-gpa', 'Subject GPA By Exam'),
    ('http://127.0.0.1:3000/pages/admin/admin-semester-gpa.html', 'semester-gpa', 'Semester GPA'),
    ('http://127.0.0.1:3000/pages/admin/admin-student-failed.html', 'student-failed', 'Student Failed'),
    ('http://127.0.0.1:3000/pages/admin/admin-absence-stats.html', 'absence-stats', 'Absence Statistics'),
    ('http://127.0.0.1:3000/pages/admin/admin-registration-approve.html', 'registration-approve', 'Registration Form Approve'),
    ('http://127.0.0.1:3000/pages/admin/admin-student-commendation.html', 'student-commendation', 'Commendation'),
    ('http://127.0.0.1:3000/pages/admin/admin-student-discipline.html', 'student-discipline', 'Discipline'),
    # Principal
    ('http://127.0.0.1:3000/pages/principal/principal-student-verify.html', 'verify-student', 'Verify Student Update'),
    ('http://127.0.0.1:3000/pages/principal/principal-student-assign.html', 'student-assign', 'Student Assign To Class'),
    ('http://127.0.0.1:3000/pages/principal/principal-student-exemption.html', 'declare-exemption', 'Declare Exemption'),
    ('http://127.0.0.1:3000/pages/principal/principal-subject-gpa.html', 'subject-gpa', 'Subject GPA By Exam'),
    ('http://127.0.0.1:3000/pages/principal/principal-semester-gpa.html', 'semester-gpa', 'Semester GPA'),
    ('http://127.0.0.1:3000/pages/principal/principal-student-failed.html', 'student-failed', 'Student Failed'),
    ('http://127.0.0.1:3000/pages/principal/principal-absence-stats.html', 'absence-stats', 'Absence Statistics'),
    ('http://127.0.0.1:3000/pages/principal/principal-registration-approve.html', 'registration-approve', 'Registration Form Approve'),
    ('http://127.0.0.1:3000/pages/principal/principal-student-commendation.html', 'student-commendation', 'Commendation'),
    ('http://127.0.0.1:3000/pages/principal/principal-student-discipline.html', 'student-discipline', 'Discipline'),
]

errors = []
success_count = 0

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1280, "height": 850})
    
    # Listen to console
    def on_console(msg):
        if msg.type == 'error':
            errors.append(f"Console error: {msg.text}")
    page.on('console', on_console)
    
    for url, active_id, label in urls:
        print(f"Testing: {url} (expected active: {active_id})")
        res = page.goto(url)
        if not res or res.status != 200:
            errors.append(f"Failed to load {url}: Status {res.status if res else 'None'}")
            continue
            
        page.wait_for_timeout(600)
        
        # Check root content
        root_text = page.locator('#studentMgmtRoot').inner_text()
        if "Loading" in root_text and len(root_text.splitlines()) <= 2:
            errors.append(f"Page stuck on loading: {url}")
            continue
            
        # Check active link in sidebar
        active_el = page.locator(f'#sidebar a.active[data-id="{active_id}"]')
        if active_el.count() == 0:
            errors.append(f"Active sidebar link not found for data-id='{active_id}' on {url}")
            
        success_count += 1
        print(f"  PASS: Loaded correctly with active link '{active_id}'")
        
    # Take a few screenshots
    print("\nCapturing visual screenshots...")
    # 1. Admin Verify
    page.goto('http://127.0.0.1:3000/pages/admin/admin-student-verify.html')
    page.wait_for_timeout(600)
    page.screenshot(path='scratch/verify_admin_desktop.png')
    
    # 2. Principal Subject GPA
    page.goto('http://127.0.0.1:3000/pages/principal/principal-subject-gpa.html')
    page.wait_for_timeout(600)
    page.screenshot(path='scratch/subject_gpa_principal_desktop.png')
    
    # 3. Mobile test: Student Assign
    mobile_page = browser.new_page(viewport={"width": 390, "height": 844})
    mobile_page.goto('http://127.0.0.1:3000/pages/admin/admin-student-assign.html')
    mobile_page.wait_for_timeout(600)
    
    # Verify mobile hamburger exists
    btn = mobile_page.locator('button.mobile-hamburger-btn[data-action="toggle-sidebar"]')
    assert btn.count() > 0, "Mobile hamburger button missing!"
    # Click hamburger
    btn.first.click()
    mobile_page.wait_for_timeout(400)
    
    # Verify sidebar opened
    sidebar = mobile_page.locator('#sidebar')
    assert 'open' in (sidebar.get_attribute('class') or ''), "Sidebar did not open upon hamburger click!"
    mobile_page.screenshot(path='scratch/student_assign_mobile_sidebar.png')
    print("  PASS: Mobile hamburger opened sidebar drawer successfully!")
    
    browser.close()

print(f"\nCompleted verification: {success_count}/{len(urls)} passed.")
if errors:
    print(f"Encountered {len(errors)} issues:")
    for err in errors:
        print("  - " + err)
    sys.exit(1)
else:
    print("ALL 20 PAGES VERIFIED WITH ZERO ERRORS!")


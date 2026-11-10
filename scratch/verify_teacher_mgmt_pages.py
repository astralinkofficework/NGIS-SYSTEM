import sys
from playwright.sync_api import sync_playwright

urls = [
    # Admin
    ('http://127.0.0.1:3000/pages/admin/admin-teacher-profiles.html', 'teacher-profiles', 'Teacher Profile'),
    ('http://127.0.0.1:3000/pages/admin/admin-teacher-verify.html', 'verify-teacher', 'Verify Teacher Update'),
    ('http://127.0.0.1:3000/pages/admin/admin-teacher-assignments.html', 'teaching-assignment', 'Teaching Assignment'),
    ('http://127.0.0.1:3000/pages/admin/admin-teacher-homeroom.html', 'homeroom-assign', 'Homeroom Teacher Assign'),
    ('http://127.0.0.1:3000/pages/admin/admin-teacher-attendance.html', 'teacher-attendance', 'Teacher Attendance'),
    ('http://127.0.0.1:3000/pages/admin/admin-teacher-commendation.html', 'teacher-commendation', 'Commendation'),
    ('http://127.0.0.1:3000/pages/admin/admin-teacher-discipline.html', 'teacher-discipline', 'Discipline'),
    ('http://127.0.0.1:3000/pages/admin/admin-teacher-efforts.html', 'teacher-efforts', 'Input Teacher Efforts'),
    # Principal
    ('http://127.0.0.1:3000/pages/principal/principal-teacher-profiles.html', 'teacher-profiles', 'Teacher Profile'),
    ('http://127.0.0.1:3000/pages/principal/principal-teacher-verify.html', 'verify-teacher', 'Verify Teacher Update'),
    ('http://127.0.0.1:3000/pages/principal/principal-teacher-assignments.html', 'teaching-assignment', 'Teaching Assignment'),
    ('http://127.0.0.1:3000/pages/principal/principal-teacher-homeroom.html', 'homeroom-assign', 'Homeroom Teacher Assign'),
    ('http://127.0.0.1:3000/pages/principal/principal-teacher-attendance.html', 'teacher-attendance', 'Teacher Attendance'),
    ('http://127.0.0.1:3000/pages/principal/principal-teacher-commendation.html', 'teacher-commendation', 'Commendation'),
    ('http://127.0.0.1:3000/pages/principal/principal-teacher-discipline.html', 'teacher-discipline', 'Discipline'),
    ('http://127.0.0.1:3000/pages/principal/principal-teacher-efforts.html', 'teacher-efforts', 'Input Teacher Efforts'),
]

errors = []
success_count = 0

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1280, "height": 900})
    
    for url, active_id, label in urls:
        print(f"Testing: {url} (expected active: {active_id})")
        res = page.goto(url)
        if not res or res.status != 200:
            errors.append(f"Failed to load {url}: Status {res.status if res else 'None'}")
            continue
            
        page.wait_for_timeout(600)
        
        # Check active link in sidebar
        active_el = page.locator(f'#sidebar a.active[data-id="{active_id}"]')
        if active_el.count() == 0:
            errors.append(f"Active sidebar link not found for data-id='{active_id}' on {url}")
        else:
            print(f"  PASS: Active link '{active_id}' verified.")
            
        success_count += 1
        
    # Take key screenshots
    print("\nCapturing visual screenshots...")
    # 1. Admin Teaching Assignment Workload Balancer
    page.goto('http://127.0.0.1:3000/pages/admin/admin-teacher-assignments.html')
    page.wait_for_timeout(600)
    page.screenshot(path='scratch/teacher_assignments_desktop.png')
    
    # 2. Principal Homeroom Allocations
    page.goto('http://127.0.0.1:3000/pages/principal/principal-teacher-homeroom.html')
    page.wait_for_timeout(600)
    page.screenshot(path='scratch/teacher_homeroom_desktop.png')

    # 3. Principal Teacher Attendance
    page.goto('http://127.0.0.1:3000/pages/principal/principal-teacher-attendance.html')
    page.wait_for_timeout(600)
    page.screenshot(path='scratch/teacher_attendance_desktop.png')
    
    # 4. Mobile test: Teacher Verify on Mobile (390px)
    mobile_page = browser.new_page(viewport={"width": 390, "height": 844})
    mobile_page.goto('http://127.0.0.1:3000/pages/admin/admin-teacher-verify.html')
    mobile_page.wait_for_timeout(600)
    
    btn = mobile_page.locator('button.mobile-hamburger-btn[data-action="toggle-sidebar"]').first
    assert btn.count() > 0, "Mobile hamburger button missing!"
    btn.click()
    mobile_page.wait_for_timeout(400)
    
    sidebar = mobile_page.locator('#sidebar')
    assert 'open' in (sidebar.get_attribute('class') or ''), "Sidebar did not open upon hamburger click!"
    mobile_page.screenshot(path='scratch/teacher_verify_mobile_sidebar.png')
    print("  PASS: Mobile hamburger opened sidebar drawer successfully!")
    
    browser.close()

print(f"\nCompleted verification: {success_count}/{len(urls)} passed.")
if errors:
    print(f"Encountered {len(errors)} issues:")
    for err in errors:
        print("  - " + err)
    sys.exit(1)
else:
    print("ALL 16 TEACHER MANAGEMENT PAGES VERIFIED WITH ZERO ERRORS!")


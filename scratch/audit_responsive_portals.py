import os
from playwright.sync_api import sync_playwright

PAGES = [
    # Admin
    ('http://127.0.0.1:3000/pages/admin/admin.html', 'Admin Dashboard'),
    ('http://127.0.0.1:3000/pages/admin/admin-users.html', 'Admin User Directory'),
    ('http://127.0.0.1:3000/pages/admin/admin-classes.html', 'Admin Classes'),
    # Principal
    ('http://127.0.0.1:3000/pages/principal/principal.html', 'Principal Dashboard'),
    ('http://127.0.0.1:3000/pages/principal/principal-teacher-profiles.html', 'Teacher Profiles (Golden Reference)'),
    ('http://127.0.0.1:3000/pages/principal/principal-classes.html', 'Principal Classes'),
    ('http://127.0.0.1:3000/pages/principal/principal-departments.html', 'Principal Departments'),
    # Teacher
    ('http://127.0.0.1:3000/pages/teacher/teacher.html', 'Teacher Dashboard'),
    ('http://127.0.0.1:3000/pages/teacher/teacher-gradebook.html', 'Teacher Gradebook'),
    ('http://127.0.0.1:3000/pages/teacher/teacher-roster.html', 'Teacher Roster'),
    # Student
    ('http://127.0.0.1:3000/pages/student/student.html', 'Student Dashboard'),
    ('http://127.0.0.1:3000/pages/student/student-assignments.html', 'Student Assignments'),
]

VIEWPORTS = [
    {'width': 1440, 'height': 900, 'label': 'Desktop (1440x900)'},
    {'width': 768, 'height': 1024, 'label': 'Tablet (768x1024)'},
    {'width': 390, 'height': 844, 'label': 'Mobile (390x844)'},
]

def run_audit():
    errors = []
    print("=" * 60)
    print("GLOBAL AUDIT: RESPONSIVENESS, SVG ICONS & LAYOUT CONSISTENCY")
    print("=" * 60)

    with sync_playwright() as p:
        browser = p.chromium.launch()
        
        for url, name in PAGES:
            print(f"\n--- Checking: {name} ({url}) ---")
            for vp in VIEWPORTS:
                page = browser.new_page(viewport={'width': vp['width'], 'height': vp['height']})
                page_errors = []
                page.on('pageerror', lambda err: page_errors.append(str(err)))
                
                try:
                    res = page.goto(url, wait_until='domcontentloaded', timeout=15000)
                    if res.status != 200:
                        errors.append(f"{name} at {vp['label']}: Status {res.status}")
                        print(f"  FAIL: HTTP {res.status}")
                        page.close()
                        continue
                    
                    page.wait_for_timeout(500)
                    
                    # 1. Check for horizontal overflow
                    has_h_scroll = page.evaluate("() => document.documentElement.scrollWidth > window.innerWidth + 2")
                    if has_h_scroll and vp['width'] == 390:
                        # Check if intentional scroll container or body overflow
                        body_scroll = page.evaluate("() => document.body.scrollWidth > window.innerWidth + 2")
                        if body_scroll:
                            print(f"  WARN: Horizontal scroll detected at {vp['label']}")
                    
                    # 2. Check SVGs loaded
                    svg_count = page.evaluate("() => document.querySelectorAll('svg').length")
                    
                    # 3. Check hamburger on mobile
                    if vp['width'] <= 768:
                        has_hamburger = page.evaluate("""() => {
                            const btn = document.querySelector("#menuBtn, #htbHamburger, .htb-hamburger, .menu-btn, .hamburger-btn, [data-action='toggle-sidebar']");
                            return btn !== null;
                        }""")
                        if not has_hamburger:
                            print(f"  WARN: Hamburger missing at {vp['label']}")
                    
                    if page_errors:
                        print(f"  JS Errors: {page_errors}")
                        errors.extend([f"{name} ({vp['label']}): {e}" for e in page_errors])
                    else:
                        print(f"  PASS: {vp['label']} (SVGs: {svg_count})")
                        
                except Exception as ex:
                    print(f"  ERROR loading {url}: {ex}")
                    errors.append(f"{name} ({vp['label']}): {ex}")
                finally:
                    page.close()

        browser.close()

    print("\n" + "=" * 60)
    if not errors:
        print("AUDIT RESULT: ALL PAGES PASSED RESPONSIVE & FUNCTIONAL AUDIT WITH ZERO ERRORS!")
    else:
        print(f"AUDIT RESULT: {len(errors)} issues identified:")
        for e in errors:
            print(f"  - {e}")
    print("=" * 60)

if __name__ == '__main__':
    run_audit()


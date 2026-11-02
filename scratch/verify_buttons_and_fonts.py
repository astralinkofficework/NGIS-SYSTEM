from playwright.sync_api import sync_playwright

test_pages = [
    ('Student Dashboard', 'http://127.0.0.1:3000/pages/student/student.html'),
    ('Teacher Classes', 'http://127.0.0.1:3000/pages/teacher/teacher-classes.html?classId=cls-10a'),
    ('Teacher Submissions', 'http://127.0.0.1:3000/pages/teacher/teacher-submissions.html'),
    ('Teacher Lost & Found', 'http://127.0.0.1:3000/pages/teacher/teacher-lost-found.html'),
    ('Teacher Services', 'http://127.0.0.1:3000/pages/teacher/teacher-services.html'),
    ('Principal Dashboard', 'http://127.0.0.1:3000/pages/principal/principal.html'),
    ('Admin Classes', 'http://127.0.0.1:3000/pages/admin/admin-classes.html'),
    ('Admin Dashboard', 'http://127.0.0.1:3000/pages/admin/admin.html')
]

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={'width': 1280, 'height': 800})
    
    for name, url in test_pages:
        print(f'\n=== Testing: {name} ===')
        page.goto(url)
        page.wait_for_load_state('domcontentloaded')
        page.wait_for_timeout(300)
        
        # 1. Check Body Font
        body_font = page.evaluate('() => window.getComputedStyle(document.body).fontFamily')
        print(f'Body Font: {body_font[:60]}')
        
        # 2. Check Headings
        h1 = page.locator('h1, h2').first
        if h1.count() > 0:
            h_weight = h1.evaluate('el => window.getComputedStyle(el).fontWeight')
            h_text = h1.evaluate('el => el.textContent.trim()')[:30]
            print(f'Heading: "{h_text}" (weight: {h_weight})')
            
        # 3. Check Primary Buttons
        primary_btns = page.locator('.btn-primary, .ngis-btn-primary, .ov-btn-main, [data-role-action="primary"], #btnUploadAssignmentOrWork, #btnAddClass, #openReportModalBtn, #btnAddStudent, .sh-toolbar-new-btn').all()
        print(f'Primary buttons found: {len(primary_btns)}')
        for btn in primary_btns[:3]:
            if btn.is_visible():
                bg = btn.evaluate('el => window.getComputedStyle(el).backgroundColor')
                color = btn.evaluate('el => window.getComputedStyle(el).color')
                txt = btn.evaluate('el => el.textContent.trim()')[:25]
                print(f'  [Primary Btn] "{txt}": bg={bg}, text={color}')
                
        # 4. Check Secondary Buttons
        sec_btns = page.locator('.btn-secondary, .btn-ghost, .btn-outline, #btnExportCSV, .hamburger-btn, .category-filter-btn').all()
        for btn in sec_btns[:2]:
            if btn.is_visible():
                bg = btn.evaluate('el => window.getComputedStyle(el).backgroundColor')
                color = btn.evaluate('el => window.getComputedStyle(el).color')
                txt = btn.evaluate('el => el.textContent.trim()')[:25]
                print(f'  [Secondary Btn] "{txt}": bg={bg}, text={color}')
                
    # Capture screenshots of key pages
    page.goto('http://127.0.0.1:3000/pages/teacher/teacher-submissions.html')
    page.wait_for_load_state('networkidle')
    page.screenshot(path='C:/Users/oudom/.gemini/antigravity/brain/92720a74-07b3-40fa-91e3-a384311b91aa/buttons_submissions.png')
    
    page.goto('http://127.0.0.1:3000/pages/student/student.html')
    page.wait_for_load_state('networkidle')
    page.screenshot(path='C:/Users/oudom/.gemini/antigravity/brain/92720a74-07b3-40fa-91e3-a384311b91aa/buttons_student_dashboard.png')

    page.goto('http://127.0.0.1:3000/pages/principal/principal.html')
    page.wait_for_load_state('networkidle')
    page.screenshot(path='C:/Users/oudom/.gemini/antigravity/brain/92720a74-07b3-40fa-91e3-a384311b91aa/buttons_principal_dashboard.png')
    
    browser.close()
    print('\nAll checks and screenshots complete!')


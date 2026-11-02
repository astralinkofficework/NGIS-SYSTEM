from playwright.sync_api import sync_playwright

urls = [
    'http://127.0.0.1:3000/pages/teacher/teacher-classes.html?classId=cls-10a',
    'http://127.0.0.1:3000/pages/student/student.html',
    'http://127.0.0.1:3000/pages/teacher/teacher.html',
    'http://127.0.0.1:3000/pages/principal/principal.html',
    'http://127.0.0.1:3000/pages/admin/admin.html',
    'http://127.0.0.1:3000/pages/student/student-grades.html'
]

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    
    total_issues = 0
    total_checked = 0
    
    for url in urls:
        page.goto(url)
        page.wait_for_load_state('domcontentloaded')
        
        cards = page.locator('.card, .ws-card, .dept-card, .hub-card, .stat-card, .stat, .ov-profile, .ov-upcoming, .ov-deadlines, [class~="card"]').all()
        print(f'\nURL: {url} -> {len(cards)} card elements found')
        
        for c in cards[:10]:
            try:
                if not c.is_visible():
                    continue
                tag = c.evaluate('el => el.tagName')
                cls = c.evaluate('el => el.className')
                
                bg_0 = c.evaluate('el => window.getComputedStyle(el).backgroundColor')
                pseudo_b_0 = c.evaluate('el => window.getComputedStyle(el, "::before").content')
                pseudo_a_0 = c.evaluate('el => window.getComputedStyle(el, "::after").content')
                
                c.hover(force=True)
                
                bg_h = c.evaluate('el => window.getComputedStyle(el).backgroundColor')
                pseudo_b_h = c.evaluate('el => window.getComputedStyle(el, "::before").content')
                pseudo_a_h = c.evaluate('el => window.getComputedStyle(el, "::after").content')
                
                # Check for child icon badge hover background if any
                child_icons = c.locator('.w-9.h-9, [class*="rounded"], .ql-icon-wrap').all()
                for ic in child_icons[:2]:
                    if ic.is_visible():
                        ic_bg = ic.evaluate('el => window.getComputedStyle(el).backgroundColor')
                        # Check if child icon is colored like blue/teal/purple
                        # rgb(66, 79, 123) was the old brand-600
                        if '66, 79, 123' in ic_bg:
                            print(f'  [CHILD ICON COLOR FLIP] {ic_bg} inside {cls[:30]}')
                            total_issues += 1
                
                if bg_0 != bg_h:
                    print(f'  [FAIL BG] {tag}.{cls[:30]}: {bg_0} -> {bg_h}')
                    total_issues += 1
                if pseudo_b_h not in ['none', 'normal', '""', '']:
                    print(f'  [FAIL ::before] {tag}.{cls[:30]}: {pseudo_b_h}')
                    total_issues += 1
                if pseudo_a_h not in ['none', 'normal', '""', '']:
                    print(f'  [FAIL ::after] {tag}.{cls[:30]}: {pseudo_a_h}')
                    total_issues += 1
                
                total_checked += 1
            except Exception as e:
                pass
                
    print(f'\nVerification complete! Total cards checked: {total_checked}. Total issues: {total_issues}')
    browser.close()


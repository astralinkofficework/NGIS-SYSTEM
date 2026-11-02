from playwright.sync_api import sync_playwright

test_urls = [
    'http://127.0.0.1:3000/pages/teacher/teacher-classes.html?classId=cls-10a',
    'http://127.0.0.1:3000/pages/teacher/teacher.html',
    'http://127.0.0.1:3000/pages/principal/principal.html',
    'http://127.0.0.1:3000/pages/admin/admin.html',
    'http://127.0.0.1:3000/pages/student/student-calendar.html',
    'http://127.0.0.1:3000/pages/student/student-grades.html',
    'http://127.0.0.1:3000/pages/teacher/teacher-lessons.html',
    'http://127.0.0.1:3000/pages/shared/lessons.html',
    'http://127.0.0.1:3000/pages/admin/admin-departments.html'
]

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    
    for url in test_urls:
        print(f'\n=== Testing {url} ===')
        try:
            page.goto(url, timeout=10000)
            page.wait_for_load_state('domcontentloaded')
            page.wait_for_timeout(500)
            
            # Find interactive cards
            cards = page.locator('.card, .ws-card, .dept-card, .hub-card, .stat-card, .stat, .lesson-card, .cal-card, .club-card, .subj-card, .ov-profile, .ov-upcoming, .ov-deadlines, [class*="card"]').all()
            print(f'Found {len(cards)} card elements')
            
            tested = 0
            for card in cards[:15]:
                if not card.is_visible():
                    continue
                tag = card.evaluate('el => el.tagName')
                cls = card.evaluate('el => el.className')
                
                # Check style before hover
                bg_before = card.evaluate('el => window.getComputedStyle(el).backgroundColor')
                shadow_before = card.evaluate('el => window.getComputedStyle(el).boxShadow')
                before_pseudo = card.evaluate('el => window.getComputedStyle(el, "::before").content')
                after_pseudo = card.evaluate('el => window.getComputedStyle(el, "::after").content')
                
                # Check hover
                card.hover()
                bg_hover = card.evaluate('el => window.getComputedStyle(el).backgroundColor')
                shadow_hover = card.evaluate('el => window.getComputedStyle(el).boxShadow')
                before_pseudo_hover = card.evaluate('el => window.getComputedStyle(el, "::before").content')
                after_pseudo_hover = card.evaluate('el => window.getComputedStyle(el, "::after").content')
                
                # Check for background change or pseudo content
                if bg_before != bg_hover:
                    print(f'  [BG CHANGE] {tag}.{cls[:30]}: {bg_before} -> {bg_hover}')
                if before_pseudo_hover not in ['none', 'normal', '""', '']:
                    print(f'  [::before PSEUDO] {tag}.{cls[:30]}: {before_pseudo_hover}')
                if after_pseudo_hover not in ['none', 'normal', '""', '']:
                    print(f'  [::after PSEUDO] {tag}.{cls[:30]}: {after_pseudo_hover}')
                
                tested += 1
            print(f'Tested {tested} visible cards.')
        except Exception as e:
            print(f'Error testing {url}: {e}')
            
    browser.close()


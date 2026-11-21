import sys
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={'width': 1440, 'height': 900})
    page.goto('http://127.0.0.1:3000/pages/student/student-exams.html')
    page.wait_for_selector('.exw-roadmap-container')

    # 1. Verify title and subtitle
    title = page.locator('#roadmapTitle').inner_text()
    sub = page.locator('#roadmapSubtitle').inner_text()
    assert 'Subsequent Examinations Roadmap' in title, f'Title mismatch: {title}'
    assert 'Chronological progression through July 2026 evaluations' in sub, f'Subtitle mismatch: {sub}'

    # 2. Verify 5 queued badge
    badge = page.locator('#roadmapQueuedBadge').inner_text()
    assert '5' in badge and 'Queued' in badge, f'Badge mismatch: {badge}'

    # 3. Verify 5 rows and items
    rows = page.locator('.exw-roadmap-row').all()
    assert len(rows) == 5, f'Expected 5 rows, got {len(rows)}'
    
    # 4. Test search filter
    search_input = page.locator('#roadmapFilter')
    search_input.fill('Math')
    page.wait_for_timeout(300)
    filtered_rows = page.locator('.exw-roadmap-row').all()
    assert len(filtered_rows) == 1, f'Expected 1 row for Math, got {len(filtered_rows)}'
    
    # Reset filter
    search_input.fill('')
    page.wait_for_timeout(300)
    reset_rows = page.locator('.exw-roadmap-row').all()
    assert len(reset_rows) == 5, f'Expected 5 rows after reset, got {len(reset_rows)}'

    # 5. Verify no bold fonts (max font-weight 500)
    weights = page.evaluate('''() => {
        const els = document.querySelectorAll('.exw-roadmap-container *');
        const heavy = [];
        for (const el of els) {
            const fw = parseInt(window.getComputedStyle(el).fontWeight, 10);
            if (fw > 500) {
                heavy.push({ tag: el.tagName, cls: el.className, fw: fw });
            }
        }
        return heavy;
    }''')
    assert len(weights) == 0, f'Found heavy fonts: {weights}'

    # 6. Verify mobile viewport (375px)
    page_mob = browser.new_page(viewport={'width': 375, 'height': 812})
    page_mob.goto('http://127.0.0.1:3000/pages/student/student-exams.html')
    page_mob.wait_for_selector('.exw-roadmap-container')
    
    scroll_w = page_mob.evaluate('() => document.documentElement.scrollWidth')
    client_w = page_mob.evaluate('() => document.documentElement.clientWidth')
    assert scroll_w <= client_w, f'Horizontal scroll at 375px: scrollWidth={scroll_w}, clientWidth={client_w}'

    # Mobile hamburger button
    visible_btns = [b for b in page_mob.locator('[data-action="toggle-sidebar"]').all() if b.is_visible()]
    assert len(visible_btns) > 0, 'Mobile hamburger button must be visible'
    box = visible_btns[0].bounding_box()
    assert box['width'] >= 44 and box['height'] >= 44, f'Hamburger touch target too small: {box}'

    browser.close()

print('ALL STUDENT ROADMAP VERIFICATION TESTS PASSED SUCCESSFULLY!')

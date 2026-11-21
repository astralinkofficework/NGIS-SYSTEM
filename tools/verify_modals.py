from playwright.sync_api import sync_playwright

def test_all():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for w, h, name in [(1440, 900, 'desktop'), (1024, 768, 'tablet'), (375, 667, 'mobile')]:
            page = browser.new_page(viewport={'width': w, 'height': h})
            page.goto('http://127.0.0.1:3000/pages/admin/admin-student-profiles.html', wait_until='networkidle')
            page.locator('button[data-act="view"]').first.click()
            page.wait_for_selector('#profileModalInner', state='visible')
            page.wait_for_timeout(400)
            page.screenshot(path=f'profile_modal_reengineered_{name}.png')
            print(f'{name} modal screenshot captured')
            page.close()

        # Also test student-grades modal
        page = browser.new_page(viewport={'width': 1440, 'height': 900})
        page.goto('http://127.0.0.1:3000/pages/student/student-grades.html', wait_until='networkidle')
        page.locator('button[aria-label="View Report Card"]').first.click()
        page.wait_for_selector('#reportCardModal', state='visible')
        page.wait_for_timeout(300)
        page.screenshot(path='report_card_modal_1440.png')
        print('report_card_modal_1440.png captured')
        page.close()

        # Mobile report card modal
        page = browser.new_page(viewport={'width': 375, 'height': 667})
        page.goto('http://127.0.0.1:3000/pages/student/student-grades.html', wait_until='networkidle')
        page.locator('button[aria-label="View Report Card"]').first.click()
        page.wait_for_selector('#reportCardModal', state='visible')
        page.wait_for_timeout(300)
        page.screenshot(path='report_card_modal_375.png')
        print('report_card_modal_375.png captured')
        page.close()

        browser.close()

if __name__ == '__main__':
    test_all()

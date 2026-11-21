import os
from playwright.sync_api import sync_playwright

def verify():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={'width': 1440, 'height': 900})
        page.goto('http://127.0.0.1:3000/pages/student/student.html')
        page.wait_for_timeout(1000)
        
        # 1. Count rows
        rows = page.locator('#todayClassesList .workspace-row')
        row_count = rows.count()
        print(f"Today's Classes rows count: {row_count}")
        assert row_count == 7, f"Expected 7 rows, got {row_count}"
        
        # 2. Extract row details
        details = page.evaluate("""() => {
            const list = document.querySelectorAll('#todayClassesList .workspace-row');
            return Array.from(list).map(r => ({
                time: (r.querySelector('.workspace-row-time') || {}).innerText,
                subject: (r.querySelector('.workspace-row-heading') || {}).innerText,
                sub: (r.querySelector('.workspace-row-sub') || {}).innerText,
                cursor: window.getComputedStyle(r).cursor
            }));
        }""")
        for idx, d in enumerate(details, 1):
            print(f"  Row {idx}: {d['time']} | {d['subject']} | {d['sub']} | cursor: {d['cursor']}")
        
        # 3. Test click behavior: no navigation, no popup
        initial_url = page.url
        rows.first.click()
        page.wait_for_timeout(300)
        assert page.url == initial_url, "URL changed after click!"
        
        open_modals = page.locator('.is-open, dialog[open], .modal-open').count()
        print(f"Open modals after click: {open_modals}")
        assert open_modals == 0, f"Expected 0 open modals, found {open_modals}"
        
        # 4. Take screenshots
        # Card screenshot
        today_card = page.locator('.workspace-card').first
        today_card.screenshot(path='todays_classes_7rows_card.png')
        print("Captured todays_classes_7rows_card.png")
        
        # Full deck screenshot
        page.screenshot(path='student_dashboard_7rows_desktop.png')
        print("Captured student_dashboard_7rows_desktop.png")
        
        # Mobile view
        page.set_viewport_size({'width': 390, 'height': 844})
        page.wait_for_timeout(500)
        page.screenshot(path='student_dashboard_7rows_mobile.png')
        print("Captured student_dashboard_7rows_mobile.png")
        
        browser.close()

if __name__ == '__main__':
    verify()

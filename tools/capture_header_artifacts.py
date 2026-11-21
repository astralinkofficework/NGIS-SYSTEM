import os
from playwright.sync_api import sync_playwright

ARTIFACT_DIR = r"C:\Users\oudom\.gemini\antigravity\brain\f0e0db56-cd04-4f51-a7f8-40ba21b43536"

def capture():
    with sync_playwright() as p:
        b = p.chromium.launch()

        # 1. Default State (with live notifications red dot)
        p1 = b.new_page(viewport={'width': 375, 'height': 812})
        p1.goto('http://127.0.0.1:3000/pages/student/student-exams.html')
        p1.wait_for_selector('#ngisMobileHeader')
        p1.wait_for_timeout(600)
        p1.screenshot(path=os.path.join(ARTIFACT_DIR, 'mobile_header_default_375.png'))
        print("Captured mobile_header_default_375.png")

        # 2. Open Notifications Panel
        p1.locator('#ngisMobileNotifBtn').click()
        p1.wait_for_timeout(400)
        p1.screenshot(path=os.path.join(ARTIFACT_DIR, 'mobile_header_notif_panel_375.png'))
        print("Captured mobile_header_notif_panel_375.png")

        # 3. Open Language Dropdown
        p1.locator('#ngisMobileLangBtn').click()
        p1.wait_for_timeout(400)
        p1.screenshot(path=os.path.join(ARTIFACT_DIR, 'mobile_header_lang_dropdown_375.png'))
        print("Captured mobile_header_lang_dropdown_375.png")

        # 4. Open Sidebar Drawer (Hamburger transforms to Close icon)
        p1.locator('#ngisMobileMenuBtn').click()
        p1.wait_for_timeout(500)
        p1.screenshot(path=os.path.join(ARTIFACT_DIR, 'mobile_header_drawer_open_375.png'))
        print("Captured mobile_header_drawer_open_375.png")
        p1.close()

        # 5. Desktop Isolation at 1440px
        p2 = b.new_page(viewport={'width': 1440, 'height': 900})
        p2.goto('http://127.0.0.1:3000/pages/student/student-exams.html')
        p2.wait_for_timeout(500)
        p2.screenshot(path=os.path.join(ARTIFACT_DIR, 'mobile_header_desktop_1440.png'))
        print("Captured mobile_header_desktop_1440.png")
        p2.close()

        b.close()
    print("All artifact screenshots captured successfully!")

if __name__ == '__main__':
    capture()

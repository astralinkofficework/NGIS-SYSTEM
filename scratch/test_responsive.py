from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    for w in [1440, 1280, 1100, 1024, 900, 800, 768, 640, 500, 375]:
        page = browser.new_page(viewport={'width': w, 'height': 800})
        page.goto('http://127.0.0.1:3000/pages/principal/principal-classes.html')
        page.wait_for_timeout(300)
        box_grade = page.locator('#gradeFilter').bounding_box()
        box_campus = page.locator('#campusFilter').bounding_box()
        box_status = page.locator('#statusFilter').bounding_box()
        box_search = page.locator('#classSearchInput').bounding_box()
        print(f"Width {w}: Search Y={box_search['y']}, Grade Y={box_grade['y']}, Campus Y={box_campus['y']}, Status Y={box_status['y']}")
        page.close()
    browser.close()


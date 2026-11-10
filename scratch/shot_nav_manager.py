"""Capture screenshots of the Global Sidebar Manager for visual review."""
from playwright.sync_api import sync_playwright

URL = "http://127.0.0.1:3000/pages/admin/admin-dashboard-content.html"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)

    for name, w, h in [("sgm_desktop", 1600, 950), ("sgm_tablet", 1024, 900), ("sgm_mobile", 400, 900)]:
        page = browser.new_page(viewport={"width": w, "height": h})
        page.goto(URL, wait_until="networkidle", timeout=60000)
        page.wait_for_timeout(1500)
        try:
            page.wait_for_selector("#sgmTree .sgm-node", timeout=15000)
            page.locator("#sgmTree .sgm-node").first.click()
            page.wait_for_timeout(400)
        except Exception as e:
            print("warn:", e)
        page.screenshot(path="scratch/%s.png" % name, full_page=False)
        print("saved scratch/%s.png" % name)
        page.close()

    browser.close()

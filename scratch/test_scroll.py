from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={'width': 1600, 'height': 900})
    page.goto("http://127.0.0.1:3000/pages/principal/principal-attendance.html", wait_until="networkidle")

    # Take screenshot before any clicks
    page.screenshot(path="C:/Users/oudom/.gemini/antigravity/brain/8fd19b10-a09a-43d8-a122-cb4a75dc0ff6/attendance_redesigned_desktop.png")
    print("Clean desktop screenshot captured at scrollLeft 0!")
    browser.close()

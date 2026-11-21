from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={'width': 375, 'height': 812})
    page.goto('http://127.0.0.1:3000/pages/admin/admin-classes.html', wait_until='networkidle')
    hamb = page.locator('[data-action="toggle-sidebar"]')
    count = hamb.count()
    print('Found count of toggle-sidebar:', count)
    for i in range(count):
        el = hamb.nth(i)
        print(f'Item {i}: visible = {el.is_visible()}, box = {el.bounding_box()}')
    browser.close()

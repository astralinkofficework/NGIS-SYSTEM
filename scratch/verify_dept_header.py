from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={'width': 1280, 'height': 800})
    page.goto('http://127.0.0.1:3000/pages/principal/principal-departments.html')
    page.wait_for_selector('h1')
    page.screenshot(path='C:/Users/oudom/.gemini/antigravity/brain/8fd19b10-a09a-43d8-a122-cb4a75dc0ff6/departments_header_clean.png')
    btn_exists = page.locator('button', has_text='+ Add Department').count() > 0
    print('Add Department button exists in DOM:', btn_exists)
    browser.close()


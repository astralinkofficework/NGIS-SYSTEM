from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={'width': 1440, 'height': 900})
    page.goto('http://127.0.0.1:3000/pages/principal/principal-classes.html')
    
    headers = page.locator('header').all()
    print('1440px headers count:', len(headers))
    for idx, h in enumerate(headers):
        box = h.bounding_box()
        cls = h.get_attribute('class')
        print(f'  Header {idx}: class="{cls}", box={box}')
        
    page.set_viewport_size({'width': 390, 'height': 844})
    page.wait_for_timeout(300)
    headers = page.locator('header').all()
    print('390px headers count:', len(headers))
    for idx, h in enumerate(headers):
        box = h.bounding_box()
        cls = h.get_attribute('class')
        print(f'  Header {idx}: class="{cls}", box={box}')
        
    browser.close()


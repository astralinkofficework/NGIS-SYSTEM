from playwright.sync_api import sync_playwright

viewports = [
    ('mobile_375', 375, 667),
    ('mobile_390', 390, 844),
    ('tablet_768', 768, 1024),
    ('desktop_1280', 1280, 800)
]

with sync_playwright() as p:
    browser = p.chromium.launch()
    for name, w, h in viewports:
        page = browser.new_page(viewport={'width': w, 'height': h})
        page.goto('http://127.0.0.1:3000/pages/principal/principal-departments.html')
        page.wait_for_selector('[data-purpose="filtering-controls"]')
        filter_section = page.locator('[data-purpose="filtering-controls"]')
        box = filter_section.bounding_box()
        # check page overflow
        scroll_width = page.evaluate('document.documentElement.scrollWidth')
        client_width = page.evaluate('document.documentElement.clientWidth')
        has_overflow = scroll_width > client_width
        print(f"departments @ {name} ({w}px): filter_width={box['width']:.1f}, scrollW={scroll_width}, clientW={client_width}, overflow={has_overflow}")
        filter_section.screenshot(path=f'C:/Users/oudom/.gemini/antigravity/brain/8fd19b10-a09a-43d8-a122-cb4a75dc0ff6/filter_dept_{name}.png')
        
        # also check principal-classes
        page.goto('http://127.0.0.1:3000/pages/principal/principal-classes.html')
        page.wait_for_selector('[data-purpose="filtering-controls"]')
        filter_section2 = page.locator('[data-purpose="filtering-controls"]')
        box2 = filter_section2.bounding_box()
        scroll_width2 = page.evaluate('document.documentElement.scrollWidth')
        client_width2 = page.evaluate('document.documentElement.clientWidth')
        has_overflow2 = scroll_width2 > client_width2
        print(f"classes @ {name} ({w}px): filter_width={box2['width']:.1f}, scrollW={scroll_width2}, clientW={client_width2}, overflow={has_overflow2}")
        filter_section2.screenshot(path=f'C:/Users/oudom/.gemini/antigravity/brain/8fd19b10-a09a-43d8-a122-cb4a75dc0ff6/filter_classes_{name}.png')
        page.close()
    browser.close()


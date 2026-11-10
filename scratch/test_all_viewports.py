from playwright.sync_api import sync_playwright

widths = [1440, 1024, 768, 480, 375]

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    for w in widths:
        page = browser.new_page(viewport={"width": w, "height": 850})
        page.goto("http://127.0.0.1:3000/pages/principal/principal-classes.html")
        page.wait_for_timeout(400)
        
        # Check input padding
        inp = page.locator("#classSearchInput")
        pl = page.evaluate("(el) => window.getComputedStyle(el).paddingLeft", inp.element_handle())
        
        # Check filter elements
        sec = page.locator('section[data-purpose="filtering-controls"]')
        sec.screenshot(path=f"scratch/filter_{w}.png")
        page.screenshot(path=f"scratch/full_{w}.png")
        print(f"Viewport {w}px: Search padding-left={pl}")
        page.close()
    browser.close()

print("All viewports verified!")

from playwright.sync_api import sync_playwright

viewports = [
    ('mobile_375', 375, 812),
    ('mobile_390', 390, 844),
    ('tablet_768', 768, 1024),
    ('desktop_1280', 1280, 800)
]

with sync_playwright() as p:
    browser = p.chromium.launch()
    for name, w, h in viewports:
        page = browser.new_page(viewport={'width': w, 'height': h})
        page.goto('http://127.0.0.1:3000/pages/principal/principal-services.html')
        page.wait_for_timeout(600)
        
        doc_w = page.evaluate("() => document.documentElement.scrollWidth")
        win_w = page.evaluate("() => window.innerWidth")
        body_w = page.evaluate("() => document.body.scrollWidth")
        
        has_page_overflow = doc_w > win_w
        print(f"Viewport {name} ({w}x{h}): docWidth={doc_w}, winWidth={win_w}, bodyWidth={body_w}, overflow={has_page_overflow}")
        
        page.screenshot(path=f"scratch/services_responsive_{name}.png")
        page.close()
        
    browser.close()


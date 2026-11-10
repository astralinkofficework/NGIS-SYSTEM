from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    page.goto("http://127.0.0.1:3000/pages/principal/principal-classes.html")
    page.wait_for_timeout(1000)
    page.screenshot(path="scratch/ref_classes_1440.png")

    page.set_viewport_size({"width": 390, "height": 844})
    page.wait_for_timeout(500)
    page.screenshot(path="scratch/ref_classes_390.png")

    browser.close()
print("Done ref_classes screenshots")


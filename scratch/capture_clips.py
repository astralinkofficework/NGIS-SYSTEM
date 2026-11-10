from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1280, "height": 900})
    page.goto("http://127.0.0.1:3000/pages/principal/principal-classes.html")
    page.wait_for_timeout(500)
    
    # Clip filter bar
    bar = page.locator('section[data-purpose="filtering-controls"]')
    bar.screenshot(path="scratch/filter_bar_classes.png")
    
    # Clip telemetry cards
    cards = page.locator('section[data-purpose="metrics-telemetry"]')
    cards.screenshot(path="scratch/telemetry_cards_classes.png")
    
    # Full page
    page.screenshot(path="scratch/classes_desktop.png")
    browser.close()

print("Successfully captured screenshots!")


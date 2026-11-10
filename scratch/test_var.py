from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    page.goto("http://127.0.0.1:3000/pages/principal/principal.html")
    page.wait_for_timeout(500)
    
    # Check why getComputedStyle returned rgb(255, 255, 255)
    bg = page.evaluate("""() => {
        const sb = document.querySelector('#sidebar');
        return {
            computedBg: window.getComputedStyle(sb).backgroundColor,
            computedColor: window.getComputedStyle(sb).color,
            varMidnight: window.getComputedStyle(sb).getPropertyValue('--color-midnight'),
            varMidnightRoot: window.getComputedStyle(document.documentElement).getPropertyValue('--color-midnight')
        };
    }""")
    print("Direct check:", bg)
    browser.close()


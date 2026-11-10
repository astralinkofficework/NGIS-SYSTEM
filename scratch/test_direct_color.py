from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    page.goto("http://127.0.0.1:3000/pages/principal/principal.html")
    page.wait_for_timeout(500)
    
    res = page.evaluate("""() => {
        const sb = document.querySelector('#sidebar');
        const before = window.getComputedStyle(sb).backgroundColor;
        sb.style.setProperty('background-color', '#021024', 'important');
        const after = window.getComputedStyle(sb).backgroundColor;
        return { before, after };
    }""")
    print("Result:", res)
    browser.close()


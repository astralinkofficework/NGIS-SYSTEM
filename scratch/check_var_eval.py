from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    page.goto("http://127.0.0.1:3000/pages/principal/principal.html")
    page.wait_for_timeout(500)
    
    vals = page.evaluate("""() => {
        const root = window.getComputedStyle(document.documentElement);
        const sb = document.querySelector('#sidebar');
        const sbStyle = window.getComputedStyle(sb);
        return {
            '--color-midnight': root.getPropertyValue('--color-midnight'),
            '--color-deep-blue': root.getPropertyValue('--color-deep-blue'),
            'sidebar-bg': sbStyle.backgroundColor,
            'sidebar-color': sbStyle.color,
            'sidebar-inline-style': sb.getAttribute('style')
        };
    }""")
    print("Computed values:", vals)
    browser.close()


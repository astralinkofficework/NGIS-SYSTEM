from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    page.goto("http://127.0.0.1:3000/pages/principal/principal.html")
    page.wait_for_timeout(500)
    
    info = page.evaluate("""() => {
        const sb = document.querySelector('#sidebar');
        if (!sb) return 'No sidebar';
        const styles = window.getComputedStyle(sb);
        return {
            bg: styles.backgroundColor,
            color: styles.color,
            classList: Array.from(sb.classList),
            // check matched rules
        };
    }""")
    print("Sidebar Info:", info)
    browser.close()


from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={'width': 390, 'height': 844})
    page.goto('http://127.0.0.1:3000/pages/principal/principal.html', wait_until='domcontentloaded')
    page.wait_for_timeout(500)
    
    info = page.evaluate('''() => {
        const btns = Array.from(document.querySelectorAll('[data-action="toggle-sidebar"], #menuBtn, .hamburger-btn, .htb-hamburger, #htbHamburger'));
        return btns.map(b => {
            const style = window.getComputedStyle(b);
            const rect = b.getBoundingClientRect();
            return {
                id: b.id,
                className: b.className,
                display: style.display,
                visibility: style.visibility,
                opacity: style.opacity,
                rect: { width: rect.width, height: rect.height, top: rect.top, left: rect.left },
                parent: b.parentElement ? b.parentElement.tagName + '.' + b.parentElement.className : null
            };
        });
    }''')
    print("Found hamburger buttons:", info)
    browser.close()


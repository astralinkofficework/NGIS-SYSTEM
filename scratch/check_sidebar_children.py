from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    page.goto("http://127.0.0.1:3000/pages/principal/principal.html")
    page.wait_for_timeout(500)
    
    data = page.evaluate("""() => {
        const sb = document.querySelector('#sidebar');
        const brand = document.querySelector('.side-brand');
        const nav = document.querySelector('.side-nav');
        const link = document.querySelector('.nav-link');
        const activeLink = document.querySelector('.nav-link.active');
        
        return {
            sb: sb ? {
                tag: sb.tagName,
                id: sb.id,
                bg: window.getComputedStyle(sb).backgroundColor,
                color: window.getComputedStyle(sb).color
            } : null,
            brand: brand ? {
                bg: window.getComputedStyle(brand).backgroundColor,
                color: window.getComputedStyle(brand).color
            } : null,
            nav: nav ? {
                bg: window.getComputedStyle(nav).backgroundColor
            } : null,
            link: link ? {
                bg: window.getComputedStyle(link).backgroundColor,
                color: window.getComputedStyle(link).color
            } : null,
            activeLink: activeLink ? {
                bg: window.getComputedStyle(activeLink).backgroundColor,
                color: window.getComputedStyle(activeLink).color
            } : null
        };
    }""")
    print("Element Backgrounds:", data)
    browser.close()


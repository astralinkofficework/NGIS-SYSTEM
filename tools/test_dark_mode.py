from playwright.sync_api import sync_playwright

url = "http://127.0.0.1:3000/pages/admin/admin-security.html"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    page.goto(url, wait_until="networkidle")
    page.wait_for_timeout(300)
    
    page.evaluate("document.documentElement.setAttribute('data-theme', 'dark');")
    page.wait_for_timeout(200)
    
    normal = page.evaluate("""() => {
        const topbar = document.querySelector('.hero-topbar');
        const notif = document.getElementById('htbNotifBtn');
        const cal = document.getElementById('htbCalBtn');
        return {
            inlineBg: topbar ? topbar.style.backgroundColor : null,
            computedBg: topbar ? window.getComputedStyle(topbar).backgroundColor : null,
            notifColor: notif ? window.getComputedStyle(notif).color : null,
            calColor: cal ? window.getComputedStyle(cal).color : null,
            isStuck: topbar ? topbar.classList.contains('ngis-sticky-fixed') : null
        };
    }""")
    print("Dark NORMAL:", normal)
    
    page.evaluate("window.scrollTo(0, 300);")
    page.wait_for_timeout(400)
    
    scrolled = page.evaluate("""() => {
        const topbar = document.querySelector('.hero-topbar');
        const notif = document.getElementById('htbNotifBtn');
        const cal = document.getElementById('htbCalBtn');
        return {
            inlineBg: topbar ? topbar.style.backgroundColor : null,
            computedBg: topbar ? window.getComputedStyle(topbar).backgroundColor : null,
            notifColor: notif ? window.getComputedStyle(notif).color : null,
            calColor: cal ? window.getComputedStyle(cal).color : null,
            isStuck: topbar ? topbar.classList.contains('ngis-sticky-fixed') : null
        };
    }""")
    print("Dark SCROLLED:", scrolled)
    browser.close()

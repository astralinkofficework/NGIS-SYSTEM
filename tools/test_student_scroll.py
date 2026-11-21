from playwright.sync_api import sync_playwright

url = "http://127.0.0.1:3000/pages/student/student.html"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    page.goto(url, wait_until="networkidle")
    page.wait_for_timeout(500)
    
    # Normal state
    normal = page.evaluate("""() => {
        const notif = document.getElementById('htbNotifBtn');
        const topbar = document.querySelector('.hero-topbar');
        return {
            notifColor: notif ? window.getComputedStyle(notif).color : null,
            topbarBg: topbar ? window.getComputedStyle(topbar).backgroundColor : null
        };
    }""")
    print("Normal state:", normal)
    
    # Scroll 400px
    page.evaluate("window.scrollTo(0, 400);")
    page.wait_for_timeout(500)
    
    scrolled = page.evaluate("""() => {
        const notif = document.getElementById('htbNotifBtn');
        const topbar = document.querySelector('.hero-topbar');
        return {
            notifColor: notif ? window.getComputedStyle(notif).color : null,
            topbarBg: topbar ? window.getComputedStyle(topbar).backgroundColor : null,
            topbarClass: topbar ? topbar.className : null
        };
    }""")
    print("Scrolled state:", scrolled)
    
    browser.close()

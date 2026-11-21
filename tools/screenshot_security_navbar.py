import sys
from playwright.sync_api import sync_playwright

url = "http://127.0.0.1:3000/pages/admin/admin-security.html"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    
    # 1. Desktop 1280x1024 (matching the user's uploaded screenshot resolution!)
    context = browser.new_context(viewport={"width": 1280, "height": 1024})
    page = context.new_page()
    page.goto(url, wait_until="networkidle", timeout=15000)
    page.wait_for_timeout(1000)
    
    # Check topbar computed styles
    data = page.evaluate("""() => {
        const hero = document.getElementById('heroBanner');
        const topbar = hero ? hero.querySelector('.hero-topbar') : null;
        const brand = hero ? hero.querySelector('.htb-brand-wrap') : null;
        const cal = document.getElementById('htbCalBtn');
        const notif = document.getElementById('htbNotifBtn');
        const burger = document.getElementById('htbHamburger');
        
        function styleOf(el) {
            if (!el) return null;
            const cs = window.getComputedStyle(el);
            return {
                bg: cs.backgroundColor,
                color: cs.color,
                border: cs.border,
                boxShadow: cs.boxShadow,
                display: cs.display,
                visibility: cs.visibility,
                rect: el.getBoundingClientRect()
            };
        }
        
        return {
            bodyBg: window.getComputedStyle(document.body).backgroundColor,
            hero: styleOf(hero),
            topbar: styleOf(topbar),
            cal: styleOf(cal),
            notif: styleOf(notif),
            burger: styleOf(burger)
        };
    }""")
    print("Desktop 1280x1024 Evaluation:", data)
    
    # Take screenshot of the top header area
    page.screenshot(path="C:/Users/oudom/.gemini/antigravity/brain/f0e0db56-cd04-4f51-a7f8-40ba21b43536/test_security_desktop_1280.png")
    
    # Scroll and take screenshot
    page.evaluate("window.scrollTo(0, 300);")
    page.wait_for_timeout(500)
    scrolled_data = page.evaluate("""() => {
        const stuck = document.querySelector('.ngis-sticky-fixed');
        if (!stuck) return null;
        const cs = window.getComputedStyle(stuck);
        return {
            tag: stuck.tagName,
            className: stuck.className,
            bg: cs.backgroundColor,
            borderBottom: cs.borderBottom,
            boxShadow: cs.boxShadow
        };
    }""")
    print("Desktop Scrolled Stuck State:", scrolled_data)
    page.screenshot(path="C:/Users/oudom/.gemini/antigravity/brain/f0e0db56-cd04-4f51-a7f8-40ba21b43536/test_security_desktop_scrolled.png")
    context.close()
    
    # 2. Mobile 375x667
    context_m = browser.new_context(viewport={"width": 375, "height": 667})
    page_m = context_m.new_page()
    page_m.goto(url, wait_until="networkidle", timeout=15000)
    page_m.wait_for_timeout(1000)
    
    mobile_data = page_m.evaluate("""() => {
        const mAppbar = document.querySelector('.mobile-appbar');
        const burger = document.querySelector('.mobile-appbar [data-action="toggle-sidebar"], .mobile-hamburger-btn');
        return {
            appbar: mAppbar ? window.getComputedStyle(mAppbar).backgroundColor : null,
            burgerVisible: burger ? window.getComputedStyle(burger).display !== 'none' : false,
            burgerRect: burger ? burger.getBoundingClientRect() : null
        };
    }""")
    print("Mobile 375x667 Evaluation:", mobile_data)
    page_m.screenshot(path="C:/Users/oudom/.gemini/antigravity/brain/f0e0db56-cd04-4f51-a7f8-40ba21b43536/test_security_mobile_375.png")
    context_m.close()
    
    browser.close()
    print("Screenshots saved successfully.")

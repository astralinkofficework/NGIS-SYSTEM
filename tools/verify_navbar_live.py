import sys
import time
from playwright.sync_api import sync_playwright

test_urls = [
    "http://127.0.0.1:3000/pages/admin/admin-security.html",
    "http://127.0.0.1:3000/pages/admin/admin.html",
    "http://127.0.0.1:3000/pages/student/student.html",
    "http://127.0.0.1:3000/pages/teacher/teacher.html",
    "http://127.0.0.1:3000/pages/principal/principal.html",
    "http://127.0.0.1:3000/pages/admin/admin-classes.html",
    "http://127.0.0.1:3000/pages/shared/announcements.html"
]

viewports = [
    {"name": "Desktop 1440x900", "width": 1440, "height": 900},
    {"name": "Tablet 768x1024", "width": 768, "height": 1024},
    {"name": "Mobile 375x667", "width": 375, "height": 667}
]

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    
    for url in test_urls:
        print(f"\n==================================================")
        print(f"Testing URL: {url}")
        print(f"==================================================")
        
        for vp in viewports:
            context = browser.new_context(viewport={"width": vp["width"], "height": vp["height"]})
            page = context.new_page()
            
            try:
                page.goto(url, wait_until="networkidle", timeout=15000)
            except Exception as e:
                print(f"[{vp['name']}] Navigation timeout or error: {e}")
                # Try with domcontentloaded
                try:
                    page.goto(url, wait_until="domcontentloaded", timeout=10000)
                except Exception as e2:
                    print(f"[{vp['name']}] Second try failed: {e2}")
                    context.close()
                    continue
            
            page.wait_for_timeout(800)
            
            # Inspect header and topbar
            eval_result = page.evaluate("""() => {
                const hero = document.getElementById('heroBanner');
                const topbar = hero ? hero.querySelector('.hero-topbar') : null;
                const mobileAppbar = document.querySelector('.mobile-appbar, #mobileMainAppbar');
                const activeSticky = document.querySelector('.ngis-sticky-active');
                
                function getInfo(el) {
                    if (!el) return null;
                    const style = window.getComputedStyle(el);
                    const rect = el.getBoundingClientRect();
                    return {
                        tag: el.tagName,
                        id: el.id,
                        className: el.className,
                        bg: style.backgroundColor,
                        bgImage: style.backgroundImage,
                        borderBottom: style.borderBottom,
                        boxShadow: style.boxShadow,
                        display: style.display,
                        visibility: style.visibility,
                        height: rect.height,
                        width: rect.width,
                        top: rect.top
                    };
                }
                
                // Check icons
                const icons = [];
                const iconButtons = document.querySelectorAll('#htbHamburger, #htbCalBtn, #htbNotifBtn, .htb-ctrl-btn, [data-action="toggle-sidebar"]');
                iconButtons.forEach(btn => {
                    const style = window.getComputedStyle(btn);
                    const svg = btn.querySelector('svg');
                    const mi = btn.querySelector('.mi');
                    const badge = btn.querySelector('.htb-ctrl-badge, .htb-badge');
                    icons.push({
                        id: btn.id || btn.className.split(' ')[0],
                        color: style.color,
                        bg: style.backgroundColor,
                        hasSvg: !!svg,
                        svgSize: svg ? `${svg.getBoundingClientRect().width}x${svg.getBoundingClientRect().height}` : null,
                        miText: mi ? (mi.innerText || mi.textContent || '').trim() : null,
                        badgeText: badge ? (badge.innerText || badge.textContent || '').trim() : null
                    });
                });
                
                return {
                    bodyBg: window.getComputedStyle(document.body).backgroundColor,
                    hero: getInfo(hero),
                    topbar: getInfo(topbar),
                    mobileAppbar: getInfo(mobileAppbar),
                    activeSticky: getInfo(activeSticky),
                    icons: icons
                };
            }""")
            
            print(f"[{vp['name']}] Results:")
            print(f"  Body BG: {eval_result['bodyBg']}")
            if eval_result.get('topbar'):
                print(f"  Topbar BG: {eval_result['topbar']['bg']} (display: {eval_result['topbar']['display']}, h: {eval_result['topbar']['height']:.1f}px, border: {eval_result['topbar']['borderBottom']})")
            if eval_result.get('mobileAppbar'):
                print(f"  MobileAppbar BG: {eval_result['mobileAppbar']['bg']} (display: {eval_result['mobileAppbar']['display']}, h: {eval_result['mobileAppbar']['height']:.1f}px)")
            if eval_result.get('activeSticky'):
                print(f"  ActiveSticky BG: {eval_result['activeSticky']['bg']} (border: {eval_result['activeSticky']['borderBottom']})")
            
            # Print icon info
            print(f"  Icons ({len(eval_result['icons'])}):")
            for ic in eval_result['icons'][:6]:
                print(f"    - {ic['id']}: color={ic['color']}, hasSvg={ic['hasSvg']} ({ic['svgSize']}), badge={ic['badgeText']}")
            
            # Now scroll down 200px and check sticky behavior
            page.evaluate("window.scrollTo(0, 300);")
            page.wait_for_timeout(400)
            
            scrolled_result = page.evaluate("""() => {
                const activeSticky = document.querySelector('.ngis-sticky-active.ngis-sticky-fixed, .ngis-sticky-fixed');
                if (!activeSticky) return null;
                const style = window.getComputedStyle(activeSticky);
                return {
                    className: activeSticky.className,
                    bg: style.backgroundColor,
                    borderBottom: style.borderBottom,
                    boxShadow: style.boxShadow
                };
            }""")
            
            if scrolled_result:
                print(f"  Scrolled Sticky State: BG={scrolled_result['bg']}, border={scrolled_result['borderBottom']}, shadow={scrolled_result['boxShadow']}")
            else:
                print("  Scrolled Sticky State: none detected as .ngis-sticky-fixed")
                
            context.close()
            
    browser.close()

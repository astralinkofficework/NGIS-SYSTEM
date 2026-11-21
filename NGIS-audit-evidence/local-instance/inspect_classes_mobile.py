from playwright.sync_api import sync_playwright
import json

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 390, "height": 844})
    page.goto("http://127.0.0.1:3000/pages/admin/admin-classes.html")
    page.wait_for_timeout(1000)
    
    classes_mobile = page.evaluate('''() => {
        const header = document.querySelector('header');
        const heroBanner = document.querySelector('#heroBanner');
        const sidebar = document.querySelector('.sidebar, #sidebar');
        const main = document.querySelector('.main, main');
        
        return {
            headerOuterHTML: header ? header.outerHTML.slice(0, 500) : 'NONE',
            heroBannerOuterHTML: heroBanner ? heroBanner.outerHTML.slice(0, 500) : 'NONE',
            sidebarStyle: sidebar ? {
                display: window.getComputedStyle(sidebar).display,
                position: window.getComputedStyle(sidebar).position,
                transform: window.getComputedStyle(sidebar).transform,
                width: window.getComputedStyle(sidebar).width
            } : 'NONE'
        };
    }''')
    print("Classes mobile data:", json.dumps(classes_mobile, indent=2))
    
    # Test hamburger click on classes
    btn = page.query_selector('[data-action="toggle-sidebar"]')
    if btn:
        btn.click()
        page.wait_for_timeout(500)
        page.screenshot(path="classes_mobile_drawer_open.png")
        classes_drawer = page.evaluate('''() => {
            const sidebar = document.querySelector('.sidebar, #sidebar');
            const backdrop = document.querySelector('.sidebar-backdrop, .sidebar-scrim, [data-action="close-sidebar"]');
            return {
                sidebarClass: sidebar ? sidebar.className : '',
                sidebarTransform: sidebar ? window.getComputedStyle(sidebar).transform : '',
                sidebarWidth: sidebar ? window.getComputedStyle(sidebar).width : '',
                sidebarLeft: sidebar ? window.getComputedStyle(sidebar).left : '',
                backdropFound: backdrop !== null,
                backdropVisible: backdrop ? window.getComputedStyle(backdrop).display : 'NONE'
            };
        }''')
        print("Classes drawer open:", json.dumps(classes_drawer, indent=2))
    
    browser.close()

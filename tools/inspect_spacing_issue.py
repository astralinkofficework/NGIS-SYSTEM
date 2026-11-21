import os
from playwright.sync_api import sync_playwright

artifact_dir = r"C:\Users\oudom\.gemini\antigravity\brain\f0e0db56-cd04-4f51-a7f8-40ba21b43536"

with sync_playwright() as p:
    browser = p.chromium.launch()
    
    for vp_name, w, h in [('desktop', 1440, 900), ('mobile', 375, 812), ('tablet', 768, 1024)]:
        for page_name, url in [
            ('principal_attendance', 'http://127.0.0.1:3000/pages/principal/principal-attendance.html'),
            ('principal_dash', 'http://127.0.0.1:3000/pages/principal/principal.html'),
            ('student_exams', 'http://127.0.0.1:3000/pages/student/student-exams.html'),
            ('admin_dash', 'http://127.0.0.1:3000/pages/admin/admin.html')
        ]:
            page = browser.new_page(viewport={'width': w, 'height': h})
            page.goto(url)
            page.wait_for_timeout(1000)
            
            details = page.evaluate("""() => {
                const nav = document.getElementById('ngisGlobalNavbar');
                const sidebar = document.getElementById('sidebar');
                const main = document.querySelector('main, .main-content, .page, #mainContent');
                const hero = document.querySelector('#heroBanner, .hero-banner, .dashboard-hero');
                
                return {
                    nav: nav ? {
                        box: nav.getBoundingClientRect(),
                        style: {
                            position: window.getComputedStyle(nav).position,
                            top: window.getComputedStyle(nav).top,
                            marginTop: window.getComputedStyle(nav).marginTop,
                            paddingTop: window.getComputedStyle(nav).paddingTop,
                            zIndex: window.getComputedStyle(nav).zIndex
                        },
                        parent: nav.parentElement ? nav.parentElement.tagName + '.' + nav.parentElement.className : null
                    } : null,
                    sidebar: sidebar ? {
                        box: sidebar.getBoundingClientRect(),
                        display: window.getComputedStyle(sidebar).display,
                        position: window.getComputedStyle(sidebar).position,
                        top: window.getComputedStyle(sidebar).top
                    } : null,
                    main: main ? {
                        box: main.getBoundingClientRect(),
                        style: {
                            marginTop: window.getComputedStyle(main).marginTop,
                            paddingTop: window.getComputedStyle(main).paddingTop,
                            position: window.getComputedStyle(main).position,
                            top: window.getComputedStyle(main).top
                        }
                    } : null,
                    hero: hero ? {
                        box: hero.getBoundingClientRect(),
                        style: {
                            marginTop: window.getComputedStyle(hero).marginTop,
                            paddingTop: window.getComputedStyle(hero).paddingTop
                        }
                    } : null,
                    bodyPadTop: window.getComputedStyle(document.body).paddingTop,
                    bodyMarginTop: window.getComputedStyle(document.body).marginTop
                };
            }""")
            
            print(f"=== {page_name} [{vp_name}] ===")
            print("  Nav:", details["nav"])
            print("  Sidebar:", details["sidebar"])
            print("  Main:", details["main"])
            print("  Hero:", details["hero"])
            print(f"  Body pad top: {details['bodyPadTop']}, margin top: {details['bodyMarginTop']}")
            
            # Screenshot top area
            page.screenshot(path=os.path.join(artifact_dir, f"debug_spacing_{page_name}_{vp_name}.png"), clip={"x": 0, "y": 0, "width": w, "height": min(h, 450)})
            page.close()
            
    browser.close()

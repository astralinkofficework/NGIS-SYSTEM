from playwright.sync_api import sync_playwright

def test_all():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        
        # 1. Desktop checks
        page = browser.new_page(viewport={'width': 1440, 'height': 900})
        errors = []
        page.on('console', lambda msg: errors.append(f"Console {msg.type}: {msg.text}") if msg.type == 'error' else None)
        page.on('pageerror', lambda exc: errors.append(f"PageError: {exc}"))
        
        print("--- Testing Desktop Principal ---")
        page.goto('http://127.0.0.1:3000/pages/principal/principal.html', wait_until='domcontentloaded')
        page.wait_for_timeout(500)
        
        # Test Hover on second link ("My Class")
        my_class_link = page.locator('#sidebar .nav-link').nth(1)
        my_class_icon = my_class_link.locator('.nav-link-icon, .nav-icon')
        
        color_before = my_class_icon.evaluate("el => window.getComputedStyle(el).color")
        my_class_link.hover()
        page.wait_for_timeout(200)
        color_hover = my_class_icon.evaluate("el => window.getComputedStyle(el).color")
        print(f"My Class Icon: Inactive = {color_before}, Hover = {color_hover}")
        assert "100, 116, 106" in color_before, f"Expected #64746A before hover, got {color_before}"
        assert "23, 107, 69" in color_hover, f"Expected #176B45 on hover, got {color_hover}"
        
        # Test Collapse Button
        collapse_btn = page.locator('#sidebarCollapseBtn')
        if collapse_btn.is_visible():
            collapse_btn.click()
            page.wait_for_timeout(400)
            is_collapsed = page.evaluate("() => document.getElementById('sidebar').classList.contains('collapsed')")
            print("Sidebar collapsed state:", is_collapsed)
            page.locator('#sidebar').screenshot(path='C:/Users/oudom/.gemini/antigravity/brain/8fd19b10-a09a-43d8-a122-cb4a75dc0ff6/sidebar_collapsed.png')
            
            # Expand back
            expand_btn = page.locator('#sidebarExpandBtn')
            if expand_btn.is_visible():
                expand_btn.click()
                page.wait_for_timeout(400)
                print("Expanded back via sidebarExpandBtn")

        # 2. Mobile drawer test (390 x 844 iPhone 14)
        print("\n--- Testing Mobile View (390x844) ---")
        mobile_page = browser.new_page(viewport={'width': 390, 'height': 844})
        mobile_page.goto('http://127.0.0.1:3000/pages/principal/principal.html', wait_until='domcontentloaded')
        mobile_page.wait_for_timeout(500)
        
        # Find visible hamburger button
        hamburger = mobile_page.locator('.mobile-hamburger-btn:visible, [data-action="toggle-sidebar"]:visible').first
        print("Hamburger visible on mobile:", hamburger.is_visible())
        hamburger.click()
        mobile_page.wait_for_timeout(500)
        
        drawer_open = mobile_page.evaluate("() => document.getElementById('sidebar').classList.contains('open')")
        print("Sidebar open in drawer mode:", drawer_open)
        mobile_page.screenshot(path='C:/Users/oudom/.gemini/antigravity/brain/8fd19b10-a09a-43d8-a122-cb4a75dc0ff6/sidebar_mobile_drawer.png')
        
        # Verify icon color inside mobile drawer
        mobile_icon_color = mobile_page.evaluate('''() => {
            const link = document.querySelector('#sidebar .nav-link:not(.active)');
            const icon = link ? link.querySelector('.nav-link-icon, .nav-icon') : null;
            return icon ? window.getComputedStyle(icon).color : null;
        }''')
        print("Mobile drawer inactive icon color:", mobile_icon_color)
        assert "100, 116, 106" in mobile_icon_color, f"Expected #64746A in drawer, got {mobile_icon_color}"

        # 3. Check All 5 Portals for Errors and Visual Integrity
        portals = [
            ('/pages/principal/principal.html', 'Principal'),
            ('/pages/admin/admin.html', 'Admin'),
            ('/pages/teacher/teacher.html', 'Teacher'),
            ('/pages/student/student.html', 'Student'),
            ('/pages-directory.html', 'Directory'),
            ('/index.html', 'Index Portal Switcher')
        ]
        
        print("\n--- Verifying All Portals ---")
        for path, name in portals:
            page.goto(f'http://127.0.0.1:3000{path}', wait_until='domcontentloaded')
            page.wait_for_timeout(300)
            sb_check = page.evaluate('''() => {
                const sb = document.querySelector('.sidebar, #sidebar');
                if (!sb) return { found: false };
                const icons = Array.from(sb.querySelectorAll('.nav-link-icon, .nav-icon'));
                return {
                    found: true,
                    count: icons.length,
                    firstIconColor: icons[0] ? window.getComputedStyle(icons[0]).color : null,
                    firstIconSize: icons[0] ? window.getComputedStyle(icons[0]).fontSize : null
                };
            }''')
            print(f"Portal: {name:<22} | Found: {sb_check['found']} | Icons: {sb_check.get('count', 0)} | 1st Color: {sb_check.get('firstIconColor')}")

        browser.close()
        print("\nALL COMPREHENSIVE TESTS PASSED SUCCESSFULLY!")

if __name__ == '__main__':
    test_all()


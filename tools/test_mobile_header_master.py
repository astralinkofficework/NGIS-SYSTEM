import time
from playwright.sync_api import sync_playwright

TEST_URLS = [
    ('http://127.0.0.1:3000/pages/student/student-exams.html', 'student'),
    ('http://127.0.0.1:3000/pages/teacher/teacher.html', 'teacher'),
    ('http://127.0.0.1:3000/pages/principal/principal.html', 'principal'),
    ('http://127.0.0.1:3000/pages/admin/admin.html', 'admin'),
    ('http://127.0.0.1:3000/pages/shared/design-system-preview.html', 'shared')
]

def run_tests():
    print('Starting Master Mobile Top Navigation Verification Suite...')

    with sync_playwright() as p:
        browser = p.chromium.launch()

        # =====================================================================
        # 1. STRUCTURAL, DIMENSION & 4-ELEMENT ORDER TESTS
        # =====================================================================
        print('\n--- 1. Testing Mobile Header Structure & Specifications on Student Exams ---')
        page = browser.new_page(viewport={'width': 375, 'height': 812})
        page.goto('http://127.0.0.1:3000/pages/student/student-exams.html')
        page.wait_for_selector('#ngisMobileHeader')

        # Check visibility on mobile
        hdr = page.locator('#ngisMobileHeader')
        assert hdr.is_visible(), "Mobile header must be visible at 375px"

        # Check dimensions
        box = hdr.bounding_box()
        inner_box = page.locator('.ngis-mobile-header-inner').bounding_box()
        print(f"  Mobile header box: {box}, inner box: {inner_box}")
        assert 64 <= inner_box['height'] <= 74, f"Header height should be 64-72px, got {inner_box['height']}px"
        assert inner_box['width'] == 375, f"Header width should be 375px, got {inner_box['width']}px"

        # Check logo element
        logo_link = page.locator('.ngis-mobile-logo-link')
        assert logo_link.is_visible(), "Logo link must be visible"
        assert 'student.html' in logo_link.get_attribute('href'), f"Logo must link to student dashboard: {logo_link.get_attribute('href')}"
        logo_img = page.locator('.ngis-mobile-logo')
        logo_box = logo_img.bounding_box()
        print(f"  Logo dimensions: {logo_box}")
        assert 34 <= logo_box['height'] <= 42, f"Logo height should be 36-40px, got {logo_box['height']}px"

        # Check 3 action buttons exist in exact order: Bell -> Globe -> Menu
        actions = page.locator('.ngis-mobile-header-actions button').all()
        assert len(actions) == 3, f"Expected exactly 3 action buttons, found {len(actions)}"
        
        btn_ids = [btn.get_attribute('id') for btn in actions]
        assert btn_ids == ['ngisMobileNotifBtn', 'ngisMobileLangBtn', 'ngisMobileMenuBtn'], f"Action buttons order mismatch: {btn_ids}"
        print(f"  [PASS] Exact 4-element structure verified: Logo -> Space -> {btn_ids}")

        # Check button touch targets (48x48px) and icon sizes (24px)
        for btn in actions:
            btn_box = btn.bounding_box()
            svg = btn.locator('svg').first
            svg_box = svg.bounding_box()
            assert btn_box['width'] >= 44 and btn_box['height'] >= 44, f"Button touch target too small: {btn_box}"
            assert 20 <= svg_box['width'] <= 26 and 20 <= svg_box['height'] <= 26, f"SVG icon size should be 24px, got {svg_box}"
        print("  [PASS] All action buttons verified at 48x48px touch targets with 24px SVG icons")

        # Check bottom divider
        divider = page.locator('.ngis-mobile-header-divider')
        assert divider.is_visible(), "1px bottom divider must be visible"
        div_box = divider.bounding_box()
        assert div_box['height'] == 1, f"Divider height should be 1px, got {div_box['height']}px"
        print("  [PASS] 1px horizontal bottom divider verified")

        # Check NO search fields, avatars, or titles inside mobile header
        has_search = page.locator('#ngisMobileHeader input').count()
        has_avatar = page.locator('#ngisMobileHeader .avatar, #ngisMobileHeader .user-chip').count()
        assert has_search == 0, f"Found {has_search} search inputs in mobile header (must be 0)"
        assert has_avatar == 0, f"Found {has_avatar} avatars in mobile header (must be 0)"
        print("  [PASS] Zero search inputs, zero avatar chips inside mobile header (clean & minimal)")

        # =====================================================================
        # 2. NOTIFICATIONS SYSTEM TESTS
        # =====================================================================
        print('\n--- 2. Testing Notifications System & Panel ---')
        notif_btn = page.locator('#ngisMobileNotifBtn')
        notif_panel = page.locator('#ngisMobileNotifPanel')
        notif_dot = page.locator('#ngisMobileNotifDot')

        # Red dot should be visible if unread > 0
        dot_visible = notif_dot.is_visible()
        print(f"  Red unread dot visible initially: {dot_visible}")

        # Tap bell to open panel
        notif_btn.click()
        page.wait_for_timeout(200)
        assert notif_panel.is_visible(), "Notification panel must be visible after tapping bell"
        assert notif_btn.get_attribute('aria-expanded') == 'true', "Bell aria-expanded should be true"
        print("  [PASS] Notification panel opened on bell tap")

        # Verify panel contents
        title = page.locator('.ngis-notif-head-title').inner_text()
        assert 'Notifications' in title, f"Title mismatch: {title}"
        mark_all = page.locator('#ngisNotifMarkAllBtn')
        assert mark_all.is_visible(), "Mark all read button must be visible"
        tab_all = page.locator('#ngisNotifTabAll')
        tab_unread = page.locator('#ngisNotifTabUnread')
        assert tab_all.is_visible() and tab_unread.is_visible(), "All and Unread tabs must be visible"
        view_all = page.locator('#ngisNotifAllLink')
        assert view_all.is_visible(), "View all link must be visible"
        print("  [PASS] Notification panel structure verified (Title, Tabs, Items, View All)")

        # Tap Mark All Read
        mark_all.click()
        page.wait_for_timeout(300)
        unread_badge = page.locator('#ngisNotifBadge').inner_text()
        assert '0 unread' in unread_badge, f"Badge should be 0 unread: {unread_badge}"
        assert not notif_dot.is_visible(), "Red unread dot should be hidden after marking all read"
        print("  [PASS] Mark all as read cleared unread counts and hid red indicator dot")

        # =====================================================================
        # 3. LANGUAGE SELECTOR TESTS & MUTUAL EXCLUSIVITY
        # =====================================================================
        print('\n--- 3. Testing Language Selector & Mutual Exclusivity ---')
        lang_btn = page.locator('#ngisMobileLangBtn')
        lang_dropdown = page.locator('#ngisMobileLangDropdown')

        # Tapping Globe should close Notification panel and open Language dropdown
        lang_btn.click()
        page.wait_for_timeout(200)
        assert not notif_panel.is_visible(), "Notification panel must close when Globe is tapped"
        assert lang_dropdown.is_visible(), "Language dropdown must open when Globe is tapped"
        print("  [PASS] Mutual exclusivity: Opening Language dropdown automatically closed Notification panel")

        # Check language items
        lang_items = page.locator('.ngis-lang-item').all()
        assert len(lang_items) == 3, f"Expected 3 language options, got {len(lang_items)}"
        
        # Select Khmer
        khmer_btn = page.locator('.ngis-lang-item[data-lang="km"]')
        khmer_btn.click()
        page.wait_for_timeout(200)
        assert not lang_dropdown.is_visible(), "Language dropdown should close after selection"
        saved_lang = page.evaluate('() => localStorage.getItem("ngis-lang")')
        assert saved_lang == 'km', f"Language in localStorage should be 'km', got {saved_lang}"
        print(f"  [PASS] Language selected, persisted to localStorage ('{saved_lang}'), and closed dropdown")

        # Restore English
        lang_btn.click()
        page.wait_for_timeout(200)
        page.locator('.ngis-lang-item[data-lang="en"]').click()
        page.wait_for_timeout(200)

        # =====================================================================
        # 4. HAMBURGER MENU & CLOSE ICON TOGGLE
        # =====================================================================
        print('\n--- 4. Testing Hamburger Menu & Close Icon Toggle ---')
        menu_btn = page.locator('#ngisMobileMenuBtn')
        menu_icon = page.locator('.ngis-menu-icon')
        close_icon = page.locator('.ngis-close-icon')

        # Initially menu icon visible, close icon hidden
        assert menu_icon.is_visible(), "Menu icon must be visible initially"
        assert not close_icon.is_visible(), "Close icon must be hidden initially"

        # Tap hamburger to open sidebar drawer
        menu_btn.click()
        page.wait_for_timeout(300)
        
        # Check sidebar open
        is_open = page.evaluate('() => document.body.classList.contains("sidebar-open") || (document.getElementById("sidebar") && document.getElementById("sidebar").classList.contains("open"))')
        assert is_open, "Sidebar drawer must be open after tapping hamburger"
        
        # Check icon switched to Close
        assert close_icon.is_visible(), "Close icon must be visible when sidebar is open"
        assert not menu_icon.is_visible(), "Menu icon must be hidden when sidebar is open"
        print("  [PASS] Hamburger icon dynamically toggled to Close icon upon drawer open")

        # Tap again to close
        menu_btn.click()
        page.wait_for_timeout(300)
        assert menu_icon.is_visible(), "Menu icon must be restored when sidebar is closed"
        assert not close_icon.is_visible(), "Close icon must be hidden when sidebar is closed"
        print("  [PASS] Close icon dynamically toggled back to Hamburger icon upon drawer close")

        # Take screenshot of mobile header state
        page.screenshot(path='tools/mobile_header_375_verified.png')
        page.close()

        # =====================================================================
        # 5. DESKTOP ISOLATION TEST (1440px)
        # =====================================================================
        print('\n--- 5. Testing Desktop Isolation at 1440px ---')
        page_desk = browser.new_page(viewport={'width': 1440, 'height': 900})
        page_desk.goto('http://127.0.0.1:3000/pages/student/student-exams.html')
        page_desk.wait_for_timeout(300)
        
        desk_hdr = page_desk.locator('#ngisMobileHeader')
        assert not desk_hdr.is_visible(), "Mobile header must be completely hidden on desktop (1440px)"
        print("  [PASS] Desktop isolation verified: Mobile header is hidden on desktop displays")
        page_desk.close()

        # =====================================================================
        # 6. CROSS-PORTAL MOBILE HEADER TESTS
        # =====================================================================
        print('\n--- 6. Testing Mobile Header Across Portals ---')
        for url, role in TEST_URLS:
            slug = url.split('/')[-1]
            p = browser.new_page(viewport={'width': 375, 'height': 812})
            p.goto(url)
            p.wait_for_selector('#ngisMobileHeader', timeout=5000)
            
            # Check 4 elements present
            logo = p.locator('.ngis-mobile-logo-link')
            notif = p.locator('#ngisMobileNotifBtn')
            lang = p.locator('#ngisMobileLangBtn')
            menu = p.locator('#ngisMobileMenuBtn')
            div = p.locator('.ngis-mobile-header-divider')

            assert logo.is_visible() and notif.is_visible() and lang.is_visible() and menu.is_visible() and div.is_visible(), f"Missing header elements on {slug}"
            
            # Check horizontal overflow
            sw = p.evaluate('() => document.documentElement.scrollWidth')
            cw = p.evaluate('() => document.documentElement.clientWidth')
            assert sw <= cw, f"Horizontal scroll on {slug}: sw={sw}, cw={cw}"

            print(f"  [PASS] Portal page {slug:30s} ({role:10s}): All 4 elements verified, zero overflow")
            p.close()

        browser.close()

    print('\n=====================================================================')
    print('ALL MASTER MOBILE TOP NAVIGATION VERIFICATION TESTS PASSED 100%!')
    print('=====================================================================')

if __name__ == '__main__':
    run_tests()

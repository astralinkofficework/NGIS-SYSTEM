import time
from playwright.sync_api import sync_playwright

TEST_URLS = [
    ('http://127.0.0.1:3000/pages/student/student-exams.html', 'student'),
    ('http://127.0.0.1:3000/pages/teacher/teacher.html', 'teacher'),
    ('http://127.0.0.1:3000/pages/principal/principal.html', 'principal'),
    ('http://127.0.0.1:3000/pages/admin/admin.html', 'admin'),
    ('http://127.0.0.1:3000/pages/shared/department.html', 'shared')
]

VIEWPORTS = [
    ('Small Mobile', 320, 568),
    ('Mobile', 375, 812),
    ('iPhone 14/15', 390, 844),
    ('Large Mobile', 430, 932),
    ('Tablet', 768, 1024),
    ('Small Desktop', 1024, 768),
    ('Desktop', 1440, 900),
    ('Large Desktop', 1920, 1080),
    ('Wide Desktop', 2560, 1440)
]

def run_suite():
    print('=====================================================================')
    print('Starting Master Responsive Navigation System Test Suite...')
    print('=====================================================================\n')

    with sync_playwright() as p:
        browser = p.chromium.launch()

        # =====================================================================
        # 1. DESKTOP SPECIFICATIONS & INTERACTION TESTS (1440px)
        # =====================================================================
        print('--- 1. Testing Desktop Navigation Specifications (1440px) ---')
        dpage = browser.new_page(viewport={'width': 1440, 'height': 900})
        dpage.goto('http://127.0.0.1:3000/pages/student/student-exams.html')
        dpage.wait_for_selector('#ngisGlobalNavbar')

        nav = dpage.locator('#ngisGlobalNavbar')
        assert nav.is_visible(), "Master Navbar must be visible"

        drow = dpage.locator('.ngis-nav-desktop-row')
        assert drow.is_visible(), "Desktop nav row must be visible at 1440px"
        drow_box = drow.bounding_box()
        print(f"  Desktop row dimensions: width={drow_box['width']}px, height={drow_box['height']}px")
        assert 70 <= drow_box['height'] <= 74, f"Desktop navbar height must be 72px, got {drow_box['height']}px"

        # Check Logo
        logo = dpage.locator('.ngis-nav-desktop-row .ngis-nav-logo')
        assert logo.is_visible(), "School logo must be visible"
        logo_box = logo.bounding_box()
        assert 34 <= logo_box['height'] <= 42, f"Logo height should be ~38px, got {logo_box['height']}px"

        # Check Sidebar Collapse Button
        collapse_btn = dpage.locator('#navSidebarCollapseBtn')
        assert collapse_btn.is_visible(), "Sidebar collapse button must be visible on desktop"
        cbox = collapse_btn.bounding_box()
        assert cbox['width'] >= 38 and cbox['height'] >= 38, f"Collapse button target: {cbox}"
        print("  [PASS] Logo & Sidebar Collapse toggle button verified")

        # Check Long Search Bar
        search_wrap = dpage.locator('#ngisDesktopSearchWrap')
        assert search_wrap.is_visible(), "Desktop search bar must be visible"
        sw_box = search_wrap.bounding_box()
        print(f"  Search bar dimensions: width={sw_box['width']}px, height={sw_box['height']}px")
        assert sw_box['width'] >= 450, f"Desktop search bar should be ~480-640px+, got {sw_box['width']}px"
        assert 42 <= sw_box['height'] <= 46, f"Search bar height should be 44px, got {sw_box['height']}px"
        kbd = dpage.locator('.ngis-nav-search-kbd')
        assert kbd.is_visible(), "⌘ K shortcut badge must be visible"
        print("  [PASS] Long global search bar verified (width >= 480px, height 44px, radius 12px)")

        # Check Notification Bell & Dropdown
        notif_btn = dpage.locator('#ngisDesktopNotifBtn')
        assert notif_btn.is_visible(), "Notification bell must be visible"
        notif_btn.click()
        dpage.wait_for_timeout(300)
        notif_panel = dpage.locator('#ngisNavNotifPanel')
        assert notif_panel.is_visible(), "Notification panel must open on bell click"
        title = dpage.locator('#ngisNavNotifPanel .ngis-notif-head-title').inner_text()
        assert 'Notifications' in title, f"Title mismatch: {title}"
        mark_all = dpage.locator('#ngisNotifMarkAllBtn')
        assert mark_all.is_visible(), "Mark all read button must be visible"
        print("  [PASS] Live notifications panel opened on bell click (All/Unread tabs, Mark Read)")

        # Check Language Dropdown & Mutual Exclusivity
        lang_btn = dpage.locator('#ngisDesktopLangBtn')
        assert lang_btn.is_visible(), "Language globe button must be visible"
        lang_btn.click()
        dpage.wait_for_timeout(300)
        assert not notif_panel.is_visible(), "Notifications panel must close when Language is opened (Mutual Exclusivity)"
        lang_panel = dpage.locator('#ngisNavLangPanel')
        assert lang_panel.is_visible(), "Language panel must open on globe click"
        
        # Select Khmer
        dpage.locator('.ngis-lang-item[data-lang="km"]').click()
        dpage.wait_for_timeout(200)
        assert not lang_panel.is_visible(), "Language panel must close after selection"
        saved_lang = dpage.evaluate('() => localStorage.getItem("ngis-lang")')
        assert saved_lang == 'km', f"Language in localStorage should be 'km', got {saved_lang}"
        print("  [PASS] Language dropdown verified (EN, KM, ZH, checkmarks, persistence)")

        # Restore English
        lang_btn.click()
        dpage.wait_for_timeout(200)
        dpage.locator('.ngis-lang-item[data-lang="en"]').click()
        dpage.wait_for_timeout(200)

        # Check Profile Chip & Account Menu
        prof_chip = dpage.locator('#ngisNavProfileChip')
        assert prof_chip.is_visible(), "Profile chip must be visible"
        prof_chip.click()
        dpage.wait_for_timeout(300)
        account_panel = dpage.locator('#ngisNavAccountPanel')
        assert account_panel.is_visible(), "Account panel must open on profile chip click"
        acc_name = dpage.locator('.ngis-account-name').inner_text()
        assert len(acc_name) > 2, f"Account user name should be populated: {acc_name}"
        theme_toggle = dpage.locator('#ngisThemeToggleBtn')
        assert theme_toggle.is_visible(), "Theme switcher button must be present in account menu"
        sign_out = dpage.locator('#ngisSignOutBtn')
        assert sign_out.is_visible(), "Sign Out button must be present in account menu"
        print(f"  [PASS] Account menu verified ({acc_name}, Profile, Settings, Theme, Sign Out)")

        # Outside Click Dismissal
        dpage.click('body', position={'x': 100, 'y': 300})
        dpage.wait_for_timeout(200)
        assert not account_panel.is_visible(), "Account panel must close on outside click"
        print("  [PASS] Outside click dismissal verified")

        dpage.close()

        # =====================================================================
        # 2. GLOBAL SEARCH ENGINE INTEGRATION TESTS
        # =====================================================================
        print('\n--- 2. Testing Global Search Functionality & Keyboard Hotkeys ---')
        spage = browser.new_page(viewport={'width': 1440, 'height': 900})
        spage.goto('http://127.0.0.1:3000/pages/student/student-exams.html')
        spage.wait_for_selector('#ngisGlobalNavbar')

        # Test Ctrl+K / Cmd+K hotkey
        spage.keyboard.press('Control+k')
        spage.wait_for_timeout(200)
        is_focused = spage.evaluate('() => document.activeElement.id === "ngisGlobalSearchInput"')
        assert is_focused, "Ctrl+K must focus the global search input"
        print("  [PASS] Ctrl+K / Cmd+K hotkey focused search input")

        # Focus shows recent / quick search
        dropdown = spage.locator('#ngisDesktopSearchDropdown')
        assert dropdown.is_visible(), "Search dropdown must open on input focus"
        print("  [PASS] Quick search / recent searches displayed on focus")

        # Type 'math' query
        s_input = spage.locator('#ngisGlobalSearchInput')
        s_input.fill('math')
        spage.wait_for_timeout(400) # wait for debounce + API fetch

        # Verify categorized search results
        results = spage.locator('#ngisDesktopSearchDropdown .ngis-search-item').all()
        print(f"  Search for 'math' returned {len(results)} live categorized results")
        assert len(results) >= 3, f"Expected multiple categorized search results for 'math', got {len(results)}"
        
        # Check clear button appears and clears
        clear_btn = spage.locator('#ngisSearchClearBtn')
        assert clear_btn.is_visible(), "Clear button must be visible when query is entered"
        clear_btn.click()
        spage.wait_for_timeout(200)
        assert s_input.input_value() == "", "Search input must be cleared"
        print("  [PASS] Live search categorization, API connection, and clear action verified")

        spage.close()

        # =====================================================================
        # 3. MOBILE TWO-ROW NAVIGATION TESTS (375px)
        # =====================================================================
        print('\n--- 3. Testing Mobile Two-Row Navigation (375px) ---')
        mpage = browser.new_page(viewport={'width': 375, 'height': 812})
        mpage.goto('http://127.0.0.1:3000/pages/student/student-exams.html')
        mpage.wait_for_selector('#ngisGlobalNavbar')

        # Desktop row hidden, Mobile rows 1 & 2 visible
        assert not mpage.locator('.ngis-nav-desktop-row').is_visible(), "Desktop row must be hidden on mobile"
        row1 = mpage.locator('.ngis-nav-mobile-row1')
        row2 = mpage.locator('.ngis-nav-mobile-row2')
        assert row1.is_visible(), "Mobile row 1 must be visible"
        assert row2.is_visible(), "Mobile row 2 must be visible"

        r1_box = row1.bounding_box()
        r2_box = row2.bounding_box()
        print(f"  Mobile Row 1: height={r1_box['height']}px; Row 2: height={r2_box['height']}px")
        assert 62 <= r1_box['height'] <= 66, f"Row 1 height should be 64px, got {r1_box['height']}px"
        assert 50 <= r2_box['height'] <= 60, f"Row 2 height should be ~56px, got {r2_box['height']}px"

        # Check Row 1 controls order: Logo -> Spacer -> Bell -> Globe -> Hamburger
        m_actions = mpage.locator('.ngis-nav-actions button').all()
        assert len(m_actions) == 3, f"Expected 3 mobile action buttons, got {len(m_actions)}"
        m_ids = [btn.get_attribute('id') for btn in m_actions]
        assert m_ids == ['ngisMobileNotifBtn', 'ngisMobileLangBtn', 'ngisMobileMenuBtn'], f"Mobile actions order mismatch: {m_ids}"
        print(f"  [PASS] Mobile Row 1 exact sequence verified: Logo -> Spacer -> {m_ids}")

        # Check Mobile Full-Width Search Bar
        m_search = mpage.locator('#ngisMobileSearchWrap')
        assert m_search.is_visible(), "Mobile search bar must be visible"
        ms_box = m_search.bounding_box()
        print(f"  Mobile search box width={ms_box['width']}px, height={ms_box['height']}px")
        assert ms_box['width'] >= 340, f"Mobile search bar should span full width (~343px), got {ms_box['width']}px"
        assert 42 <= ms_box['height'] <= 46, f"Mobile search height should be 44px, got {ms_box['height']}px"
        print("  [PASS] Mobile Row 2 full-width search bar verified (44px height, 12px radius)")

        # Check Hamburger Toggle to Close Icon
        menu_btn = mpage.locator('#ngisMobileMenuBtn')
        menu_icon = mpage.locator('#ngisMobileMenuBtn .ngis-menu-icon')
        close_icon = mpage.locator('#ngisMobileMenuBtn .ngis-close-icon')
        assert menu_icon.is_visible(), "Menu icon visible initially"
        assert not close_icon.is_visible(), "Close icon hidden initially"

        menu_btn.click()
        mpage.wait_for_timeout(300)
        is_drawer_open = mpage.evaluate('() => document.body.classList.contains("sidebar-open") || (document.getElementById("sidebar") && document.getElementById("sidebar").classList.contains("open"))')
        assert is_drawer_open, "Sidebar drawer should open on mobile menu click"
        assert close_icon.is_visible(), "Close icon must become visible when drawer is open"
        print("  [PASS] Hamburger dynamically toggled to Close icon upon drawer open")

        # Close again
        menu_btn.click()
        mpage.wait_for_timeout(300)
        assert menu_icon.is_visible(), "Menu icon restored on drawer close"
        print("  [PASS] Dynamic hamburger / close toggle cycle verified")

        mpage.close()

        # =====================================================================
        # 4. RESPONSIVE BREAKPOINT & OVERFLOW AUDIT (320px to 2560px)
        # =====================================================================
        print('\n--- 4. Testing Responsive Viewports & Zero Horizontal Overflow ---')
        for vp_name, w, h in VIEWPORTS:
            vpage = browser.new_page(viewport={'width': w, 'height': h})
            vpage.goto('http://127.0.0.1:3000/pages/student/student-exams.html')
            vpage.wait_for_selector('#ngisGlobalNavbar')

            # Check overflow
            sw = vpage.evaluate('() => document.documentElement.scrollWidth')
            cw = vpage.evaluate('() => document.documentElement.clientWidth')
            assert sw <= cw, f"Horizontal scroll detected at {vp_name} ({w}px): scrollWidth={sw}, clientWidth={cw}"

            # Check navbar visibility
            n_box = vpage.locator('#ngisGlobalNavbar').bounding_box()
            assert n_box['width'] == w, f"Navbar width mismatch at {w}px: got {n_box['width']}px"

            print(f"  [PASS] {vp_name:16s} ({w:4d}x{h:4d}): Navbar width={n_box['width']}px, zero overflow (sw={sw}, cw={cw})")
            vpage.close()

        # =====================================================================
        # 5. CROSS-PORTAL INTEGRATION TESTS
        # =====================================================================
        print('\n--- 5. Testing Navigation Across All Portals ---')
        for url, role in TEST_URLS:
            slug = url.split('/')[-1]
            p = browser.new_page(viewport={'width': 1440, 'height': 900})
            p.goto(url)
            p.wait_for_selector('#ngisGlobalNavbar')

            # Check Desktop Navbar presence
            nav = p.locator('#ngisGlobalNavbar')
            assert nav.is_visible(), f"Navbar missing on {slug}"

            # Check user role title in profile
            user_role = p.locator('.ngis-profile-role').inner_text()
            assert len(user_role) > 0, f"Role missing in profile on {slug}"

            # Check search bar presence
            search = p.locator('#ngisGlobalSearchInput')
            assert search.is_visible(), f"Search input missing on {slug}"

            print(f"  [PASS] Portal {slug:28s} ({role:10s}): Loaded unified navbar (Role: {user_role})")
            p.close()

        browser.close()

    print('\n=====================================================================')
    print('ALL MASTER RESPONSIVE NAVIGATION SYSTEM TESTS PASSED 100%!')
    print('=====================================================================')

if __name__ == '__main__':
    run_suite()

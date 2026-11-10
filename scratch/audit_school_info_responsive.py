from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()

    # 1. Mobile (390x844)
    page_mobile = browser.new_page(viewport={'width': 390, 'height': 844})
    errors = []
    page_mobile.on('console', lambda msg: errors.append(msg.text) if msg.type == 'error' else None)
    page_mobile.goto('http://127.0.0.1:3000/pages/admin/admin-school-information.html', wait_until='networkidle')
    page_mobile.wait_for_timeout(1000)

    # Check mobile hamburger
    hamb = page_mobile.locator('[data-action="toggle-sidebar"], .hamburger-btn, .mobile-hamburger-btn')
    assert hamb.count() > 0, "Hamburger button not found on mobile"
    assert hamb.first.is_visible(), "Hamburger button not visible on mobile"
    print("Mobile hamburger verified!")

    # Check that .page is present and wraps the content
    has_page = page_mobile.locator('.page').count()
    assert has_page > 0, ".page container not found"
    print(".page container verified!")

    # Check horizontal tabs on mobile
    tabs = page_mobile.locator('.si-mobile-tab')
    print(f"Mobile tabs count: {tabs.count()}")
    assert tabs.count() > 0, "Mobile navigation tabs not rendered"

    # Screenshot initial mobile view
    page_mobile.screenshot(path='scratch/school_info_mobile_390_v2.png')
    print("Captured scratch/school_info_mobile_390_v2.png")

    # Tap on 'campuses' tab
    campuses_tab = page_mobile.locator('.si-mobile-tab[data-sec="campuses"]')
    campuses_tab.click()
    page_mobile.wait_for_timeout(500)
    page_mobile.screenshot(path='scratch/school_info_mobile_campuses_v2.png')
    print("Captured scratch/school_info_mobile_campuses_v2.png")

    # Open mobile navigation drawer via hamburger
    hamb.first.click()
    page_mobile.wait_for_timeout(500)
    page_mobile.screenshot(path='scratch/school_info_mobile_drawer_v2.png')
    print("Captured scratch/school_info_mobile_drawer_v2.png")

    # Close mobile page
    page_mobile.close()

    # 2. Tablet (768x1024)
    page_tablet = browser.new_page(viewport={'width': 768, 'height': 1024})
    page_tablet.goto('http://127.0.0.1:3000/pages/admin/admin-school-information.html', wait_until='networkidle')
    page_tablet.wait_for_timeout(1000)
    page_tablet.screenshot(path='scratch/school_info_tablet_768_v2.png')
    print("Captured scratch/school_info_tablet_768_v2.png")
    page_tablet.close()

    # 3. Desktop (1440x900)
    page_desktop = browser.new_page(viewport={'width': 1440, 'height': 900})
    page_desktop.goto('http://127.0.0.1:3000/pages/admin/admin-school-information.html', wait_until='networkidle')
    page_desktop.wait_for_timeout(1000)
    page_desktop.screenshot(path='scratch/school_info_desktop_1440_v2.png')
    print("Captured scratch/school_info_desktop_1440_v2.png")
    page_desktop.close()

    print(f"Total console errors across all viewports: {len(errors)}")
    for err in errors[:5]:
        print(" -", err)

    browser.close()
    print("All responsive audit tests completed successfully!")

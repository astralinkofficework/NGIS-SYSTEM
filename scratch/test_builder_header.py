from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    page.goto("http://127.0.0.1:3000/pages/principal/principal-timetable-builder.html")
    page.wait_for_timeout(1000)

    # 1. Desktop Check
    topbar = page.locator(".hero-topbar")
    print("Desktop topbar count:", topbar.count())
    page.screenshot(path="scratch/builder_1440.png")

    # 2. Tablet 768px Check
    page.set_viewport_size({"width": 768, "height": 1024})
    page.wait_for_timeout(500)
    page.screenshot(path="scratch/builder_768.png")

    # 3. Mobile 390px Check
    page.set_viewport_size({"width": 390, "height": 844})
    page.wait_for_timeout(500)
    page.screenshot(path="scratch/builder_390.png")

    # Check mobile hamburger button
    hamb = page.locator("#htbHamburger")
    print("Mobile hamburger is visible:", hamb.is_visible())
    
    # Click hamburger to verify sidebar toggle
    sidebar = page.locator("#sidebar, aside, [data-purpose='sidebar'], nav.sidebar")
    print("Sidebar count:", sidebar.count())
    hamb.click()
    page.wait_for_timeout(400)
    page.screenshot(path="scratch/builder_mobile_sidebar_open.png")

    browser.close()
print("Verification complete!")


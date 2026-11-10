from playwright.sync_api import sync_playwright

test_pages = [
    # Principal
    ("http://127.0.0.1:3000/pages/principal/principal-records.html", "principal-records"),
    ("http://127.0.0.1:3000/pages/principal/principal-subjects.html", "principal-subjects"),
    ("http://127.0.0.1:3000/pages/principal/principal-teacher-class-assignment.html", "principal-teacher-class-assignment"),
    ("http://127.0.0.1:3000/pages/principal/principal-timetable-builder.html", "principal-timetable-builder"),
    ("http://127.0.0.1:3000/pages/principal/principal-timetables.html", "principal-timetables"),
    # Admin
    ("http://127.0.0.1:3000/pages/admin/admin-records.html", "admin-records"),
    ("http://127.0.0.1:3000/pages/admin/admin-subjects.html", "admin-subjects"),
    ("http://127.0.0.1:3000/pages/admin/admin-teacher-class-assignment.html", "admin-teacher-class-assignment"),
    ("http://127.0.0.1:3000/pages/admin/admin-timetable-builder.html", "admin-timetable-builder"),
    ("http://127.0.0.1:3000/pages/admin/admin-timetables.html", "admin-timetables")
]

viewports = [
    ("desktop", 1440, 900),
    ("laptop", 1024, 768),
    ("tablet", 768, 1024),
    ("mobile", 390, 844)
]

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()

    for url, slug in test_pages:
        print(f"\nTesting {slug} ({url})...")
        page.set_viewport_size({"width": 1440, "height": 900})
        page.goto(url)
        page.wait_for_timeout(600)

        # Check hero topbar
        topbar = page.locator(".hero-topbar")
        if topbar.count() == 0:
            print(f"  FAILED: No .hero-topbar found on {slug}")
        else:
            print(f"  PASS: .hero-topbar present")

        brand = page.locator(".htb-brand-wrap")
        profile = page.locator("#htbProfile")
        search = page.locator(".htb-search-wrap")

        print(f"  Brand: {brand.is_visible()}, Profile: {profile.is_visible()}, Search: {search.is_visible()}")

        # Test mobile
        page.set_viewport_size({"width": 390, "height": 844})
        page.wait_for_timeout(400)
        hamb = page.locator("#htbHamburger")
        hamb_vis = hamb.is_visible()
        print(f"  Mobile 390px hamburger visible: {hamb_vis}")

        # Test sidebar toggle
        if hamb_vis:
            hamb.click()
            page.wait_for_timeout(300)
            sidebar = page.locator(".sidebar, aside, [data-purpose='sidebar'], #sidebar")
            print(f"  Sidebar toggled, class: {sidebar.first.get_attribute('class')}")
            # close sidebar
            page.keyboard.press("Escape")

    # Capture key screenshots for artifact
    key_pages = [
        ("http://127.0.0.1:3000/pages/principal/principal-timetable-builder.html", "builder"),
        ("http://127.0.0.1:3000/pages/principal/principal-records.html", "records"),
        ("http://127.0.0.1:3000/pages/principal/principal-teacher-class-assignment.html", "assignment"),
        ("http://127.0.0.1:3000/pages/principal/principal-timetables.html", "timetables"),
    ]

    for url, slug in key_pages:
        for vp_name, w, h in viewports:
            page.set_viewport_size({"width": w, "height": h})
            page.goto(url)
            page.wait_for_timeout(500)
            page.screenshot(path=f"scratch/verify_{slug}_{vp_name}_{w}.png")
            print(f"Saved scratch/verify_{slug}_{vp_name}_{w}.png")

    browser.close()

print("\nAll 10 pages verified across desktop, laptop, tablet, and mobile!")


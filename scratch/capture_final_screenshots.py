from playwright.sync_api import sync_playwright

pages_to_snap = [
    ("http://127.0.0.1:3000/pages/principal/principal-timetable-builder.html", "timetable_builder"),
    ("http://127.0.0.1:3000/pages/principal/principal-timetables.html", "timetables_master"),
    ("http://127.0.0.1:3000/pages/principal/principal-teacher-class-assignment.html", "assignment_matrix"),
    ("http://127.0.0.1:3000/pages/principal/principal-records.html", "data_entry_records")
]

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()

    for url, name in pages_to_snap:
        # Desktop 1440
        page.set_viewport_size({"width": 1440, "height": 900})
        page.goto(url)
        page.wait_for_timeout(800)
        page.screenshot(path=f"scratch/{name}_desktop_1440.png")

        # Tablet 768
        page.set_viewport_size({"width": 768, "height": 1024})
        page.wait_for_timeout(400)
        page.screenshot(path=f"scratch/{name}_tablet_768.png")

        # Mobile 390
        page.set_viewport_size({"width": 390, "height": 844})
        page.wait_for_timeout(400)
        page.screenshot(path=f"scratch/{name}_mobile_390.png")

        print(f"Captured {name} across 1440, 768, 390")

    browser.close()
print("All screenshots captured successfully!")


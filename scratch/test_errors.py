from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    for name, path in [
        ("Teacher Assignment", "pages/principal/principal-teacher-class-assignment.html"),
        ("Timetable Builder", "pages/principal/principal-timetable-builder.html"),
        ("Timetables", "pages/principal/principal-timetables.html"),
        ("Subjects", "pages/principal/principal-subjects.html"),
        ("Records", "pages/principal/principal-records.html")
    ]:
        page = browser.new_page(viewport={"width": 1440, "height": 900})
        errors = []
        page.on("console", lambda m: errors.append(f"[{m.type}] {m.text}") if m.type in ["error"] else None)
        page.on("pageerror", lambda e: errors.append(f"[PAGE ERROR] {e}"))
        res = page.goto(f"http://127.0.0.1:3000/{path}")
        page.wait_for_timeout(800)
        print(f"{name}: HTTP {res.status}, {len(errors)} console errors")
        for err in errors:
            print("  ", err)
        page.close()
    browser.close()


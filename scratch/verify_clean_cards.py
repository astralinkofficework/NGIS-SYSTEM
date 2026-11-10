from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1440, "height": 900})

    errors = []
    page.on("console", lambda msg: errors.append(f"[{msg.type}] {msg.text}") if msg.type == "error" else None)
    page.on("pageerror", lambda err: errors.append(f"[pageerror] {err}"))

    # 1. Teacher Profiles
    print("\n--- Checking Principal Teacher Profiles ---")
    page.goto("http://127.0.0.1:3000/pages/principal/principal-teacher-profiles.html", wait_until="networkidle")
    page.wait_for_timeout(500)
    cards = page.locator(".telemetry-card")
    print(f"Rendered telemetry cards count: {cards.count()}")
    sub_elements = page.locator(".telemetry-card .bg-slate-50\\/80, .telemetry-card .border-slate-100")
    print(f"Found bottom sub-elements in teacher cards: {sub_elements.count()}")

    # Capture screenshot
    page.screenshot(path=r"C:\Users\oudom\.gemini\antigravity\brain\8fd19b10-a09a-43d8-a122-cb4a75dc0ff6\teacher_profiles_clean_cards.png")

    # 2. Student Profiles
    print("\n--- Checking Principal Student Profiles ---")
    page.goto("http://127.0.0.1:3000/pages/principal/principal-student-profiles.html", wait_until="networkidle")
    page.wait_for_timeout(500)
    cards_s = page.locator(".telemetry-card")
    print(f"Rendered telemetry cards count: {cards_s.count()}")
    sub_elements_s = page.locator(".telemetry-card .bg-slate-50\\/80, .telemetry-card .border-slate-100")
    print(f"Found bottom sub-elements in student cards: {sub_elements_s.count()}")

    # Capture screenshot
    page.screenshot(path=r"C:\Users\oudom\.gemini\antigravity\brain\8fd19b10-a09a-43d8-a122-cb4a75dc0ff6\student_profiles_clean_cards.png")

    print(f"\nConsole Errors: {len(errors)}")
    if errors:
        for err in errors:
            print(f"  {err}")
    else:
        print("SUCCESS: 0 console errors!")

    browser.close()


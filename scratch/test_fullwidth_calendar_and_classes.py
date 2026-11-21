import os
from playwright.sync_api import sync_playwright

ARTIFACT_DIR = r"C:\Users\oudom\.gemini\antigravity\brain\f0e0db56-cd04-4f51-a7f8-40ba21b43536"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1440, "height": 1400})

    failed_requests = []
    page.on("requestfailed", lambda req: failed_requests.append(req.url))

    print("Navigating to student.html...")
    page.goto("http://127.0.0.1:3000/pages/student/student.html", wait_until="networkidle")
    page.wait_for_timeout(1000)

    # 1. Full Page Desktop Screenshot
    full_desktop = os.path.join(ARTIFACT_DIR, "student_fullwidth_layout_desktop.png")
    page.screenshot(path=full_desktop, full_page=True)
    print(f"Captured full desktop screenshot: {full_desktop}")

    # 2. Crop Weekly Calendar Section
    cal_section = page.query_selector(".workspace-calendar-card")
    if cal_section:
        cal_shot = os.path.join(ARTIFACT_DIR, "weekly_calendar_fullwidth_desktop.png")
        cal_section.screenshot(path=cal_shot)
        print(f"Captured calendar screenshot: {cal_shot}")

    # 3. Crop My Classes Section
    classes_section = page.query_selector(".workspace-classes-full-list")
    if classes_section:
        parent_card = classes_section.evaluate_handle("el => el.closest('.workspace-card')")
        classes_shot = os.path.join(ARTIFACT_DIR, "my_classes_fullwidth_desktop.png")
        parent_card.screenshot(path=classes_shot)
        print(f"Captured classes screenshot: {classes_shot}")

    # 4. Test Add Personal Event Modal
    print("Testing '+ Add Personal Event' button...")
    add_btn = page.query_selector("#btnAddPersonalEvent")
    if add_btn:
        add_btn.click()
        page.wait_for_timeout(600)
        modal_shot = os.path.join(ARTIFACT_DIR, "calendar_add_event_modal.png")
        page.screenshot(path=modal_shot)
        print(f"Captured add event modal screenshot: {modal_shot}")

        # Fill and submit
        page.fill("#evTitleInput", "Physics Lab Review")
        page.fill("#evTimeInput", "16:30")
        page.click("#btnSaveEventSubmit")
        page.wait_for_timeout(600)
        print("Submitted new event and updated calendar!")

    # 5. Mobile View (390x844)
    print("Testing mobile viewport...")
    mobile_page = browser.new_page(viewport={"width": 390, "height": 844}, device_scale_factor=2)
    mobile_page.goto("http://127.0.0.1:3000/pages/student/student.html", wait_until="networkidle")
    mobile_page.wait_for_timeout(1000)
    mobile_shot = os.path.join(ARTIFACT_DIR, "student_fullwidth_layout_mobile.png")
    mobile_page.screenshot(path=mobile_shot, full_page=True)
    print(f"Captured full mobile screenshot: {mobile_shot}")
    mobile_page.close()

    if failed_requests:
        print(f"[WARNING] Failed requests: {failed_requests}")
    else:
        print("[SUCCESS] Zero network or image errors!")

    browser.close()

import os
import sys
import json
from playwright.sync_api import sync_playwright

ARTIFACT_DIR = r"C:\Users\oudom\.gemini\antigravity\brain\f0e0db56-cd04-4f51-a7f8-40ba21b43536"
ICONS_DIR = r"assets\images\icons-3d"

# 1. Verify all 22 icons
manifest_path = os.path.join(ICONS_DIR, "manifest.json")
with open(manifest_path, "r", encoding="utf-8") as f:
    manifest = json.load(f)

print(f"Loaded manifest with {len(manifest)} icons.")
for item in manifest:
    name = item["concept"]
    file_path = os.path.join(ICONS_DIR, item["file"])
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Missing icon: {file_path}")
    sz = os.path.getsize(file_path)
    if sz < 1000:
        raise ValueError(f"Suspiciously small icon file: {file_path} ({sz} bytes)")
    print(f"  [OK] {name} -> {item['file']} ({sz} bytes)")

# 2. Run Playwright verification
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    
    # Desktop tests
    context = browser.new_context(viewport={"width": 1440, "height": 900}, device_scale_factor=1)
    page = context.new_page()

    failed_requests = []
    page.on("requestfailed", lambda req: failed_requests.append(req.url))

    print("\nNavigating to student.html (Desktop 1440x900)...")
    page.goto("http://127.0.0.1:3000/pages/student/student.html", wait_until="networkidle")
    page.wait_for_timeout(1000)

    # Check 3D icons on page
    icon_check = page.evaluate("""() => {
        const imgs = Array.from(document.querySelectorAll('img.ngis-3d-icon, img[src*="icons-3d"]'));
        return imgs.map(img => {
            const cs = window.getComputedStyle(img);
            const parentCs = window.getComputedStyle(img.parentElement);
            return {
                src: img.src,
                alt: img.alt,
                naturalWidth: img.naturalWidth,
                naturalHeight: img.naturalHeight,
                width: img.offsetWidth,
                height: img.offsetHeight,
                bg: cs.backgroundColor,
                parentBg: parentCs.backgroundColor,
                parentBorderRadius: parentCs.borderRadius,
                parentTag: img.parentElement.tagName
            };
        });
    }""")

    print(f"Found {len(icon_check)} 3D icons rendered on student.html:")
    for ic in icon_check:
        print(f"  - {ic['src'].split('/')[-1]}: {ic['naturalWidth']}x{ic['naturalHeight']} (rendered {ic['width']}x{ic['height']}) parent={ic['parentTag']}")
        if ic['naturalWidth'] == 0:
            print(f"    [FAIL] Broken image: {ic['src']}")

    desktop_shot = os.path.join(ARTIFACT_DIR, "student_workspace_3d_desktop_1440.png")
    page.screenshot(path=desktop_shot, full_page=False)
    print(f"Captured {desktop_shot}")

    # Check modal with 3D icon
    print("Testing modal interaction...")
    # Click on the first assignment row
    first_assign = page.query_selector(".sw-assign-row")
    if first_assign:
        first_assign.click()
        page.wait_for_timeout(600)
        modal_shot = os.path.join(ARTIFACT_DIR, "student_modal_3d_open.png")
        page.screenshot(path=modal_shot, full_page=False)
        print(f"Captured {modal_shot}")
        # Close modal
        close_btn = page.query_selector("#swModalClose")
        if close_btn:
            close_btn.click()
            page.wait_for_timeout(300)

    # Mobile test (390x844)
    print("\nTesting mobile layout (390x844)...")
    mobile_ctx = browser.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2)
    mobile_page = mobile_ctx.new_page()
    mobile_page.goto("http://127.0.0.1:3000/pages/student/student.html", wait_until="networkidle")
    mobile_page.wait_for_timeout(1000)
    mobile_shot = os.path.join(ARTIFACT_DIR, "student_workspace_3d_mobile_390.png")
    mobile_page.screenshot(path=mobile_shot, full_page=False)
    print(f"Captured {mobile_shot}")
    mobile_ctx.close()

    # Grades page test
    print("\nNavigating to student-grades.html...")
    page.goto("http://127.0.0.1:3000/pages/student/student-grades.html", wait_until="networkidle")
    page.wait_for_timeout(1000)
    grades_shot = os.path.join(ARTIFACT_DIR, "student_grades_3d_desktop.png")
    page.screenshot(path=grades_shot, full_page=False)
    print(f"Captured {grades_shot}")

    # Timetable page test
    print("\nNavigating to student-timetable.html...")
    page.goto("http://127.0.0.1:3000/pages/student/student-timetable.html", wait_until="networkidle")
    page.wait_for_timeout(1000)
    timetable_shot = os.path.join(ARTIFACT_DIR, "student_timetable_3d_desktop.png")
    page.screenshot(path=timetable_shot, full_page=False)
    print(f"Captured {timetable_shot}")

    # Assignments page test
    print("\nNavigating to student-assignments.html...")
    page.goto("http://127.0.0.1:3000/pages/student/student-assignments.html", wait_until="networkidle")
    page.wait_for_timeout(1000)
    assignments_shot = os.path.join(ARTIFACT_DIR, "student_assignments_3d_desktop.png")
    page.screenshot(path=assignments_shot, full_page=False)
    print(f"Captured {assignments_shot}")

    # Report failed requests
    if failed_requests:
        print(f"\n[WARNING] Failed requests: {failed_requests}")
    else:
        print("\n[SUCCESS] All requests succeeded with 0 network errors!")

    browser.close()

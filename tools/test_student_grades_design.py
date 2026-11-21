import os
import sys
from playwright.sync_api import sync_playwright

BASE_URL = "http://127.0.0.1:3000"
ARTIFACT_DIR = r"C:\Users\oudom\.gemini\antigravity\brain\f0e0db56-cd04-4f51-a7f8-40ba21b43536"

def verify_student_grades():
    print("=" * 70)
    print("VERIFYING STUDENT-GRADES.HTML OLD DESIGN RESTORATION")
    print("=" * 70)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1440, "height": 900})
        page = context.new_page()

        url = f"{BASE_URL}/pages/student/student-grades.html"
        print(f"Loading {url}...")
        page.goto(url, wait_until="load", timeout=8000)
        page.wait_for_timeout(500)

        # 1. Desktop Screenshot
        shot_desktop = os.path.join(ARTIFACT_DIR, "student_grades_restored_desktop.png")
        page.screenshot(path=shot_desktop, full_page=False)
        print(f"[SCREENSHOT] Saved desktop view: {shot_desktop}")

        # 2. Check Hero Title
        hero_title = page.locator(".hero-title").inner_text()
        print(f"  Hero Title: '{hero_title}'")
        assert "Report Cards & Performance" in hero_title, f"Unexpected hero title: {hero_title}"

        # 3. Check 4 Stat Cards
        stats_text = page.locator(".subpage-container .stat-item-card").all_inner_texts()
        print(f"  Found {len(stats_text)} stat cards:")
        for idx, s in enumerate(stats_text, 1):
            clean = " | ".join(s.splitlines())
            print(f"    Card {idx}: {clean}")
        assert len(stats_text) == 4, f"Expected 4 stat cards, got {len(stats_text)}"
        assert "3.88 / 4.00" in stats_text[0]
        assert "28.0 Credits" in stats_text[1]
        assert "Semester 2" in stats_text[2]
        assert "Tier 1 Dean's List" in stats_text[3]

        # 4. Check Section Heading & Export Button
        heading = page.locator("h2:has-text('Academic Report Cards & Evaluation Record')")
        assert heading.is_visible(), "Section heading not visible"
        export_btn = page.locator("button:has-text('Export Official PDF')")
        assert export_btn.is_visible(), "Export Official PDF button not visible"

        # 5. Check Row Card 1 (Semester 1)
        row1 = page.locator(".record-row-card").first
        row1_text = row1.inner_text()
        assert "ពិន្ទុឆមាសទី១" in row1_text, "Row 1 missing Khmer title"
        assert "Semester 1 Examination" in row1_text, "Row 1 missing semester title"
        assert "Verified & Uploaded" in row1_text, "Row 1 missing Verified badge"
        assert "View Card" in row1_text, "Row 1 missing View Card button"

        # 6. Test Modal 1: View Card (Report Card Modal)
        view_btn = row1.locator("button:has-text('View Card')")
        view_btn.click()
        page.wait_for_timeout(350)
        report_modal = page.locator("#reportCardModal")
        assert report_modal.is_visible(), "Report Card modal did not open on View Card click"
        shot_modal1 = os.path.join(ARTIFACT_DIR, "student_grades_report_card_modal.png")
        page.screenshot(path=shot_modal1)
        print(f"[SCREENSHOT] Saved report card modal: {shot_modal1}")

        # Close Modal 1
        page.locator("#reportCardModal button[aria-label='Close modal']").click()
        page.wait_for_timeout(200)
        assert not page.locator("#reportCardModal").is_visible(), "Report Card modal should be closed"

        # 7. Test Modal 2: Breakdown Modal
        breakdown_btn = page.locator("button:has-text('Breakdown')")
        breakdown_btn.click()
        page.wait_for_timeout(350)
        breakdown_modal = page.locator("#breakdownModal")
        assert breakdown_modal.is_visible(), "Breakdown modal did not open"
        shot_modal2 = os.path.join(ARTIFACT_DIR, "student_grades_breakdown_modal.png")
        page.screenshot(path=shot_modal2)
        print(f"[SCREENSHOT] Saved breakdown modal: {shot_modal2}")

        page.locator("#breakdownModal button[aria-label='Close modal']").click()
        page.wait_for_timeout(200)

        # 8. Test Modal 3: Projected GPA Modal
        proj_btn = page.locator("button:has-text('View Projected GPA')")
        proj_btn.click()
        page.wait_for_timeout(350)
        proj_modal = page.locator("#projectedGpaModal")
        assert proj_modal.is_visible(), "Projected GPA modal did not open"
        shot_modal3 = os.path.join(ARTIFACT_DIR, "student_grades_projected_gpa_modal.png")
        page.screenshot(path=shot_modal3)
        print(f"[SCREENSHOT] Saved projected GPA modal: {shot_modal3}")

        page.locator("#projectedGpaModal button[aria-label='Close modal']").click()
        page.wait_for_timeout(200)

        # 9. Test Mobile Viewport (375px)
        print("\nTesting Mobile Viewport (375px)...")
        page.set_viewport_size({"width": 375, "height": 812})
        page.reload(wait_until="load")
        page.wait_for_timeout(400)

        shot_mobile = os.path.join(ARTIFACT_DIR, "student_grades_restored_mobile_375.png")
        page.screenshot(path=shot_mobile, full_page=False)
        print(f"[SCREENSHOT] Saved mobile view: {shot_mobile}")

        # Check hamburger button
        hamb = page.locator(".hamburger-btn, [data-action='toggle-sidebar']").first
        assert hamb.is_visible(), "Mobile hamburger menu button not visible"

        browser.close()

    print("\n" + "=" * 70)
    print("ALL STUDENT-GRADES DESIGN RESTORATION CHECKS PASSED!")
    print("=" * 70)

if __name__ == '__main__':
    verify_student_grades()

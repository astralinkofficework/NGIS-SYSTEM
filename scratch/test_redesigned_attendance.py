import time
from playwright.sync_api import sync_playwright

def test_attendance():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={'width': 1400, 'height': 900})
        page = context.new_page()

        console_errors = []
        page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)

        print("Navigating to http://127.0.0.1:3000/pages/principal/principal-attendance.html...")
        page.goto("http://127.0.0.1:3000/pages/principal/principal-attendance.html", wait_until="networkidle")
        time.sleep(1)

        # 1. Verify Title & Page Structure
        title = page.title()
        print(f"Page Title: {title}")
        assert "Arrival Verification" in title or "Attendance" in title

        # 2. Check Telemetry Cards
        kpi_rate = page.locator("#kpiPresentRate").inner_text()
        kpi_count = page.locator("#kpiPresentCount").inner_text()
        print(f"KPI Rate: {kpi_rate}, Present Count: {kpi_count}")
        assert len(kpi_rate) > 0
        assert len(kpi_count) > 0

        # Check telemetry cards have no footer clutter
        card_footers = page.locator(".telemetry-card .border-t").count()
        print(f"Telemetry card border-t footers: {card_footers} (expected 0)")
        assert card_footers == 0, "Telemetry cards must not have footer clutter"

        # 3. Check Table rendering
        rows = page.locator("#attendanceTableBody tr")
        row_count = rows.count()
        print(f"Initial table rows: {row_count}")
        assert row_count >= 20, f"Expected at least 20 rows, got {row_count}"

        # 4. Check Checkpoint Flow in row 1
        row1_flow = page.locator("#attendanceTableBody tr").first.locator("td:nth-child(5)").inner_text()
        print(f"Row 1 Checkpoint Flow: {row1_flow}")
        assert "Gate" in row1_flow or "Scanner" in row1_flow

        # 5. Check Master Checkbox & Batch Selection
        master_cb = page.locator("#selectAllCheckbox")
        master_cb.check()
        time.sleep(0.5)

        selected_count = page.locator("#selectedCount").inner_text()
        print(f"Selected count after master check: {selected_count}")
        assert int(selected_count) >= 20

        # Click Batch SMS
        page.locator("#btnBatchSms").click()
        time.sleep(0.5)
        toast_text = page.locator("#toast").inner_text()
        print(f"Toast after Batch SMS: {toast_text}")
        assert "SMS" in toast_text

        # Uncheck master
        master_cb.uncheck()
        time.sleep(0.3)
        assert page.locator("#selectedCount").inner_text() == "0"

        # 6. Test Search filter
        search_input = page.locator("#attSearchInput")
        search_input.fill("Sophea")
        time.sleep(0.5)
        filtered_rows = page.locator("#attendanceTableBody tr").count()
        print(f"Rows after searching 'Sophea': {filtered_rows}")
        assert filtered_rows >= 1

        # Test Reset
        page.locator("button[title='Reset All Filters']").click()
        time.sleep(0.5)
        reset_rows = page.locator("#attendanceTableBody tr").count()
        print(f"Rows after reset: {reset_rows}")
        assert reset_rows == row_count

        # 7. Test Snapshot Modal
        snapshot_btn = page.locator("#attendanceTableBody tr").first.locator("button[title='Gate Camera Snapshot']")
        if snapshot_btn.count() > 0:
            snapshot_btn.click()
            time.sleep(0.5)
            assert not page.locator("#snapshotModal").is_hidden()
            snap_name = page.locator("#snapName").inner_text()
            print(f"Snapshot modal opened for: {snap_name}")
            page.screenshot(path="C:/Users/oudom/.gemini/antigravity/brain/8fd19b10-a09a-43d8-a122-cb4a75dc0ff6/attendance_snapshot_modal.png")
            page.locator("#snapshotModal button:has-text('Close')").click()
            time.sleep(0.3)
            assert page.locator("#snapshotModal").is_hidden()

        # 8. Test History Audit Modal
        history_btn = page.locator("#attendanceTableBody tr").first.locator("button[title='Audit Ledger Trail']")
        if history_btn.count() > 0:
            history_btn.click()
            time.sleep(0.5)
            assert not page.locator("#historyModal").is_hidden()
            hist_title = page.locator("#histTitle").inner_text()
            print(f"History modal opened: {hist_title}")
            page.locator("#historyModal button:has-text('Close Audit')").click()
            time.sleep(0.3)
            assert page.locator("#historyModal").is_hidden()

        # 9. Test Official Correction Modal
        audit_btn = page.locator("#attendanceTableBody tr").first.locator("button[title*='Audit']").first
        audit_btn.click()
        time.sleep(0.5)
        assert not page.locator("#correctionModal").is_hidden()
        corr_name = page.locator("#corrStudentName").inner_text()
        print(f"Correction modal opened for: {corr_name}")
        page.screenshot(path="C:/Users/oudom/.gemini/antigravity/brain/8fd19b10-a09a-43d8-a122-cb4a75dc0ff6/attendance_correction_modal.png")
        page.locator("#correctionModal button:has-text('Cancel')").click()
        time.sleep(0.3)
        assert page.locator("#correctionModal").is_hidden()

        # Capture Desktop Full Page Screenshot
        page.screenshot(path="C:/Users/oudom/.gemini/antigravity/brain/8fd19b10-a09a-43d8-a122-cb4a75dc0ff6/attendance_redesigned_desktop.png")
        print("Desktop screenshot captured!")

        # 10. Test Mobile Viewport
        page.set_viewport_size({'width': 375, 'height': 812})
        time.sleep(0.5)
        mobile_header = page.locator("header.lg\\:hidden")
        assert mobile_header.is_visible()
        hamburger = mobile_header.locator("button[data-action='toggle-sidebar']")
        assert hamburger.is_visible()
        print("Mobile header and hamburger verified!")

        page.screenshot(path="C:/Users/oudom/.gemini/antigravity/brain/8fd19b10-a09a-43d8-a122-cb4a75dc0ff6/attendance_redesigned_mobile.png")
        print("Mobile screenshot captured!")

        print(f"Total console errors: {len(console_errors)}")
        if console_errors:
            print("Errors:", console_errors)
        assert len(console_errors) == 0

        browser.close()
        print("\nALL PLAYWRIGHT TESTS PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    test_attendance()


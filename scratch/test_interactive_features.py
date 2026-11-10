import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1440, "height": 900})
        await page.goto("http://127.0.0.1:3000/pages/principal/principal-teacher-profiles.html")
        await page.wait_for_timeout(2000)

        # 1. Test Search
        search_input = await page.wait_for_selector("#dirSearch")
        await search_input.fill("Sarah")
        await page.wait_for_timeout(500)
        rows = await page.query_selector_all(".teacher-row-card")
        print("1. Search 'Sarah' rows found:", len(rows))
        assert len(rows) == 1, "Expected 1 row for Sarah"
        await page.screenshot(path="scratch/test_search_sarah.png")

        # Clear search
        await search_input.fill("")
        await page.wait_for_timeout(500)
        rows_all = await page.query_selector_all(".teacher-row-card")
        print("2. Search cleared, total rows:", len(rows_all))

        # 2. Test Inline Editing and Saving
        first_edit = await page.query_selector('[data-act="edit-row"]')
        await first_edit.click()
        await page.wait_for_timeout(500)

        # Modify Target Workload to 20
        target_input = await page.query_selector('[id^="edTarget_"]')
        await target_input.fill("20")

        # Click Save Changes
        save_btn = await page.query_selector('[data-act="save-editor"]')
        await save_btn.click()
        await page.wait_for_timeout(1000)

        # Verify toast or updated target
        first_row_text = await page.inner_text(".teacher-row-card")
        print("3. Updated target in row:", "20 hrs/wk" in first_row_text)
        assert "20 hrs/wk" in first_row_text, "Expected '20 hrs/wk' in updated row"

        # 3. Test Add Teacher inline form
        add_btn = await page.query_selector("#btnAddTeacher")
        await add_btn.click()
        await page.wait_for_timeout(500)
        new_form = await page.query_selector("#newTeacherRowWrap:not(.hidden)")
        print("4. Add Teacher inline form open?", new_form is not None)
        await page.screenshot(path="scratch/test_add_teacher_form.png")

        # Close Add Teacher form
        cancel_add = await page.query_selector("#btnDiscardNewTeacher")
        await cancel_add.click()
        await page.wait_for_timeout(300)

        # 4. Test Excel Import Modal
        paste_btn = await page.query_selector("#btnPasteExcel")
        await paste_btn.click()
        await page.wait_for_timeout(500)
        excel_modal = await page.query_selector("#excelImportModal:not(.hidden)")
        print("5. Excel Paste Modal open?", excel_modal is not None)

        # Paste sample row
        sample_tsv = "Khem Sovan\tComputer Science\tICT Department\tkhem.sovan@ngis.edu.kh\tCS1\t18"
        paste_area = await page.query_selector("#excelPasteInput")
        await paste_area.fill(sample_tsv)
        await page.wait_for_timeout(500)

        preview_count = await page.inner_text("#excelParsedCount")
        print("6. Parsed records preview count:", preview_count)
        assert preview_count == "1", "Expected 1 parsed record"
        await page.screenshot(path="scratch/test_excel_paste_modal.png")

        # Close Excel Modal
        close_btn = await page.query_selector("#excelImportModal button:has-text('Cancel')")
        await close_btn.click()
        await page.wait_for_timeout(300)

        # 5. Test Mobile View at 390px
        await page.set_viewport_size({"width": 390, "height": 844})
        await page.wait_for_timeout(500)
        await page.screenshot(path="scratch/test_mobile_390.png", full_page=True)

        # Test Narrow Mobile View at 320px
        await page.set_viewport_size({"width": 320, "height": 700})
        await page.wait_for_timeout(500)
        await page.screenshot(path="scratch/test_mobile_320.png", full_page=True)
        print("7. Mobile 390px and 320px screenshots captured")

        print("ALL TESTS PASSED SUCCESSFULLY!")
        await browser.close()

asyncio.run(run())


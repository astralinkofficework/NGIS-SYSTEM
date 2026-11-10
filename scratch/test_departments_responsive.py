import asyncio
from playwright.async_api import async_playwright
import os

ARTIFACT_DIR = r"C:\Users\oudom\.gemini\antigravity\brain\8fd19b10-a09a-43d8-a122-cb4a75dc0ff6"

async def test_departments():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        
        viewports = [
            ("Desktop", 1440, 900),
            ("Tablet", 768, 1024),
            ("Mobile", 375, 812)
        ]

        auth_storage = {
            "ngis_role": "principal",
            "ngis_token": "mock-token",
            "ngis_user": '{"id":"PRN-2024-002","name":"Dr. Ly Bunheng","role":"principal"}',
            "ngis-theme": "light"
        }

        url = "http://127.0.0.1:3000/pages/principal/principal-departments.html"

        print(f"\n==========================================")
        print(f" TESTING Academic Departments ({url})")
        print(f"==========================================")

        for vp_name, w, h in viewports:
            context = await browser.new_context(viewport={"width": w, "height": h})
            page = await context.new_page()

            # Set localStorage
            await page.goto("http://127.0.0.1:3000/")
            await page.evaluate(f"""() => {{
                for (const [k, v] of Object.entries({auth_storage})) {{
                    localStorage.setItem(k, v);
                }}
            }}""")

            await page.goto(url, wait_until="domcontentloaded")
            await page.wait_for_selector("#departmentsTableBody tr", timeout=8000)
            await page.wait_for_timeout(600)

            # Check Search Input padding
            search_input = page.locator("#deptSearchInput")
            await search_input.wait_for(state="visible", timeout=10000)
            computed_pl = await search_input.evaluate("el => window.getComputedStyle(el).paddingLeft")
            print(f"[{vp_name}] Search padding-left: {computed_pl}")
            assert float(computed_pl.replace("px", "")) >= 40, f"Search padding-left too small: {computed_pl}"

            # Check 4 KPI cards
            kpis = page.locator(".telemetry-card")
            kpi_count = await kpis.count()
            print(f"[{vp_name}] KPI telemetry cards count: {kpi_count}")
            assert kpi_count == 4, f"Expected 4 KPI cards, got {kpi_count}"

            # Check Table rows
            rows = page.locator("#departmentsTableBody tr")
            row_count = await rows.count()
            print(f"[{vp_name}] Table row count: {row_count}")
            assert row_count >= 5, f"Expected at least 5 rows, got {row_count}"

            # Test Search input
            await search_input.fill("math")
            await page.wait_for_timeout(300)
            filtered_count = await page.locator("#departmentsTableBody tr").count()
            print(f"[{vp_name}] Filtered row count for 'math': {filtered_count}")
            assert filtered_count >= 1, "Filter for 'math' returned no rows"

            # Clear search
            clear_btn = page.locator("#clearDeptSearch")
            if await clear_btn.is_visible():
                await clear_btn.click()
                await page.wait_for_timeout(300)

            # Screenshot
            shot_path = os.path.join(ARTIFACT_DIR, f"departments_{vp_name.lower()}.png")
            await page.screenshot(path=shot_path, full_page=False)
            print(f"[{vp_name}] Screenshot saved: {shot_path}")

            # Test View Syllabi modal on Desktop
            if vp_name == "Desktop":
                view_btn = page.locator('button:has-text("View Syllabi")').first
                await view_btn.click()
                await page.wait_for_timeout(600)
                fac_modal = page.locator("#facultyModal")
                assert await fac_modal.is_visible(), "Faculty modal failed to open!"
                
                modal_shot = os.path.join(ARTIFACT_DIR, "departments_faculty_modal_desktop.png")
                await page.screenshot(path=modal_shot, full_page=False)
                print(f"[{vp_name}] Faculty modal screenshot saved: {modal_shot}")
                await page.keyboard.press("Escape")
                await page.wait_for_timeout(300)

                # Test Grid view mode
                grid_btn = page.locator("#btnViewGrid")
                await grid_btn.click()
                await page.wait_for_timeout(400)
                grid_container = page.locator("#departmentsGrid")
                assert await grid_container.is_visible(), "Grid view failed to display!"
                grid_shot = os.path.join(ARTIFACT_DIR, "departments_grid_desktop.png")
                await page.screenshot(path=grid_shot, full_page=False)
                print(f"[{vp_name}] Grid view screenshot saved: {grid_shot}")

                # Switch back to table
                table_btn = page.locator("#btnViewTable")
                await table_btn.click()
                await page.wait_for_timeout(300)

            await context.close()

        await browser.close()
        print("\n ALL DEPARTMENTS RESPONSIVENESS AND INTERACTION TESTS PASSED!")

if __name__ == "__main__":
    asyncio.run(test_departments())


import asyncio
from playwright.async_api import async_playwright
import os

ARTIFACT_DIR = r"C:\Users\oudom\.gemini\antigravity\brain\8fd19b10-a09a-43d8-a122-cb4a75dc0ff6"

async def test_profiles():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        
        pages_to_test = [
            ("Teacher Profiles", "http://127.0.0.1:3000/pages/principal/principal-teacher-profiles.html", "teacher"),
            ("Student Profiles", "http://127.0.0.1:3000/pages/principal/principal-student-profiles.html", "student")
        ]
        
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

        for title, url, kind in pages_to_test:
            print(f"\n==========================================")
            print(f" TESTING {title} ({url})")
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
                await page.wait_for_selector("#dirBody tr", timeout=8000)
                await page.wait_for_timeout(600)

                # Verify Search Input padding
                search_input = page.locator("#dirSearch")
                await search_input.wait_for(state="visible", timeout=10000)
                
                computed_pl = await search_input.evaluate("el => window.getComputedStyle(el).paddingLeft")
                print(f"[{vp_name}] Search padding-left: {computed_pl}")
                assert float(computed_pl.replace("px", "")) >= 40, f"Search padding-left too small: {computed_pl}"

                # Verify KPI cards count
                kpis = page.locator(".telemetry-card")
                kpi_count = await kpis.count()
                print(f"[{vp_name}] KPI telemetry cards count: {kpi_count}")
                assert kpi_count == 4, f"Expected 4 KPI cards, got {kpi_count}"

                # Verify table rows loaded
                rows = page.locator("#dirBody tr")
                row_count = await rows.count()
                print(f"[{vp_name}] Table row count: {row_count}")
                assert row_count > 0, "No rows rendered in table!"

                # Test search filtering functionality
                test_term = "a"
                await search_input.fill(test_term)
                await page.wait_for_timeout(300)
                filtered_rows = await page.locator("#dirBody tr").count()
                print(f"[{vp_name}] Filtered row count after search '{test_term}': {filtered_rows}")

                # Clear search
                clear_btn = page.locator("#clearSearch")
                if await clear_btn.is_visible():
                    await clear_btn.click()
                    await page.wait_for_timeout(300)

                # Screenshot
                shot_path = os.path.join(ARTIFACT_DIR, f"{kind}_profiles_{vp_name.lower()}.png")
                await page.screenshot(path=shot_path, full_page=False)
                print(f"[{vp_name}] Screenshot saved: {shot_path}")

                # On Desktop, test opening Profile modal
                if vp_name == "Desktop":
                    profile_btn = page.locator('button[data-act="view"]').first
                    await profile_btn.click()
                    await page.wait_for_timeout(800)
                    modal = page.locator("#profileModal")
                    is_modal_visible = await modal.is_visible()
                    print(f"[{vp_name}] Profile modal opened: {is_modal_visible}")
                    assert is_modal_visible, "Profile modal failed to open!"
                    
                    # Screenshot modal
                    modal_shot = os.path.join(ARTIFACT_DIR, f"{kind}_modal_desktop.png")
                    await page.screenshot(path=modal_shot, full_page=False)
                    print(f"[{vp_name}] Modal screenshot saved: {modal_shot}")

                    # Close modal
                    await page.keyboard.press("Escape")
                    await page.wait_for_timeout(300)

                await context.close()

        await browser.close()
        print("\n ALL PROFILE RESPONSIVENESS AND INTERACTION TESTS PASSED!")

if __name__ == "__main__":
    asyncio.run(test_profiles())

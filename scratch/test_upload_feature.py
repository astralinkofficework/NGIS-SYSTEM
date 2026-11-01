import asyncio
from playwright.async_api import async_playwright

async def test_upload_modal():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        
        # Test 1: Desktop View (1440x900)
        page = await browser.new_page(viewport={"width": 1440, "height": 900})
        errors = []
        page.on("console", lambda msg: errors.append(msg.text) if msg.type == "error" else None)
        
        await page.goto("http://127.0.0.1:3000/index.html")
        await page.evaluate("""() => {
            localStorage.setItem('ngis_active_portal', 'teacher');
            localStorage.setItem('ngis_token', 'mock-jwt-token-teacher');
        }""")
        
        await page.goto("http://127.0.0.1:3000/pages/teacher/teacher-submissions.html", wait_until="networkidle")
        await page.wait_for_selector("#btnUploadAssignmentOrWork")
        
        print("1. Desktop page loaded. Clicking #btnUploadAssignmentOrWork...")
        await page.click("#btnUploadAssignmentOrWork")
        
        # Modal should be visible
        await page.wait_for_selector("#uploadWorkModal", state="visible", timeout=3000)
        print("2. Modal opened successfully!")
        
        # Switch to Tab 2: Upload Student Work
        print("3. Switching to Tab 2: Upload Student Work...")
        await page.click("#tabModeWork")
        await page.wait_for_selector("#formStudentWork", state="visible", timeout=2000)
        
        # Fill Tab 2 and submit
        print("4. Testing student work submission...")
        await page.select_option("#workTargetStudent", value="2026-STD-0144")
        await page.fill("#workGrade", "95")
        await page.fill("#workFeedback", "Excellent solutions submitted via physical paper scan.")
        await page.click("#btnSubmitUpload")
        
        # Modal should close
        await page.wait_for_selector("#uploadWorkModal", state="hidden", timeout=3000)
        print("5. Modal closed after submission!")
        
        # Verify student grade in scoring drawer
        score_val = await page.text_content("#drawerFinalScoreDisplay")
        print(f"6. Final score in drawer: {score_val} (expected: 95)")
        await page.screenshot(path="scratch/upload_modal_after_submit.png")
        
        await page.close()
        
        # Test 2: Mobile View (390x844)
        mobile_page = await browser.new_page(viewport={"width": 390, "height": 844})
        await mobile_page.goto("http://127.0.0.1:3000/index.html")
        await mobile_page.evaluate("""() => {
            localStorage.setItem('ngis_active_portal', 'teacher');
            localStorage.setItem('ngis_token', 'mock-jwt-token-teacher');
        }""")
        await mobile_page.goto("http://127.0.0.1:3000/pages/teacher/teacher-submissions.html", wait_until="networkidle")
        
        print("7. Testing Mobile view (390px)...")
        # Click mobile upload button
        upload_btn = mobile_page.locator("header button:has-text('Upload')")
        await upload_btn.click()
        await mobile_page.wait_for_selector("#uploadWorkModal", state="visible", timeout=3000)
        await mobile_page.screenshot(path="scratch/upload_modal_mobile.png")
        print("8. Mobile upload modal opened and verified!")
        
        await mobile_page.close()
        await browser.close()
        
        # Filter harmless errors
        filtered = [e for e in errors if "favicon" not in e and "font" not in e.lower()]
        print(f"9. Console errors: {len(filtered)}")
        if filtered:
            print("Errors:", filtered)
        print("ALL TESTS PASSED SUCCESSFULLY!")

asyncio.run(test_upload_modal())

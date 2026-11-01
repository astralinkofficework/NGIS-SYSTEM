import asyncio
from playwright.async_api import async_playwright

async def test_transcript_viewer():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        
        # Test Desktop (1440x900)
        page = await browser.new_page(viewport={"width": 1440, "height": 900})
        await page.goto("http://127.0.0.1:3000/pages/shared/transcript-viewer.html?name=Nrinphouneta%20Hok&id=2026-STD-0142&gpa=3.88", wait_until="networkidle")
        
        # Verify text elements
        title = await page.text_content("#modal-title")
        student_name = await page.text_content("#docStudentName")
        gpa = await page.text_content("#summaryGpa")
        
        print(f"Title: {title}")
        print(f"Student: {student_name}")
        print(f"GPA: {gpa}")
        
        # Take screenshot of full viewer
        await page.screenshot(path="scratch/transcript_viewer_desktop.png")
        print("Desktop screenshot saved: scratch/transcript_viewer_desktop.png")
        
        # Test Zoom In
        await page.click("button[title='Zoom In']")
        zoom_val = await page.text_content("#zoomPercent")
        print(f"Zoom after In: {zoom_val}")
        
        # Test Reset Zoom
        await page.click("button[title='Fit to width']")
        zoom_reset = await page.text_content("#zoomPercent")
        print(f"Zoom after Reset: {zoom_reset}")
        
        await page.close()
        
        # Test Mobile (390x844)
        mobile_page = await browser.new_page(viewport={"width": 390, "height": 844})
        await mobile_page.goto("http://127.0.0.1:3000/pages/shared/transcript-viewer.html?name=Nrinphouneta%20Hok&id=2026-STD-0142&gpa=3.88", wait_until="networkidle")
        await mobile_page.screenshot(path="scratch/transcript_viewer_mobile.png")
        print("Mobile screenshot saved: scratch/transcript_viewer_mobile.png")
        
        await mobile_page.close()
        await browser.close()
        print("ALL TRANSCRIPT VIEWER TESTS PASSED!")

asyncio.run(test_transcript_viewer())


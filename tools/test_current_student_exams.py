import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1280, "height": 900})
        
        errors = []
        page.on("pageerror", lambda err: errors.append(str(err)))
        page.on("console", lambda msg: print(f"[{msg.type}] {msg.text}"))
        
        await page.goto("http://127.0.0.1:3000/pages/student/student-exams.html", wait_until="networkidle")
        await page.wait_for_timeout(1500)
        
        await page.screenshot(path="C:/Users/oudom/.gemini/antigravity/brain/f0e0db56-cd04-4f51-a7f8-40ba21b43536/current_student_exams.png")
        print("Screenshot saved to current_student_exams.png")
        
        # Check what HTML is inside examsWorkspace
        html = await page.locator("#examsWorkspace").inner_html()
        print(f"examsWorkspace length: {len(html)}")
        
        await browser.close()

asyncio.run(main())

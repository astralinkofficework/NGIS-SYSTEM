import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1280, "height": 900})
        await page.goto("http://127.0.0.1:3000/pages/student/student-exams.html", wait_until="networkidle")
        await page.wait_for_timeout(1000)
        
        # Get exams data from window / state
        exams = await page.evaluate('''() => {
            return window.__examsData || [];
        }''')
        
        html = await page.locator("#examsWorkspace").inner_html()
        print("HTML snippet:")
        print(html[:1500])
        
        await browser.close()

asyncio.run(main())

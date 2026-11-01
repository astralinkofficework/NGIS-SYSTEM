import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1440, "height": 900})
        await page.goto("http://127.0.0.1:3000/pages/student/student.html", wait_until="networkidle")
        await page.screenshot(path="scratch/current_student_screenshot.png")
        print("Screenshot saved to scratch/current_student_screenshot.png")
        await browser.close()

asyncio.run(main())


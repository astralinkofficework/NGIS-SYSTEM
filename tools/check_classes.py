import asyncio
from playwright.async_api import async_playwright

async def test():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto('http://127.0.0.1:3000/pages/shared/department.html', wait_until='domcontentloaded')
        classes = await page.evaluate("() => document.querySelector('#cardAttendance').className")
        print("Classes on #cardAttendance:", repr(classes))
        await browser.close()

asyncio.run(test())

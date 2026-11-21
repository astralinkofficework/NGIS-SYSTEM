import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={'width': 1280, 'height': 850})
        await page.goto('http://127.0.0.1:3000/pages/student/student-exams.html', wait_until='networkidle')
        await page.wait_for_timeout(500)
        hero = await page.evaluate("() => document.getElementById('heroBanner')?.offsetHeight")
        workspace = await page.evaluate("() => document.getElementById('examsWorkspace')?.getBoundingClientRect()")
        print("Hero height:", hero)
        print("Workspace rect:", workspace)
        await browser.close()

if __name__ == '__main__':
    asyncio.run(run())

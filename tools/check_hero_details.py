import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={'width': 1280, 'height': 850})
        await page.goto('http://127.0.0.1:3000/pages/student/student-exams.html', wait_until='networkidle')
        await page.wait_for_timeout(500)
        info = await page.evaluate("""() => {
            const h = document.querySelector('header');
            const nav = document.querySelector('.topbar, nav, header');
            const hero = document.getElementById('heroBanner');
            return {
                headerExists: !!h,
                heroExists: !!hero,
                heroHeight: hero ? hero.offsetHeight : 0,
                heroHTML: hero ? hero.outerHTML.slice(0, 100) : ''
            };
        }""")
        print(info)
        await browser.close()

if __name__ == '__main__':
    asyncio.run(run())

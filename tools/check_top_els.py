import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={'width': 1280, 'height': 850})
        await page.goto('http://127.0.0.1:3000/pages/student/student-exams.html', wait_until='networkidle')
        await page.wait_for_timeout(500)
        top_elements = await page.evaluate("""() => {
            const els = Array.from(document.body.children).filter(el => el.offsetParent !== null);
            return els.map(el => ({ tag: el.tagName, id: el.id, class: el.className, rect: el.getBoundingClientRect() }));
        }""")
        for el in top_elements:
            print(el)
        await browser.close()

if __name__ == '__main__':
    asyncio.run(run())

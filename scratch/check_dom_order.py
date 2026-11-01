import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.set_viewport_size({'width': 390, 'height': 844})
        await page.goto('http://127.0.0.1:3000/pages/student/student.html', wait_until='networkidle')
        
        children = await page.evaluate('''() => {
            return Array.from(document.body.children).map(c => ({
                tag: c.tagName,
                id: c.id,
                className: c.className,
                offsetHeight: c.offsetHeight,
                display: window.getComputedStyle(c).display,
                position: window.getComputedStyle(c).position
            }));
        }''')
        for idx, ch in enumerate(children):
            print(f"{idx}: {ch['tag']}#{ch['id']}.{ch['className']} - display:{ch['display']}, pos:{ch['position']}, h:{ch['offsetHeight']}")
        await browser.close()

asyncio.run(main())

import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.set_viewport_size({'width': 390, 'height': 844})
        await page.goto('http://127.0.0.1:3000/pages/student/student.html', wait_until='networkidle')
        
        info = await page.evaluate('''() => {
            const shell = document.querySelector('.shell');
            const children = shell ? Array.from(shell.children).map(c => ({
                tag: c.tagName,
                id: c.id,
                className: c.className,
                display: window.getComputedStyle(c).display,
                h: c.offsetHeight
            })) : [];
            return {
                shellDisplay: shell ? window.getComputedStyle(shell).display : null,
                shellHeight: shell ? shell.offsetHeight : null,
                children: children
            };
        }''')
        print(info)
        await browser.close()

asyncio.run(main())

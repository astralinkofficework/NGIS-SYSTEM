import asyncio
from playwright.async_api import async_playwright

async def inspect_mobile_hb():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        for page_name, url in [
            ('Student', 'http://127.0.0.1:3000/pages/student/student.html'),
            ('Teacher', 'http://127.0.0.1:3000/pages/teacher/teacher.html'),
            ('Principal', 'http://127.0.0.1:3000/pages/principal/principal.html')
        ]:
            page = await browser.new_page(viewport={'width': 390, 'height': 844})
            await page.goto(url, wait_until='domcontentloaded')
            await page.wait_for_timeout(1000)
            
            res = await page.evaluate('''() => {
                const candidates = document.querySelectorAll('button, a, div');
                const matches = [];
                candidates.forEach(el => {
                    const cls = el.className || '';
                    const action = el.getAttribute('data-action') || '';
                    if (cls.includes('hamburger') || action === 'toggle-sidebar' || el.querySelector('.ph-list, [data-action="toggle-sidebar"]')) {
                        const r = el.getBoundingClientRect();
                        matches.push({
                            tag: el.tagName,
                            cls: cls,
                            action: action,
                            w: r.width,
                            h: r.height,
                            x: r.x,
                            y: r.y,
                            display: getComputedStyle(el).display,
                            visibility: getComputedStyle(el).visibility,
                            parent: el.parentElement ? el.parentElement.className : null
                        });
                    }
                });
                return matches;
            }''')
            print(f'=== {page_name} ===')
            for m in res:
                print(m)
        await browser.close()

asyncio.run(inspect_mobile_hb())


import asyncio
from playwright.async_api import async_playwright

async def inspect_dom():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={'width': 390, 'height': 844})
        await page.goto('http://127.0.0.1:3000/pages/teacher/teacher-lost-found.html', wait_until='networkidle')
        await page.wait_for_timeout(1000)
        
        info = await page.evaluate("""() => {
            const btns = Array.from(document.querySelectorAll('button')).map(b => ({
                id: b.id,
                cls: b.className,
                action: b.getAttribute('data-action'),
                vis: b.offsetParent !== null,
                rect: b.getBoundingClientRect()
            }));
            const header = document.querySelector('header');
            const topbar = document.querySelector('.topbar, .htb, .lh-topbar');
            const sidebar = document.getElementById('sidebar');
            return {
                buttons: btns,
                hasHeader: !!header,
                hasTopbar: !!topbar,
                hasSidebar: !!sidebar,
                sidebarClasses: sidebar ? sidebar.className : null
            };
        }""")
        import pprint
        pprint.pprint(info)
        await browser.close()

asyncio.run(inspect_dom())


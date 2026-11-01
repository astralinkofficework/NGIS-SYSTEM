import asyncio
from playwright.async_api import async_playwright

async def measure():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1440, "height": 900})
        await page.goto("http://127.0.0.1:3000/pages/student/student.html", wait_until="domcontentloaded")
        await page.wait_for_selector(".dash-overlap")
        await page.wait_for_timeout(1000)
        
        info = await page.evaluate("""() => {
            const deck = document.querySelector('.dash-overlap');
            const profile = document.querySelector('.ov-profile');
            const upcoming = document.querySelector('.ov-upcoming');
            const deadlines = document.querySelector('.ov-deadlines');
            const panels = Array.from(document.querySelectorAll('.ov-inner-panel'));
            const deadlinePanels = Array.from(document.querySelectorAll('.ov-deadline-panel'));
            const feedBody = document.querySelector('.ov-upcoming [style*="max-height"]');
            
            return {
                deckHeight: deck?.getBoundingClientRect().height,
                profileHeight: profile?.getBoundingClientRect().height,
                upcomingHeight: upcoming?.getBoundingClientRect().height,
                deadlinesHeight: deadlines?.getBoundingClientRect().height,
                panels: panels.map(p => ({
                    head: p.querySelector('.ov-inner-head')?.textContent.trim(),
                    height: p.getBoundingClientRect().height,
                    itemCount: p.querySelectorAll('.ov-inner-item').length
                })),
                deadlinePanels: deadlinePanels.map(p => ({
                    head: p.querySelector('.ov-deadline-head')?.textContent.trim(),
                    height: p.getBoundingClientRect().height,
                    itemCount: p.querySelectorAll('.ov-deadline-item').length
                })),
                feedBodyHeight: feedBody?.getBoundingClientRect().height
            };
        }""")
        
        print("Panel measurements:")
        import pprint
        pprint.pprint(info)
        await browser.close()

asyncio.run(measure())

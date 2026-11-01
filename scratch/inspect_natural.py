import asyncio
from playwright.async_api import async_playwright

async def inspect():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1440, "height": 900})
        await page.goto("http://127.0.0.1:3000/pages/student/student.html", wait_until="domcontentloaded")
        await page.wait_for_selector(".dash-overlap")
        await page.wait_for_timeout(500)
        
        info = await page.evaluate("""() => {
            const profile = document.querySelector('.ov-profile');
            const upcoming = document.querySelector('.ov-upcoming');
            const deadlines = document.querySelector('.ov-deadlines');
            
            // Measure natural content heights by temporarily setting height: auto and align-items: flex-start on .dash-overlap
            const deck = document.querySelector('.dash-overlap');
            deck.style.alignItems = 'flex-start';
            profile.style.height = 'auto';
            upcoming.style.height = 'auto';
            deadlines.style.height = 'auto';
            
            return {
                profileNaturalHeight: profile.scrollHeight,
                profileClientHeight: profile.clientHeight,
                upcomingNaturalHeight: upcoming.scrollHeight,
                upcomingClientHeight: upcoming.clientHeight,
                deadlinesNaturalHeight: deadlines.scrollHeight,
                deadlinesClientHeight: deadlines.clientHeight,
                
                // Why dlItems are 63.8px:
                dlItemInfo: Array.from(document.querySelectorAll('.ov-deadline-item')).map(it => ({
                    html: it.outerHTML,
                    computed: {
                        display: window.getComputedStyle(it).display,
                        lineHeight: window.getComputedStyle(it).lineHeight,
                        fontSize: window.getComputedStyle(it).fontSize
                    }
                }))
            };
        }""")
        
        import pprint
        pprint.pprint({
            'profileNaturalHeight': info['profileNaturalHeight'],
            'upcomingNaturalHeight': info['upcomingNaturalHeight'],
            'deadlinesNaturalHeight': info['deadlinesNaturalHeight'],
            'dlItemHtml': info['dlItemInfo'][0] if info['dlItemInfo'] else None
        })
        await browser.close()

asyncio.run(inspect())


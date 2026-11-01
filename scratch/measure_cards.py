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
            const profileHeader = document.querySelector('.ov-profile-header');
            const profileBody = document.querySelector('.ov-profile-body');
            const actions = document.querySelector('.ov-actions');
            const promo = document.querySelector('.promo-slideshow');
            
            return {
                deckHeight: deck ? deck.getBoundingClientRect().height : null,
                profileHeight: profile ? profile.getBoundingClientRect().height : null,
                upcomingHeight: upcoming ? upcoming.getBoundingClientRect().height : null,
                deadlinesHeight: deadlines ? deadlines.getBoundingClientRect().height : null,
                profileHeaderHeight: profileHeader ? profileHeader.getBoundingClientRect().height : null,
                profileBodyHeight: profileBody ? profileBody.getBoundingClientRect().height : null,
                actionsHeight: actions ? actions.getBoundingClientRect().height : null,
                gapInsideProfile: actions.getBoundingClientRect().top - profileBody.getBoundingClientRect().bottom,
                promoTop: promo ? promo.getBoundingClientRect().top : null,
                promoBottom: promo ? promo.getBoundingClientRect().bottom : null,
                viewportHeight: window.innerHeight
            };
        }""")
        
        print("Live Card Measurements:")
        for k, v in info.items():
            print(f"  {k}: {v}")
            
        await page.screenshot(path="scratch/live_student_dashboard.png")
        print("Screenshot saved to scratch/live_student_dashboard.png")
        await browser.close()

asyncio.run(measure())

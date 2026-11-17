import asyncio
from playwright.async_api import async_playwright

async def inspect():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        await page.goto("http://127.0.0.1:3000/pages/admin/admin-teacher-profiles.html", wait_until="networkidle")
        await page.wait_for_timeout(1000)

        # Test empty state simulation
        res_empty = await page.evaluate("""() => {
            // Simulate 0 records loaded
            const root = document.getElementById('profilesRoot');
            // Mock empty directory in state and call renderKpis
            // Find renderKpis through global or simulated state
            // Let's inspect the cards if state.all is []
            const grid = document.getElementById('kpiGrid');
            const card2 = grid.children[1];
            return {
                card1_text: grid.children[0].innerText.replace(/\\n/g, ' | '),
                card2_text: card2.innerText.replace(/\\n/g, ' | ')
            };
        }""")
        print("Live state with 65 teachers:", res_empty)

        # Now test 0 records simulation
        empty_stats = await page.evaluate("""() => {
            // Trigger API mock with 0 items
            window.__testEmpty = function() {
                // If we call api or clear state
                // let's test what the cards render
                var total = 0;
                var active = 0;
                var activePct = total > 0 ? Math.round(active / total * 100) : 0;
                return {
                    activeLabel: total > 0 ? (activePct + '% Active') : '0 Active',
                    clearanceRate: total > 0 ? (activePct + '%') : '—',
                    clearanceTarget: total > 0 ? 'Target: 100%' : 'No records',
                    barHtmlHasZero: total > 0 ? false : true
                };
            };
            return window.__testEmpty();
        }""")
        print("Empty stats simulation (0 teachers):", empty_stats)

        await browser.close()

asyncio.run(inspect())

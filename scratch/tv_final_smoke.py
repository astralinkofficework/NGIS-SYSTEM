import asyncio
import json
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={'width': 1440, 'height': 900})
        errs = []
        page.on('pageerror', lambda e: errs.append(str(e)))

        # ── Services ──
        await page.goto('http://127.0.0.1:3000/pages/teacher/teacher-services.html', wait_until='networkidle')
        await page.wait_for_timeout(700)
        await page.click('[data-filter="completed"]')
        await page.wait_for_timeout(300)
        s1 = await page.evaluate("document.getElementById('tab-completed').className.includes('bg-primary')")
        await page.click('#fabNewRequestBtn')
        await page.wait_for_timeout(300)
        m1 = await page.evaluate("document.getElementById('newRequestModal').classList.contains('show')")
        await page.evaluate("closeNewRequestModal()")
        await page.click('[data-cat="it_support"]')
        await page.wait_for_timeout(300)
        await page.click('#tab-all')
        await page.screenshot(path='scratch/tv_services_final.png')
        print('services: tab pill activates:', s1, '| FAB opens modal:', m1)

        # ── Lost & Found ──
        await page.goto('http://127.0.0.1:3000/pages/teacher/teacher-lost-found.html', wait_until='networkidle')
        await page.wait_for_timeout(700)
        await page.click('[data-catpill="electronics"]')
        await page.wait_for_timeout(300)
        pill_on = await page.evaluate("document.querySelector('[data-catpill=electronics]').className.includes('bg-primary')")
        sel_synced = await page.evaluate("document.getElementById('filterCategory').value")
        await page.click('[data-catpill="all"]')
        await page.click('#fabReportItemBtn')
        await page.wait_for_timeout(300)
        m2 = await page.evaluate("document.getElementById('reportModal').classList.contains('show')")
        await page.evaluate("closeReportModal()")
        await page.click('#tab-claims')
        await page.wait_for_timeout(200)
        await page.click('#tab-all')
        cards = await page.evaluate("document.querySelectorAll('.item-card').length")
        await page.screenshot(path='scratch/tv_lostfound_final.png')
        print('lostfound: pill active:', pill_on, '| select synced:', sel_synced, '| FAB opens modal:', m2, '| cards after reset:', cards)

        # mobile screenshots
        await page.set_viewport_size({'width': 390, 'height': 844})
        for name, url in [('services', 'http://127.0.0.1:3000/pages/teacher/teacher-services.html'),
                          ('lostfound', 'http://127.0.0.1:3000/pages/teacher/teacher-lost-found.html')]:
            await page.goto(url, wait_until='networkidle')
            await page.wait_for_timeout(500)
            await page.screenshot(path=f'scratch/tv_{name}_mobile_final.png')

        print('page errors:', errs or 'NONE')
        await browser.close()

asyncio.run(main())

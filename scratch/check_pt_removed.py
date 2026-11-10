import asyncio
import json
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={'width': 1440, 'height': 900})
        errs = []
        page.on('pageerror', lambda e: errs.append(str(e)[:150]))
        await page.goto('http://127.0.0.1:3000/pages/principal/principal-teachers.html', wait_until='networkidle')
        await page.wait_for_timeout(800)
        info = await page.evaluate("""() => ({
          removedPill: !!document.getElementById('headerPendingCountPill'),
          removedCount: !!document.getElementById('showingEducatorsCount'),
          removedCrumb: document.body.innerText.includes('Principal Academic Oversight'),
          removedSub: document.body.innerText.includes('Real-time educator verification'),
          hero: !!document.querySelector('.hero .hero-topbar'),
          rows: document.querySelectorAll('#faculty-table-body tr').length,
          reviewBtn: (document.getElementById('reviewAllBtnText')||{}).textContent,
        })""")
        print(json.dumps(info, indent=1))
        print('page errors:', errs or 'NONE')
        await page.screenshot(path='scratch/principal_teachers_after_removal.png')
        await browser.close()

asyncio.run(main())

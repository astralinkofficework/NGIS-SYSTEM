import asyncio
import json
from playwright.async_api import async_playwright

URLS = [
    'http://127.0.0.1:3000/pages/teacher/teacher-services.html',
    'http://127.0.0.1:3000/pages/teacher/teacher-lost-found.html',
]

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={'width': 1440, 'height': 900})
        for url in URLS:
            await page.goto(url, wait_until='networkidle')
            await page.wait_for_timeout(600)
            info = await page.evaluate("""() => ({
              heroRendered: !!document.querySelector('.hero .hero-topbar'),
              htbProfile: !!document.getElementById('htbProfile'),
              htbHamburger: !!document.getElementById('htbHamburger'),
              heroClass: document.querySelector('.hero') ? document.querySelector('.hero').className : null,
            })""")
            print(url.split('/')[-1], '=>', json.dumps(info))
        await browser.close()

asyncio.run(main())

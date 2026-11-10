import asyncio
import glob
import json
from playwright.async_api import async_playwright

async def main():
    urls = []
    for f in sorted(glob.glob('pages/principal/*.html')):
        urls.append('http://127.0.0.1:3000/' + f.replace('\\', '/'))
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={'width': 1440, 'height': 900})
        errs = []
        page.on('pageerror', lambda e: errs.append(e))
        bad = []
        for url in urls:
            await page.goto(url, wait_until='networkidle')
            await page.wait_for_timeout(500)
            info = await page.evaluate("""() => ({
              hero: !!document.querySelector('.hero .hero-topbar'),
              title: (document.querySelector('.hero-title') || {}).textContent || null,
              sidebar: !!document.querySelector('aside, .sidebar'),
            })""")
            name = url.split('/')[-1]
            ok = info['hero'] and info['sidebar']
            if not ok:
                bad.append(name)
            print(name.ljust(32), 'hero:', info['hero'], '| sidebar:', info['sidebar'], '|', (info['title'] or '')[:40])
        print('BAD PAGES:', bad or 'NONE')
        print('page errors:', [str(e)[:120] for e in errs] or 'NONE')
        await browser.close()

asyncio.run(main())

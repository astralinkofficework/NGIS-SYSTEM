import asyncio
from playwright.async_api import async_playwright

async def inspect():
    errors = []
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={'width': 1440, 'height': 900})
        page.on('pageerror', lambda err: errors.append(f"PAGEERROR: {err}"))
        page.on('console', lambda msg: errors.append(f"CONSOLE {msg.type}: {msg.text}") if msg.type in ['error', 'warn'] else None)
        
        await page.goto('http://127.0.0.1:3000/pages/principal/principal-timetables.html', wait_until='networkidle')
        await page.wait_for_timeout(1000)
        
        print("Collected errors:")
        for e in errors:
            print(e)
            
        await browser.close()

asyncio.run(inspect())


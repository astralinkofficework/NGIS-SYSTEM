import asyncio, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={'width': 1440, 'height': 900})
        errs, notfound = [], []
        pg.on('pageerror', lambda e: errs.append(str(e)))
        for path in ['pages/teacher/teacher.html', 'pages/teacher/teacher-roster.html', 'pages/teacher/teacher-departments.html']:
            await pg.goto(f'http://127.0.0.1:3000/{path}', wait_until='networkidle')
            await pg.wait_for_timeout(500)
        # sidebar check
        items = await pg.evaluate("""() => [...document.querySelectorAll('#sidebar a, aside a, .sidebar a')]
            .map(a => a.textContent.replace(/\\s+/g,' ').trim().slice(0,40))""")
        print('My Classes in sidebar:', any('My Classes' in i for i in items))
        print('Roster & Profiles in sidebar:', any('Roster' in i for i in items))
        # dashboard View All link
        await pg.goto('http://127.0.0.1:3000/pages/teacher/teacher.html', wait_until='networkidle')
        await pg.click('a.sec-link:has-text("View All")')
        await pg.wait_for_load_state('networkidle')
        print('View All ->', pg.url.split('3000')[-1], '| rows/cards:', await pg.locator('table tbody tr, [class*=roster-card], [class*=class-card]').count())
        # old URL now 404s gracefully
        r = await pg.goto('http://127.0.0.1:3000/pages/teacher/teacher-classes.html?classId=cls-11b')
        print('old URL status:', r.status)
        print('page errors:', errs or 'NONE')
        await b.close()

asyncio.run(main())

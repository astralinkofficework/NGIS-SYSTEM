import asyncio
from playwright.async_api import async_playwright

PAGES = [
    ("Principal Dashboard", "http://127.0.0.1:3000/pages/principal/principal.html"),
    ("Principal Classes", "http://127.0.0.1:3000/pages/principal/principal-classes.html"),
    ("Teacher Dashboard", "http://127.0.0.1:3000/pages/teacher/teacher.html"),
    ("Teacher Gradebook", "http://127.0.0.1:3000/pages/teacher/teacher-gradebook.html"),
    ("Student Dashboard", "http://127.0.0.1:3000/pages/student/student.html"),
    ("Admin Dashboard", "http://127.0.0.1:3000/pages/admin/admin.html"),
]

async def audit():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={'width': 1440, 'height': 900})
        
        all_passed = True
        for name, url in PAGES:
            page = await context.new_page()
            await page.goto(url, wait_until='networkidle', timeout=15000)
            await page.wait_for_timeout(500)
            
            # Check H1
            h1_info = await page.evaluate('''() => {
                const el = document.querySelector('h1, .page-title, [data-purpose="page-title"]');
                if (!el) return null;
                const s = window.getComputedStyle(el);
                return {
                    tag: el.tagName,
                    fontFamily: s.fontFamily,
                    fontSize: s.fontSize,
                    fontWeight: s.fontWeight,
                    lineHeight: s.lineHeight
                };
            }''')
            
            # Check Body
            body_info = await page.evaluate('''() => {
                const s = window.getComputedStyle(document.body);
                return {
                    fontFamily: s.fontFamily,
                    fontSize: s.fontSize,
                    fontWeight: s.fontWeight
                };
            }''')

            # Check Button
            btn_info = await page.evaluate('''() => {
                const el = document.querySelector('button, .btn');
                if (!el) return null;
                const s = window.getComputedStyle(el);
                return {
                    fontFamily: s.fontFamily,
                    fontSize: s.fontSize,
                    fontWeight: s.fontWeight
                };
            }''')

            # Check Sidebar link
            nav_info = await page.evaluate('''() => {
                const el = document.querySelector('.nav-link');
                if (!el) return null;
                const s = window.getComputedStyle(el);
                return {
                    fontFamily: s.fontFamily,
                    fontSize: s.fontSize,
                    fontWeight: s.fontWeight
                };
            }''')
            
            print(f'=== {name} ===')
            if h1_info:
                print(f'  H1: font={h1_info["fontFamily"][:25]}, size={h1_info["fontSize"]}, weight={h1_info["fontWeight"]}, lh={h1_info["lineHeight"]}')
                if 'Manrope' not in h1_info['fontFamily'] or h1_info['fontSize'] != '28px':
                    print('  FAILED H1 requirements!')
                    all_passed = False
            else:
                print('  No H1 found')
                
            print(f'  Body: font={body_info["fontFamily"][:25]}, size={body_info["fontSize"]}, weight={body_info["fontWeight"]}')
            if 'Plus Jakarta Sans' not in body_info['fontFamily']:
                print('  FAILED Body requirements!')
                all_passed = False
                
            if btn_info:
                print(f'  Btn: font={btn_info["fontFamily"][:25]}, size={btn_info["fontSize"]}, weight={btn_info["fontWeight"]}')
            if nav_info:
                print(f'  Nav: font={nav_info["fontFamily"][:25]}, size={nav_info["fontSize"]}, weight={nav_info["fontWeight"]}')

            await page.close()
            
        await browser.close()
        print('All typography audit checks passed:', all_passed)

if __name__ == '__main__':
    asyncio.run(audit())


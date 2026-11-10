import asyncio
from playwright.async_api import async_playwright
import os

async def capture_all():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={'width': 1440, 'height': 900})
        
        pages_to_capture = [
            ('principal', 'http://127.0.0.1:3000/pages/principal/principal.html'),
            ('principal_classes', 'http://127.0.0.1:3000/pages/principal/principal-classes.html'),
            ('teacher', 'http://127.0.0.1:3000/pages/teacher/teacher.html'),
            ('teacher_gradebook', 'http://127.0.0.1:3000/pages/teacher/teacher-gradebook.html'),
            ('student', 'http://127.0.0.1:3000/pages/student/student.html'),
            ('admin', 'http://127.0.0.1:3000/pages/admin/admin.html'),
        ]
        
        for name, url in pages_to_capture:
            page = await context.new_page()
            try:
                await page.goto(url, wait_until='networkidle', timeout=15000)
                await page.wait_for_timeout(1000)
                out_path = f'scratch/green_{name}.png'
                await page.screenshot(path=out_path, full_page=False)
                print(f'Captured {name} -> {out_path}')
            except Exception as e:
                print(f'Failed {name}: {e}')
            finally:
                await page.close()
                
        # Also capture mobile view of principal-classes
        mob_context = await browser.new_context(viewport={'width': 375, 'height': 812}, is_mobile=True)
        mob_page = await mob_context.new_page()
        try:
            await mob_page.goto('http://127.0.0.1:3000/pages/principal/principal-classes.html', wait_until='networkidle', timeout=15000)
            await mob_page.wait_for_timeout(1000)
            out_mob = 'scratch/green_principal_classes_mobile.png'
            await mob_page.screenshot(path=out_mob, full_page=False)
            print(f'Captured mobile classes -> {out_mob}')
        except Exception as e:
            print(f'Failed mobile classes: {e}')
        finally:
            await mob_page.close()
            
        await browser.close()

if __name__ == '__main__':
    asyncio.run(capture_all())


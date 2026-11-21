import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context(viewport={'width': 1280, 'height': 850})
        page = await context.new_page()

        urls = [
            'http://127.0.0.1:3000/pages/teacher/teacher.html',
            'http://127.0.0.1:3000/pages/principal/principal.html',
            'http://127.0.0.1:3000/pages/admin/admin-security.html',
            'http://127.0.0.1:3000/pages/student/student.html',
            'http://127.0.0.1:3000/pages/admin/admin-roles.html'
        ]

        for u in urls:
            errors = []
            page.on('console', lambda msg: errors.append(msg.text) if msg.type == 'error' else None)
            await page.goto(u, wait_until='networkidle')
            await page.wait_for_timeout(400)
            has_motion = await page.evaluate("() => !!window.NGIS_MOTION")
            has_gsap = await page.evaluate("() => !!window.gsap")
            title = await page.title()
            print(f"[{'PASS' if has_motion and has_gsap else 'FAIL'}] {title[:35]} | motion={has_motion}, gsap={has_gsap}, errors={len(errors)}")

        await browser.close()

if __name__ == '__main__':
    asyncio.run(run())

import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={'width': 1440, 'height': 900})
        await page.goto("http://127.0.0.1:3000/index.html")
        await page.evaluate("""() => {
            localStorage.setItem('ngis_active_portal', 'teacher');
            localStorage.setItem('ngis_token', 'mock-jwt-token-teacher');
        }""")
        await page.goto('http://127.0.0.1:3000/pages/teacher/teacher-reports.html', wait_until='networkidle')
        await page.evaluate("window.previewReport('2026-STD-0142')")
        await page.wait_for_selector('#modalReportCard:not(.hidden)', timeout=3000)
        btn = await page.wait_for_selector('#btnOpenFullTranscript', timeout=2000)
        href = await btn.get_attribute('href')
        print('Full Viewer Link in teacher-reports:', href)
        await page.screenshot(path='scratch/teacher_reports_full_viewer_btn.png')
        await browser.close()
        print('SUCCESS!')

asyncio.run(run())

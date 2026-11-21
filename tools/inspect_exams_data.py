import asyncio
from playwright.async_api import async_playwright
import json

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1280, "height": 900})
        await page.goto("http://127.0.0.1:3000/pages/student/student-exams.html", wait_until="networkidle")
        await page.wait_for_timeout(1000)
        
        exams_data = await page.evaluate('''() => {
            // Find exams in state or DOM
            const lis = Array.from(document.querySelectorAll('.exw-exam'));
            return lis.map(li => {
                return {
                    day: li.querySelector('.exw-date-day')?.textContent,
                    month: li.querySelector('.exw-date-month')?.textContent,
                    title: li.querySelector('.exw-exam-title')?.textContent,
                    subject: li.querySelector('.exw-subject')?.textContent,
                    meta: Array.from(li.querySelectorAll('.exw-meta span')).map(s => s.textContent),
                    time: li.querySelector('.exw-time')?.textContent,
                    status: li.querySelector('.exw-status')?.textContent
                };
            });
        }''')
        
        print("Exams on page:")
        print(json.dumps(exams_data, indent=2))
        
        await browser.close()

asyncio.run(main())

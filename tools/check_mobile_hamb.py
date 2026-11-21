import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={'width': 375, 'height': 667})
        await page.goto('http://127.0.0.1:3000/pages/student/student-exams.html', wait_until='networkidle')
        await page.wait_for_timeout(500)
        
        btns = await page.evaluate("""() => {
            const list = Array.from(document.querySelectorAll('[data-action="toggle-sidebar"], .hamburger-btn, .mobile-hamburger-btn'));
            return list.map(b => ({
                id: b.id,
                className: b.className,
                rect: b.getBoundingClientRect(),
                display: window.getComputedStyle(b).display,
                visibility: window.getComputedStyle(b).visibility,
                parentDisplay: b.parentElement ? window.getComputedStyle(b.parentElement).display : null,
                grandParentDisplay: b.parentElement && b.parentElement.parentElement ? window.getComputedStyle(b.parentElement.parentElement).display : null
            }));
        }""")
        print("Buttons found:", len(btns))
        for b in btns:
            print(b)
        await browser.close()

if __name__ == '__main__':
    asyncio.run(run())

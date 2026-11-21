import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1440, "height": 900})
        await page.goto("http://127.0.0.1:3000/pages/student/student.html", wait_until="networkidle")
        
        info = await page.evaluate('''() => {
            const hero = document.querySelector('.hero');
            const topbar = document.querySelector('.hero-topbar');
            const title = document.querySelector('.hero-title');
            const greeting = document.querySelector('.hero-greeting');
            const date = document.querySelector('.hero-date');
            const body = document.querySelector('.hero-body');
            
            return {
                hero_bg: hero ? getComputedStyle(hero).backgroundColor : null,
                hero_color: hero ? getComputedStyle(hero).color : null,
                topbar_bg: topbar ? getComputedStyle(topbar).backgroundColor : null,
                topbar_border: topbar ? getComputedStyle(topbar).borderBottom : null,
                title_text: title ? title.textContent : null,
                title_color: title ? getComputedStyle(title).color : null,
                title_size: title ? getComputedStyle(title).fontSize : null,
                greeting_text: greeting ? greeting.textContent : null,
                date_text: date ? date.textContent : null,
                hero_html: hero ? hero.outerHTML.substring(0, 500) : null
            };
        }''')
        print(info)
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())

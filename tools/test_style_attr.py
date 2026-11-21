import asyncio
from playwright.async_api import async_playwright

async def test():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto('http://127.0.0.1:3000/pages/shared/department.html', wait_until='domcontentloaded')
        
        card = page.locator('#cardAttendance')
        style0 = await card.evaluate('el => el.getAttribute("style")')
        print("Initial style:", style0)
        
        # Hover
        await card.hover()
        await page.wait_for_timeout(200)
        style1 = await card.evaluate('el => el.getAttribute("style")')
        print("Hovered style:", style1)
        
        # Unhover
        await page.mouse.move(10, 10)
        await page.wait_for_timeout(200)
        style2 = await card.evaluate('el => el.getAttribute("style")')
        print("Unhovered style:", style2)
        
        # Switch to dark
        await page.evaluate("() => document.documentElement.setAttribute('data-theme', 'dark')")
        await page.wait_for_timeout(200)
        bg_dark = await card.evaluate('el => window.getComputedStyle(el).backgroundColor')
        style3 = await card.evaluate('el => el.getAttribute("style")')
        print("Dark BG:", bg_dark, "Style:", style3)
        
        # Hover in dark mode
        await card.hover()
        await page.wait_for_timeout(200)
        bg_dark_hover = await card.evaluate('el => window.getComputedStyle(el).backgroundColor')
        style_dark_hover = await card.evaluate('el => el.getAttribute("style")')
        print("Dark Hover BG:", bg_dark_hover, "Style:", style_dark_hover)
        
        await browser.close()

asyncio.run(test())

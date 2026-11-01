import asyncio
from playwright.async_api import async_playwright

async def verify():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        
        # 1. Desktop - English
        page = await browser.new_page(viewport={"width": 1440, "height": 900})
        await page.goto("http://127.0.0.1:3000/pages/shared/department.html?id=english", wait_until="networkidle")
        title_text = await page.text_content("#hubTitle")
        print(f"Desktop English Title: {title_text}")
        await page.screenshot(path="scratch/dept_title_english.png")
        await page.close()
        
        # 2. Desktop - Math
        page2 = await browser.new_page(viewport={"width": 1440, "height": 900})
        await page2.goto("http://127.0.0.1:3000/pages/shared/department.html?id=math", wait_until="networkidle")
        math_title = await page2.text_content("#hubTitle")
        print(f"Desktop Math Title: {math_title}")
        await page2.screenshot(path="scratch/dept_title_math.png")
        await page2.close()

        # 3. Mobile - 390px
        mobile_page = await browser.new_page(viewport={"width": 390, "height": 844})
        await mobile_page.goto("http://127.0.0.1:3000/pages/shared/department.html?id=english", wait_until="networkidle")
        await mobile_page.screenshot(path="scratch/dept_title_mobile.png")
        print("Mobile screenshot saved")
        await mobile_page.close()
        
        await browser.close()
        print("Verification complete!")

asyncio.run(verify())


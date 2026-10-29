import asyncio
from playwright.async_api import async_playwright

async def test_pages():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        
        for url_path in ["pages/admin/admin-users.html", "pages/admin/admin-students.html"]:
            page = await browser.new_page(viewport={"width": 1440, "height": 900})
            errors = []
            page.on("pageerror", lambda err: errors.append(str(err)))
            page.on("console", lambda msg: errors.append(msg.text) if msg.type == "error" else None)
            
            await page.goto(f"http://127.0.0.1:3000/{url_path}", wait_until="networkidle")
            
            # Check elements
            pills = await page.query_selector("#rolePillTabs")
            sub_role = await page.query_selector("#subRoleHeader")
            h2 = await page.query_selector("h2#directoryTitle, h2")
            h2_text = await h2.inner_text() if h2 else ""
            
            print(f"[{url_path}] rolePillTabs exists: {pills is not None}, subRoleHeader exists: {sub_role is not None}, H2: '{h2_text}'")
            print(f"[{url_path}] Console errors: {errors}")
            
            # Check responsive on mobile
            await page.set_viewport_size({"width": 390, "height": 844})
            btn = await page.query_selector(".hamburger-btn")
            btn_vis = await btn.is_visible() if btn else False
            sw = await page.evaluate("() => document.documentElement.scrollWidth")
            cw = await page.evaluate("() => document.documentElement.clientWidth")
            print(f"[{url_path} 390px] Hamburger visible: {btn_vis}, Overflow: {sw > cw}")
            
            await page.close()
            
        await browser.close()

asyncio.run(test_pages())

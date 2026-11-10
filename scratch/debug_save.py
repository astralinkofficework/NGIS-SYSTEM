import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1440, "height": 900})

        page.on("console", lambda msg: print(f"CONSOLE: {msg.type}: {msg.text}"))
        page.on("response", lambda res: print(f"RESPONSE: {res.status} {res.url}"))

        await page.goto("http://127.0.0.1:3000/pages/principal/principal-teacher-profiles.html")
        await page.wait_for_timeout(2000)

        first_edit = await page.query_selector('[data-act="edit-row"]')
        await first_edit.click()
        await page.wait_for_timeout(500)

        target_input = await page.query_selector('[id^="edTarget_"]')
        await target_input.fill("20")

        save_btn = await page.query_selector('[data-act="save-editor"]')
        await save_btn.click()
        await page.wait_for_timeout(2000)

        # Check toast
        toast = await page.query_selector("#ngisToast")
        if toast:
            print("Toast text:", await toast.inner_text(), "class:", await toast.get_attribute("class"))

        await browser.close()

asyncio.run(run())


import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1440, "height": 900})
        await page.goto("http://127.0.0.1:3000/pages/principal/principal-teacher-profiles.html")
        await page.wait_for_timeout(2000)

        first_card = await page.query_selector('.teacher-row-card')
        card_id = await first_card.get_attribute("data-id")
        print("card data-id:", repr(card_id))

        btn = await page.query_selector('[data-act="save-editor"]')
        btn_id = await btn.get_attribute("data-id")
        print("btn data-id:", repr(btn_id))

        name_input = await page.query_selector(f"#edName_{btn_id}")
        print("Found name input by id?", name_input is not None)
        if name_input:
            print("Name input value:", repr(await name_input.input_value()))

        dept_input = await page.query_selector(f"#edDept_{btn_id}")
        if dept_input:
            print("Dept input value:", repr(await dept_input.input_value()))

        subj_input = await page.query_selector(f"#edSubject_{btn_id}")
        if subj_input:
            print("Subj input value:", repr(await subj_input.input_value()))

        email_input = await page.query_selector(f"#edEmail_{btn_id}")
        if email_input:
            print("Email input value:", repr(await email_input.input_value()))

        await browser.close()

asyncio.run(run())


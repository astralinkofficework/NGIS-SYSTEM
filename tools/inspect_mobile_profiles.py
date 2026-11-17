import asyncio
from playwright.async_api import async_playwright

async def inspect():
    async with async_playwright() as p:
        # Test mobile viewport (iPhone 14 / Safari-like)
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            viewport={"width": 390, "height": 844},
            user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1"
        )
        page = await context.new_page()

        errors = []
        page.on("pageerror", lambda err: errors.append(f"PageError: {err}"))
        page.on("console", lambda msg: errors.append(f"Console {msg.type}: {msg.text}") if msg.type == "error" else None)

        print("Navigating to http://127.0.0.1:3000/pages/admin/admin-teacher-profiles.html ...")
        await page.goto("http://127.0.0.1:3000/pages/admin/admin-teacher-profiles.html", wait_until="networkidle")
        await page.wait_for_timeout(1000)

        # Check Add Teacher button text
        add_btn = await page.query_selector("#btnAddTeacher")
        if add_btn:
            btn_html = await add_btn.inner_html()
            btn_text = await add_btn.inner_text()
            print(f"Add Teacher text: '{btn_text}'")
            print(f"Add Teacher innerHTML: {btn_html}")

        # Check KPI cards layout & text
        kpis = await page.query_selector_all("#kpiGrid > div")
        print(f"Found {len(kpis)} KPI cards")
        for i, card in enumerate(kpis):
            text = (await card.inner_text()).replace('\n', ' | ')
            print(f"  KPI {i+1}: {text}")

        # Check mobile header and page title
        header_h1 = await page.query_selector("header.lg\\:hidden h1")
        if header_h1:
            h1_text = await header_h1.inner_text()
            is_vis = await header_h1.is_visible()
            print(f"Mobile header h1: '{h1_text}' (visible: {is_vis})")

        body_h1 = await page.query_selector("#profilesRoot h1")
        if body_h1:
            body_h1_text = await body_h1.inner_text()
            is_vis = await body_h1.is_visible()
            print(f"Body h1: '{body_h1_text}' (visible: {is_vis})")

        # Check search input & wrapper
        search_input = await page.query_selector("#dirSearch")
        if search_input:
            parent = await page.evaluate("el => el.parentElement.className", search_input)
            print(f"Search input parent classes: {parent}")

        # Check horizontal scroll / overflow
        scroll_width = await page.evaluate("() => document.documentElement.scrollWidth")
        client_width = await page.evaluate("() => document.documentElement.clientWidth")
        print(f"Viewport width: 390px | clientWidth: {client_width}px | scrollWidth: {scroll_width}px")

        print(f"\nErrors captured ({len(errors)}):")
        for err in errors:
            print("  ", err)

        await browser.close()

asyncio.run(inspect())

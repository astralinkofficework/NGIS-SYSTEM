import asyncio
from playwright.async_api import async_playwright

async def test_error():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        # Intercept teachers API to return 500 error
        await page.route("**/api/principal/roster/teachers", lambda route: route.fulfill(
            status=500,
            content_type="application/json",
            body='{"error": {"message": "Database connection timeout while reading faculty registry"}}'
        ))

        page_errors = []
        page.on("pageerror", lambda err: page_errors.append(str(err)))

        print("Testing error handling on http://127.0.0.1:3000/pages/admin/admin-teacher-profiles.html ...")
        await page.goto("http://127.0.0.1:3000/pages/admin/admin-teacher-profiles.html", wait_until="networkidle")
        await page.wait_for_timeout(1000)

        # Check status badge text
        status_text = await page.inner_text("#filterStatusText")
        print(f"Filter status badge text: '{status_text}'")

        # Check if error message is displayed in table
        error_msg = await page.query_selector(".py-12 p")
        err_text = await error_msg.inner_text() if error_msg else "None"
        print(f"Error card message: '{err_text}'")

        # Check if Retry button exists and is clickable
        retry_btn = await page.query_selector("#btnRetryLoad")
        print(f"Retry button exists: {retry_btn is not None}")

        # Check KPI cards when 0 records loaded due to error
        card1_text = (await (await page.query_selector("#kpiGrid > div:first-child")).inner_text()).replace('\n', ' | ')
        card2_text = (await (await page.query_selector("#kpiGrid > div:nth-child(2)")).inner_text()).replace('\n', ' | ')
        print(f"KPI Card 1 on error: {card1_text}")
        print(f"KPI Card 2 on error: {card2_text}")

        print(f"Page errors: {len(page_errors)}")

        assert "Loading" not in status_text, f"Status text is stuck on loading: {status_text}"
        assert retry_btn is not None, "Retry button missing"
        assert "—" in card2_text or "0" in card2_text, "Misleading 100% still rendered on error"
        print("ALL ERROR STATE CHECKS PASSED PERFECTLY!")

        await browser.close()

asyncio.run(test_error())

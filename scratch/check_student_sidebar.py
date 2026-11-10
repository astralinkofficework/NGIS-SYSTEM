import asyncio
from playwright.async_api import async_playwright

async def check():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={'width': 1280, 'height': 850})
        await page.goto('http://127.0.0.1:3000/pages/principal/principal.html')
        await page.wait_for_timeout(1000)

        sm_btn = page.locator(".nav-subgroup-label:has-text('Student Management')")
        print('Student Management button count:', await sm_btn.count())

        # Click to expand Student Management
        await sm_btn.click()
        await page.wait_for_timeout(300)

        # Check Academic Result button
        ar_btn = page.locator(".nav-nested-label:has-text('Academic Result')")
        print('Academic Result button count:', await ar_btn.count())

        # Click Academic Result to expand
        await ar_btn.click()
        await page.wait_for_timeout(300)

        # Check nested items
        nested = page.locator('.nav-nested-link')
        cnt = await nested.count()
        print('Nested items count under Academic Result:', cnt)
        for i in range(cnt):
            print('  ->', (await nested.nth(i).inner_text()).strip())

        # Check all direct sublinks under Student Management
        all_sub = page.locator(".nav-subgroup[data-subgroup-id='student-mgmt-drop'] .nav-sub-link, .nav-subgroup[data-subgroup-id='student-mgmt-drop'] .nav-nested-label")
        print('Total items in Student Management menu:', await all_sub.count())
        for i in range(await all_sub.count()):
            print('  [' + str(i+1) + ']', (await all_sub.nth(i).inner_text()).strip())

        await page.locator('#sidebar').screenshot(path='student_mgmt_sidebar_test.png')
        await browser.close()
        print('Screenshot saved!')

asyncio.run(check())


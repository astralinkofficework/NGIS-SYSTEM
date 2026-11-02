import asyncio
from playwright.async_api import async_playwright

async def run_checks():
    console_errors = []

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        page.on('console', lambda msg: console_errors.append(f"Console {msg.type}: {msg.text}") if msg.type == 'error' else None)

        print("Testing Principal Dashboard (Desktop)...")
        await page.set_viewport_size({'width': 1440, 'height': 900})
        await page.goto('http://127.0.0.1:3000/pages/principal/principal.html', wait_until='domcontentloaded')
        await page.wait_for_timeout(1500)
        await page.screenshot(path='scratch/principal_desktop.png')

        print("Testing Principal Dashboard (Tablet)...")
        await page.set_viewport_size({'width': 820, 'height': 1180})
        await page.goto('http://127.0.0.1:3000/pages/principal/principal.html', wait_until='domcontentloaded')
        await page.wait_for_timeout(1000)
        await page.screenshot(path='scratch/principal_tablet.png')

        print("Testing Principal Dashboard (Mobile)...")
        await page.set_viewport_size({'width': 390, 'height': 844})
        await page.goto('http://127.0.0.1:3000/pages/principal/principal.html', wait_until='domcontentloaded')
        await page.wait_for_timeout(1000)
        await page.screenshot(path='scratch/principal_mobile.png')

        # Check mobile hamburger button
        btn = await page.query_selector('[data-action="toggle-sidebar"]')
        btn_visible = await btn.is_visible() if btn else False
        print(f"Mobile hamburger button visible: {btn_visible}")

        print("\nTesting Principal Approvals Console (Desktop)...")
        await page.set_viewport_size({'width': 1440, 'height': 900})
        await page.goto('http://127.0.0.1:3000/pages/principal/principal-approvals.html', wait_until='domcontentloaded')
        await page.wait_for_timeout(1500)
        await page.screenshot(path='scratch/principal_approvals_desktop.png')

        print("Testing Principal Approvals Console (Mobile)...")
        await page.set_viewport_size({'width': 390, 'height': 844})
        await page.goto('http://127.0.0.1:3000/pages/principal/principal-approvals.html', wait_until='domcontentloaded')
        await page.wait_for_timeout(1000)
        await page.screenshot(path='scratch/principal_approvals_mobile.png')

        appr_btn = await page.query_selector('[data-action="toggle-sidebar"]')
        appr_btn_visible = await appr_btn.is_visible() if appr_btn else False
        print(f"Approvals mobile hamburger button visible: {appr_btn_visible}")

        await browser.close()

    print("\nConsole errors encountered:", len(console_errors))
    for err in console_errors:
        print("  ", err)

if __name__ == '__main__':
    asyncio.run(run_checks())

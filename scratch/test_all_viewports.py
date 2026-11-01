import asyncio
from playwright.async_api import async_playwright

viewports = [
    {"name": "desktop_1440", "width": 1440, "height": 900},
    {"name": "laptop_1280", "width": 1280, "height": 800},
    {"name": "small_laptop_1024", "width": 1024, "height": 768},
    {"name": "tablet_820", "width": 820, "height": 1180},
    {"name": "mobile_390", "width": 390, "height": 844}
]

async def test_all():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        errors = []
        
        for vp in viewports:
            page = await browser.new_page(viewport={"width": vp["width"], "height": vp["height"]})
            page.on("pageerror", lambda err: errors.append(f"[{vp['name']}] Page error: {err}"))
            page.on("console", lambda msg: errors.append(f"[{vp['name']}] Console error: {msg.text}") if msg.type == "error" else None)
            
            await page.goto("http://127.0.0.1:3000/pages/student/student.html", wait_until="domcontentloaded")
            await page.wait_for_timeout(500)
            
            await page.screenshot(path=f"scratch/live_{vp['name']}.png")
            print(f"Verified {vp['name']} (width: {vp['width']}, height: {vp['height']})")
            await page.close()
            
        await browser.close()
        
        if errors:
            print(f"Errors found ({len(errors)}):")
            for e in errors:
                print("  ", e)
        else:
            print("All viewports passed with 0 errors!")

asyncio.run(test_all())

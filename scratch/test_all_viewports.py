import asyncio
from playwright.async_api import async_playwright

VIEWPORTS = [
    {"name": "320_small_mobile", "width": 320, "height": 650},
    {"name": "375_iphone_se", "width": 375, "height": 667},
    {"name": "390_iphone_14", "width": 390, "height": 844},
    {"name": "430_iphone_promax", "width": 430, "height": 932},
    {"name": "768_tablet_portrait", "width": 768, "height": 1024},
    {"name": "1024_tablet_landscape", "width": 1024, "height": 768},
    {"name": "1268_user_screen", "width": 1268, "height": 706},
    {"name": "1366_laptop", "width": 1366, "height": 768},
    {"name": "1920_desktop_fhd", "width": 1920, "height": 1080},
    {"name": "844_landscape_phone", "width": 844, "height": 390},
]

async def run_all():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        all_passed = True
        
        for vp in VIEWPORTS:
            page = await browser.new_page(viewport={"width": vp["width"], "height": vp["height"]})
            await page.goto("http://localhost:3000/pages/student/student.html")
            await page.wait_for_timeout(800)
            
            overflow = await page.evaluate('''() => {
                const docWidth = document.documentElement.scrollWidth;
                const winWidth = window.innerWidth;
                return docWidth > winWidth;
            }''')
            
            status = "FAIL (Overflow)" if overflow else "PASS"
            if overflow:
                all_passed = False
            print(f"Viewport {vp['name']} ({vp['width']}x{vp['height']}): {status}")
            await page.close()
            
        await browser.close()
        print("\nAll viewports passed zero-overflow test:", all_passed)

asyncio.run(run_all())

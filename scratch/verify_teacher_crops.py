import asyncio
from playwright.async_api import async_playwright
from PIL import Image

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        
        # 1. Desktop verification
        page = await browser.new_page(viewport={'width': 1440, 'height': 900})
        await page.goto('http://127.0.0.1:3000/pages/teacher/teacher.html', wait_until='networkidle')
        await page.wait_for_timeout(1000)
        await page.screenshot(path='scratch/teacher_desktop_full.png', full_page=True)
        print('Saved scratch/teacher_desktop_full.png')
        
        # 2. Mobile verification with hamburger click
        page_mobile = await browser.new_page(viewport={'width': 390, 'height': 844})
        await page_mobile.goto('http://127.0.0.1:3000/pages/teacher/teacher.html', wait_until='networkidle')
        await page_mobile.wait_for_timeout(1000)
        
        # Click mobile hamburger in mobile view
        hamb = await page_mobile.query_selector('.teacher-mobile-view button[data-action="toggle-sidebar"]')
        if hamb:
            print('Found mobile hamburger button, clicking...')
            await hamb.click()
            await page_mobile.wait_for_timeout(600)
            await page_mobile.screenshot(path='scratch/teacher_mobile_drawer_open.png')
            print('Saved scratch/teacher_mobile_drawer_open.png')
            
        await browser.close()

    # Crop sections of desktop screenshot for visual inspection
    im = Image.open('scratch/teacher_desktop_full.png')
    
    # Hero & Topbar (top 0-350)
    crop_hero = im.crop((0, 0, 1440, 360))
    crop_hero.save('scratch/teacher_crop_hero.png')
    
    # Overlap Cards (y: 200 to 750)
    crop_overlap = im.crop((280, 200, 1420, 780))
    crop_overlap.save('scratch/teacher_crop_overlap.png')
    
    # Lower Dashboard (y: 750 to 1400)
    crop_lower = im.crop((280, 750, 1420, 1450))
    crop_lower.save('scratch/teacher_crop_lower.png')
    
    print('All crops generated successfully!')

asyncio.run(main())


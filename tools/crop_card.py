import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={'width': 1280, 'height': 850})
        await page.goto('http://127.0.0.1:3000/pages/student/student-exams.html', wait_until='networkidle')
        await page.wait_for_timeout(1000)
        
        card = await page.query_selector('.exw-roadmap-card')
        if card:
            await card.screenshot(path=r'C:/Users/oudom/.gemini/antigravity/brain/f0e0db56-cd04-4f51-a7f8-40ba21b43536/roadmap_card_crop.png')
            print("Card cropped and saved to roadmap_card_crop.png")
        else:
            print("Card not found!")
        await browser.close()

if __name__ == '__main__':
    asyncio.run(run())

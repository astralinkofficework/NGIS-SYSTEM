import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={'width': 1280, 'height': 900})
        
        # 1. Load page
        await page.goto('http://127.0.0.1:3000/pages/student/student-exams.html', wait_until='networkidle')
        await page.wait_for_timeout(500)
        
        # 2. Check font weights in roadmap card
        weights = await page.evaluate("""() => {
            const card = document.querySelector('.exw-roadmap-card');
            if (!card) return [];
            const els = card.querySelectorAll('*');
            const heavy = [];
            els.forEach(el => {
                const w = parseInt(window.getComputedStyle(el).fontWeight, 10);
                if (w > 500) {
                    heavy.push({ tag: el.tagName, text: el.innerText.slice(0, 30), weight: w, class: el.className });
                }
            });
            return heavy;
        }""")
        print(f"Elements with fontWeight > 500: {len(weights)}")
        if weights:
            for w in weights:
                print("  Heavy element:", w)
        assert len(weights) == 0, f"Found {len(weights)} elements with weight > 500"
        
        # 3. Test Live Search Filtering
        search_input = page.locator('#roadmapFilter')
        await search_input.fill('Math')
        await page.wait_for_timeout(300)
        
        count_after_math = await page.evaluate("() => document.getElementById('roadmapQueuedCount').innerText")
        cards_after_math = await page.evaluate("() => document.querySelectorAll('.exw-timeline-item').length")
        print(f"After typing 'Math': badge count = {count_after_math}, visible items = {cards_after_math}")
        assert count_after_math == '1', f"Expected '1' queued, got {count_after_math}"
        assert cards_after_math == 1, f"Expected 1 card, got {cards_after_math}"
        
        # Clear search
        await search_input.fill('')
        await page.wait_for_timeout(300)
        count_restored = await page.evaluate("() => document.getElementById('roadmapQueuedCount').innerText")
        cards_restored = await page.evaluate("() => document.querySelectorAll('.exw-timeline-item').length")
        print(f"After clearing search: badge count = {count_restored}, visible items = {cards_restored}")
        assert count_restored == '5', f"Expected '5' queued, got {count_restored}"
        assert cards_restored == 5, f"Expected 5 cards, got {cards_restored}"
        
        # 4. Test Modal Click
        first_card = page.locator('.exw-timeline-card').first
        await first_card.click()
        await page.wait_for_timeout(500)
        
        modal_visible = await page.evaluate("() => { const m = document.querySelector('.exw-modal-scrim'); return m !== null; }")
        modal_title = await page.evaluate("() => document.querySelector('.exw-modal-title')?.innerText")
        print(f"Modal visible on click: {modal_visible}, Modal title: {modal_title}")
        assert modal_visible, "Modal should be visible when clicking examination card"
        
        # Close modal
        close_btn = page.locator('.exw-modal-close, [data-action="close-modal"]').first
        if await close_btn.count() > 0:
            await close_btn.click()
            await page.wait_for_timeout(300)
        
        # 5. Take Desktop Screenshot (Full Card)
        card_el = await page.query_selector('.exw-roadmap-card')
        if card_el:
            await card_el.screenshot(path=r'C:/Users/oudom/.gemini/antigravity/brain/f0e0db56-cd04-4f51-a7f8-40ba21b43536/student_roadmap_desktop.png')
            print("Desktop screenshot saved to student_roadmap_desktop.png")
            
        # 6. Test Mobile Viewport (375x667)
        await page.set_viewport_size({'width': 375, 'height': 667})
        await page.wait_for_timeout(500)
        hamburger_visible = await page.evaluate("""() => {
            const btns = Array.from(document.querySelectorAll('[data-action="toggle-sidebar"], .mobile-hamburger-btn'));
            return btns.some(b => {
                const r = b.getBoundingClientRect();
                return r.width > 0 && r.height > 0 && window.getComputedStyle(b).display !== 'none' && window.getComputedStyle(b).visibility !== 'hidden';
            });
        }""")
        print(f"Mobile (375px) hamburger button visible: {hamburger_visible}")
        assert hamburger_visible, "Hamburger button must be visible on mobile"
        
        mobile_card = await page.query_selector('.exw-roadmap-card')
        if mobile_card:
            await mobile_card.screenshot(path=r'C:/Users/oudom/.gemini/antigravity/brain/f0e0db56-cd04-4f51-a7f8-40ba21b43536/student_roadmap_mobile.png')
            print("Mobile screenshot saved to student_roadmap_mobile.png")
            
        # 7. Test Dark Mode
        await page.set_viewport_size({'width': 1280, 'height': 900})
        await page.evaluate("() => document.documentElement.setAttribute('data-theme', 'dark')")
        await page.wait_for_timeout(400)
        if card_el:
            await card_el.screenshot(path=r'C:/Users/oudom/.gemini/antigravity/brain/f0e0db56-cd04-4f51-a7f8-40ba21b43536/student_roadmap_dark.png')
            print("Dark mode screenshot saved to student_roadmap_dark.png")
            
        print("\nALL VERIFICATION CHECKS PASSED PERFECTLY!")
        await browser.close()

if __name__ == '__main__':
    asyncio.run(run())

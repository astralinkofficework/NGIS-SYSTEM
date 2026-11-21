import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={'width': 1280, 'height': 850})
        
        errors = []
        page.on('console', lambda msg: print(f'Console [{msg.type}]: {msg.text}') if msg.type == 'error' else None)
        page.on('pageerror', lambda exc: errors.append(str(exc)))
        
        await page.goto('http://127.0.0.1:3000/pages/student/student-exams.html', wait_until='networkidle')
        await page.wait_for_timeout(1000)
        
        title = await page.evaluate("() => document.getElementById('roadmapTitle') ? document.getElementById('roadmapTitle').innerText : 'NOT FOUND'")
        badge = await page.evaluate("() => document.getElementById('roadmapQueuedBadge') ? document.getElementById('roadmapQueuedBadge').innerText : 'NOT FOUND'")
        items = await page.evaluate("""() => {
            const cards = Array.from(document.querySelectorAll('.exw-timeline-item'));
            return cards.map(c => {
                const node = c.querySelector('.exw-timeline-node')?.innerText;
                const time = c.querySelector('.exw-pill-time')?.innerText;
                const room = c.querySelector('.exw-pill-room')?.innerText;
                const format = c.querySelector('.exw-card-format')?.innerText;
                const title = c.querySelector('.exw-card-title')?.innerText;
                const desc = c.querySelector('.exw-card-desc')?.innerText;
                const action = c.querySelector('.exw-card-action')?.innerText;
                return { node, time, room, format, title, desc, action };
            });
        }""")
        
        print("Roadmap Title:", title)
        print("Roadmap Badge:", badge)
        print(f"Total timeline items: {len(items)}")
        for idx, it in enumerate(items):
            print(f"  [{idx+1}] Node: {it['node']} | Pill: {it['time']} | Room: {it['room']} | Format: {it['format']}")
            print(f"      Title: {it['title']} | Action: {it['action']}")
            print(f"      Desc: {it['desc']}")
        
        await page.screenshot(path=r'C:/Users/oudom/.gemini/antigravity/brain/f0e0db56-cd04-4f51-a7f8-40ba21b43536/student_roadmap_view.png')
        print("Screenshot saved to student_roadmap_view.png")
        await browser.close()

if __name__ == '__main__':
    asyncio.run(run())

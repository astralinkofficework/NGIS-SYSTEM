import os
from playwright.sync_api import sync_playwright

ARTIFACT_DIR = r"C:\Users\oudom\.gemini\antigravity\brain\f0e0db56-cd04-4f51-a7f8-40ba21b43536"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    
    print("Navigating to student.html...")
    page.goto("http://127.0.0.1:3000/pages/student/student.html", wait_until="networkidle")
    page.wait_for_timeout(1000)

    # Verify announcement rows
    news_items = page.evaluate("""() => {
        const rows = Array.from(document.querySelectorAll('.workspace-news-row'));
        return rows.map(r => {
            const img = r.querySelector('img.workspace-news-thumb');
            const title = r.querySelector('.workspace-news-title');
            const snippet = r.querySelector('.workspace-news-snippet');
            const cat = r.querySelector('.workspace-news-cat');
            return {
                title: title ? title.innerText : '',
                snippet: snippet ? snippet.innerText : '',
                cat: cat ? cat.innerText : '',
                imgSrc: img ? img.src : '',
                imgNaturalWidth: img ? img.naturalWidth : 0
            };
        });
    }""")

    print(f"Rendered {len(news_items)} news items in Announcements card:")
    for item in news_items:
        print(f"  - [{item['cat']}] {item['title']}")
        print(f"    Snippet: {item['snippet'][:60]}...")
        print(f"    Image: {item['imgSrc']} (naturalWidth: {item['imgNaturalWidth']})")
        if item['imgNaturalWidth'] == 0:
            print("    [ERROR] Image failed to load!")

    # Close-up screenshot of Announcements card
    ann_card = page.query_selector(".workspace-card:has(#announcementsList)")
    if ann_card:
        crop_path = os.path.join(ARTIFACT_DIR, "announcements_news_card_closeup.png")
        ann_card.screenshot(path=crop_path)
        print(f"Saved closeup screenshot to {crop_path}")

    # Full desktop screenshot
    desktop_shot = os.path.join(ARTIFACT_DIR, "student_workspace_news_desktop.png")
    page.screenshot(path=desktop_shot)
    print(f"Saved desktop screenshot to {desktop_shot}")

    # Modal test: click first news item
    print("Clicking first news item...")
    first_news = page.query_selector('.workspace-news-row')
    if first_news:
        first_news.click()
        page.wait_for_timeout(600)
        modal_shot = os.path.join(ARTIFACT_DIR, "announcement_news_modal_open.png")
        page.screenshot(path=modal_shot)
        print(f"Saved modal screenshot to {modal_shot}")
        modal_close = page.query_selector("#wsModalCloseBtn")
        if modal_close:
            modal_close.click()
            page.wait_for_timeout(300)

    # Mobile test (390x844)
    mobile_page = browser.new_page(viewport={"width": 390, "height": 844}, device_scale_factor=2)
    mobile_page.goto("http://127.0.0.1:3000/pages/student/student.html", wait_until="networkidle")
    mobile_page.wait_for_timeout(1000)
    mobile_ann_card = mobile_page.query_selector(".workspace-card:has(#announcementsList)")
    if mobile_ann_card:
        mobile_crop_path = os.path.join(ARTIFACT_DIR, "announcements_news_card_mobile.png")
        mobile_ann_card.screenshot(path=mobile_crop_path)
        print(f"Saved mobile card screenshot to {mobile_crop_path}")
    mobile_page.close()

    browser.close()
    print("Playwright tests completed successfully!")

from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    page.goto("http://127.0.0.1:3000/pages/principal/principal-timetable-builder.html", wait_until="networkidle")
    
    # Click 7B cohort pill
    page.click('button[data-act="set-class-cohort"][data-id="class_7B"]')
    page.wait_for_timeout(500)
    
    # Click Auto-Schedule All button
    auto_btn = page.query_selector('button[data-act="fill-class"][data-id="class_7B"]')
    if auto_btn:
        print("Clicking Auto-Schedule All for 7B...")
        auto_btn.click()
        page.wait_for_timeout(1500)
    
    # Inspect all placed cells
    cells = page.evaluate('''() => {
        const btns = document.querySelectorAll('button[data-drag-placed]');
        return Array.from(btns).map(b => ({
            key: b.getAttribute('data-drag-placed'),
            text: b.innerText.replace(/\\n/g, ' '),
            styleBg: b.style.backgroundColor,
            computedBg: window.getComputedStyle(b).backgroundColor,
            title: b.title
        }));
    }''')
    print("Placed cells on 7B count:", len(cells))
    for i, c in enumerate(cells):
        print(f"{i+1:2d}. {c['text']:25s} | bg: {c['styleBg']:24s} | key: {c['key']}")
    page.screenshot(path="scratch/test_7b_colors.png")
    browser.close()

from playwright.sync_api import sync_playwright

url = "http://127.0.0.1:3000/pages/admin/admin-security.html"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto(url, wait_until="networkidle")
    page.wait_for_timeout(300)
    
    bolds = page.evaluate("""() => {
        const topbar = document.querySelector('.hero-topbar');
        if (!topbar) return [];
        const all = topbar.querySelectorAll('*');
        const heavy = [];
        all.forEach(el => {
            const fw = parseInt(window.getComputedStyle(el).fontWeight, 10);
            if (fw > 500) {
                heavy.push({
                    tag: el.tagName,
                    className: el.className,
                    text: (el.innerText || el.textContent || '').slice(0, 30),
                    fontWeight: fw
                });
            }
        });
        return heavy;
    }""")
    print(f"Elements with fontWeight > 500 in topbar: {len(bolds)}")
    for b in bolds:
        print("  Heavy:", b)
    browser.close()

from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={'width': 375, 'height': 812})
    page.goto('http://127.0.0.1:3000/pages/principal/principal-services.html')
    page.wait_for_timeout(600)
    
    # Check if there is horizontal overflow in window or body
    overflow = page.evaluate("""() => {
        const bodyWidth = document.body.scrollWidth;
        const windowWidth = window.innerWidth;
        const docWidth = document.documentElement.scrollWidth;
        const overflowingEls = Array.from(document.querySelectorAll('*')).filter(el => {
            return el.scrollWidth > windowWidth + 5 && el.tagName !== 'HTML' && el.tagName !== 'BODY';
        }).map(el => ({
            tag: el.tagName,
            cls: el.className,
            id: el.id,
            scrollWidth: el.scrollWidth,
            clientWidth: el.clientWidth
        }));
        return {
            bodyWidth,
            windowWidth,
            docWidth,
            hasWindowOverflow: docWidth > windowWidth,
            overflowingEls: overflowingEls.slice(0, 10)
        };
    }""")
    print("Overflow analysis for 375px mobile:", overflow)
    browser.close()


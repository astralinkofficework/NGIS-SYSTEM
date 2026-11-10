from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    page.on("console", lambda msg: print(f"CONSOLE [{msg.type}]: {msg.text}"))
    page.goto("http://127.0.0.1:3000/pages-directory.html", wait_until="networkidle")

    info = page.evaluate("""() => {
        const btn = document.getElementById('viewTableBtn');
        return {
            btnExists: !!btn,
            btnOuter: btn.outerHTML,
            pagesLength: (window.NGIS_PAGES || []).length
        };
    }""")
    print("Pre-click info:", info)

    page.click("#viewTableBtn")
    page.wait_for_timeout(500)

    post_info = page.evaluate("""() => {
        return {
            gridDisplay: document.getElementById('pagesGrid').style.display,
            tableDisplay: document.getElementById('pagesTableWrap').style.display,
            tbodyHtml: document.getElementById('pagesTableBody').innerHTML.slice(0, 300)
        };
    }""")
    print("Post-click info:", post_info)

    browser.close()


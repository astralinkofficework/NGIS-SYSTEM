from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    page.on("console", lambda msg: print(f"CONSOLE [{msg.type}]: {msg.text}"))
    page.on("pageerror", lambda err: print(f"PAGE ERROR: {err}"))

    page.goto("http://127.0.0.1:3000/pages-directory.html", wait_until="load")
    page.wait_for_timeout(1000)

    res = page.evaluate("""() => {
        return {
            hasPAGES: typeof PAGES !== 'undefined' ? PAGES.length : 'no',
            viewTableBtn: !!document.getElementById('viewTableBtn'),
            viewGridBtn: !!document.getElementById('viewGridBtn'),
            state: typeof state !== 'undefined' ? state : 'no'
        };
    }""")
    print("Page state:", res)

    browser.close()


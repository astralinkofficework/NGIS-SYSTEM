from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={'width': 1440, 'height': 900})
    logs = []
    page.on('console', lambda msg: logs.append(f"[{msg.type}] {msg.text}"))
    page.on('pageerror', lambda err: logs.append(f"[ERROR] {err}"))
    page.goto('http://127.0.0.1:3000/pages/principal/principal-teacher-class-assignment.html')
    page.wait_for_load_state('networkidle')
    for l in logs:
        print(l)
    
    # check heroBanner
    res = page.evaluate("""() => {
        const el = document.getElementById('heroBanner');
        return {
            exists: !!el,
            innerHTML: el ? el.innerHTML.slice(0, 200) : null,
            heroConfig: window.HERO_CONFIG
        };
    }""")
    print('res:', res)
    browser.close()


from playwright.sync_api import sync_playwright

urls = [
    "http://127.0.0.1:3000/pages/principal/principal-teacher-class-assignment.html",
    "http://127.0.0.1:3000/pages/principal/principal-timetable-builder.html",
    "http://127.0.0.1:3000/pages/principal/principal-timetables.html",
    "http://127.0.0.1:3000/pages/principal/principal-subjects.html",
    "http://127.0.0.1:3000/pages/principal/principal-records.html"
]

with sync_playwright() as p:
    browser = p.chromium.launch()
    for u in urls:
        print(f"\n--- Testing: {u} ---")
        page = browser.new_page()
        errors = []
        logs = []
        page.on("pageerror", lambda err: errors.append(str(err)))
        page.on("console", lambda msg: logs.append(f"[{msg.type}] {msg.text}"))
        
        try:
            resp = page.goto(u, wait_until="load", timeout=10000)
            page.wait_for_timeout(1000)
            root_html = page.evaluate("() => document.getElementById('ks-root') ? document.getElementById('ks-root').innerHTML.substring(0, 200) : 'NO_KS_ROOT'")
            url_after = page.url
            print(f"Status: {resp.status}, Final URL: {url_after}")
            print(f"ks-root content: {root_html[:100]}...")
        except Exception as e:
            print(f"FAILED TO LOAD: {e}")
            
        if errors:
            print("PAGE ERRORS:")
            for err in errors:
                print("  ", err)
        else:
            print("No JavaScript errors.")
            
        page.close()
    browser.close()


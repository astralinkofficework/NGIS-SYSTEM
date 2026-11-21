from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    
    for url in [
        "http://127.0.0.1:3000/pages/principal/principal.html",
        "http://127.0.0.1:3000/pages/principal/principal-attendance.html",
        "http://127.0.0.1:3000/pages/teacher/teacher.html",
        "http://127.0.0.1:3000/pages/student/student.html",
        "http://127.0.0.1:3000/pages/admin/admin.html"
    ]:
        print(f"\n==================== {url} ====================")
        page = browser.new_page(viewport={"width": 1440, "height": 900})
        page.goto(url)
        page.wait_for_timeout(600)
        
        info = page.evaluate("""() => {
            // Find all visible elements whose top is between -10 and 200
            const all = Array.from(document.querySelectorAll('*'));
            const elementsAtTop = [];
            
            for (const el of all) {
                if (el.tagName === 'HTML' || el.tagName === 'BODY' || el.tagName === 'SCRIPT' || el.tagName === 'STYLE') continue;
                const r = el.getBoundingClientRect();
                if (r.width > 50 && r.height > 10 && r.top >= -5 && r.top <= 150) {
                    elementsAtTop.push({
                        tag: el.tagName,
                        id: el.id,
                        className: (el.className || '').toString().slice(0, 50),
                        top: Math.round(r.top),
                        bottom: Math.round(r.bottom),
                        left: Math.round(r.left),
                        width: Math.round(r.width),
                        height: Math.round(r.height),
                        display: window.getComputedStyle(el).display,
                        position: window.getComputedStyle(el).position
                    });
                }
            }
            return elementsAtTop.slice(0, 15);
        }""")
        
        for item in info:
            print(f"  {item['tag']:<10} id={item['id']:<20} top={item['top']:<4} h={item['height']:<4} l={item['left']:<4} w={item['width']:<5} pos={item['position']:<8} class={item['className']}")
            
        page.close()
    browser.close()

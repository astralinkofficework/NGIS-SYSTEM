from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={'width': 1280, 'height': 900})
    page.goto('http://127.0.0.1:3000/pages/principal/principal-timetable-builder.html', wait_until='networkidle')
    page.wait_for_timeout(1000)
    
    css = """
        .ks-timetable-grid td { padding: 0 !important; vertical-align: middle !important; }
        .ks-timetable-grid th { padding: 10px 8px !important; }
        .ks-timetable-grid td.time-col { padding: 8px 4px !important; }
    """
    page.evaluate('''([css]) => {
        const s = document.createElement("style");
        s.textContent = css;
        document.head.appendChild(s);
        document.querySelector("table").classList.add("ks-timetable-grid");
    }''', [css])
    
    info = page.evaluate('''() => {
        const btn = document.querySelector('button[data-drag-placed]');
        const td = btn.parentElement;
        const btnRect = btn.getBoundingClientRect();
        const tdRect = td.getBoundingClientRect();
        return {
            btnRect: { w: btnRect.width, h: btnRect.height },
            tdRect: { w: tdRect.width, h: tdRect.height }
        };
    }''')
    print('With override:', info)
    page.query_selector('table').screenshot(path='scratch/test_flush_box.png')
    browser.close()


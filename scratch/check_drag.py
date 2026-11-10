from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={'width': 1280, 'height': 900})
    page.goto('http://127.0.0.1:3000/pages/principal/principal-timetable-builder.html', wait_until='networkidle')
    page.wait_for_timeout(1000)
    
    drag_res = page.evaluate("""() => {
        const chips = document.querySelectorAll('[data-drag-chip]');
        const cells = document.querySelectorAll('[data-act="cell"]');
        const placed = document.querySelectorAll('[data-drag-placed]');
        return {
            chipsCount: chips.length,
            cellsCount: cells.length,
            placedCount: placed.length,
            placedDraggable: Array.from(placed).map(p => p.getAttribute('draggable'))
        };
    }""")
    print('Drag elements:', drag_res)
    browser.close()


from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={'width': 1280, 'height': 900})
    page.goto('http://127.0.0.1:3000/pages/principal/principal-timetable-builder.html', wait_until='networkidle')
    page.wait_for_timeout(1000)
    
    # 1. Test dragging chip onto empty cell
    chip = page.query_selector('[data-drag-chip]')
    empty_cell = page.query_selector('button[data-act="cell"]:not([data-drag-placed])')
    print('Chip found:', chip is not None, 'Empty cell found:', empty_cell is not None)
    
    if chip and empty_cell:
        chip_box = chip.bounding_box()
        empty_box = empty_cell.bounding_box()
        print('Chip box:', chip_box)
        print('Empty cell box:', empty_box)
        
        # Drag chip to empty cell
        page.mouse.move(chip_box['x'] + chip_box['width']/2, chip_box['y'] + chip_box['height']/2)
        page.mouse.down()
        page.mouse.move(empty_box['x'] + empty_box['width']/2, empty_box['y'] + empty_box['height']/2, steps=10)
        page.mouse.up()
        page.wait_for_timeout(1000)
        
        placed_after = page.evaluate('() => document.querySelectorAll("[data-drag-placed]").length')
        print('Placed cells after chip drag:', placed_after)
        
    # 2. Test dragging placed cell to another cell
    placed_cells = page.query_selector_all('[data-drag-placed]')
    if len(placed_cells) >= 1 and empty_cell:
        src = placed_cells[0]
        src_box = src.bounding_box()
        dst_box = empty_cell.bounding_box()
        page.mouse.move(src_box['x'] + src_box['width']/2, src_box['y'] + src_box['height']/2)
        page.mouse.down()
        page.mouse.move(dst_box['x'] + dst_box['width']/2, dst_box['y'] + dst_box['height']/2, steps=10)
        page.mouse.up()
        page.wait_for_timeout(1000)
        
        placed_after_swap = page.evaluate('() => document.querySelectorAll("[data-drag-placed]").length')
        print('Placed cells after placed-cell drag:', placed_after_swap)
        
    browser.close()


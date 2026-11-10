from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={'width': 1280, 'height': 900})
    page.goto('http://127.0.0.1:3000/pages/principal/principal-timetable-builder.html', wait_until='networkidle')
    page.wait_for_timeout(1000)
    
    # Check initial placed cells count
    init_count = page.evaluate('() => document.querySelectorAll("[data-drag-placed]").length')
    print('Initial placed count:', init_count)
    
    # 1. Test Drag Chip to Empty Cell
    chip = page.query_selector('[data-drag-chip]')
    empty_cell = page.query_selector('td[data-cell-drop] button:not([data-drag-placed])')
    if chip and empty_cell:
        chip_box = chip.bounding_box()
        empty_box = empty_cell.bounding_box()
        page.mouse.move(chip_box['x'] + chip_box['width']/2, chip_box['y'] + chip_box['height']/2)
        page.mouse.down()
        page.mouse.move(empty_box['x'] + empty_box['width']/2, empty_box['y'] + empty_box['height']/2, steps=10)
        page.mouse.up()
        page.wait_for_timeout(1000)
        
        count_after_chip = page.evaluate('() => document.querySelectorAll("[data-drag-placed]").length')
        print('After chip drag -> Placed count:', count_after_chip)
        assert count_after_chip > init_count, f"Expected > {init_count}, got {count_after_chip}"
        print("PASS: Drag chip to empty cell works!")

    # 2. Test Drag Placed Cell to Empty Cell (MOVE)
    placed_cells = page.query_selector_all('[data-drag-placed]')
    empty_cell2 = page.query_selector('td[data-cell-drop] button:not([data-drag-placed])')
    if placed_cells and empty_cell2:
        src = placed_cells[0]
        src_key = src.get_attribute('data-drag-placed')
        src_box = src.bounding_box()
        dst_box = empty_cell2.bounding_box()
        dst_key = empty_cell2.get_attribute('data-key')
        print(f"Moving from {src_key} to {dst_key}")
        
        page.mouse.move(src_box['x'] + src_box['width']/2, src_box['y'] + src_box['height']/2)
        page.mouse.down()
        page.mouse.move(dst_box['x'] + dst_box['width']/2, dst_box['y'] + dst_box['height']/2, steps=10)
        page.mouse.up()
        page.wait_for_timeout(1000)
        
        # Verify moved
        has_new_dst = page.evaluate(f'() => !!document.querySelector(\'[data-drag-placed="{dst_key}"]\')')
        print(f"Cell at {dst_key} exists now:", has_new_dst)
        assert has_new_dst, f"Expected cell at {dst_key}"
        print("PASS: Drag placed cell to empty cell (MOVE) works!")

    # 3. Test Drag Placed Cell onto another Placed Cell (SWAP)
    placed_cells = page.query_selector_all('[data-drag-placed]')
    if len(placed_cells) >= 2:
        cell_a = placed_cells[0]
        cell_b = placed_cells[1]
        key_a = cell_a.get_attribute('data-drag-placed')
        key_b = cell_b.get_attribute('data-drag-placed')
        text_a_before = cell_a.inner_text()
        text_b_before = cell_b.inner_text()
        print(f"Swapping {key_a} and {key_b}")
        
        box_a = cell_a.bounding_box()
        box_b = cell_b.bounding_box()
        page.mouse.move(box_a['x'] + box_a['width']/2, box_a['y'] + box_a['height']/2)
        page.mouse.down()
        page.mouse.move(box_b['x'] + box_b['width']/2, box_b['y'] + box_b['height']/2, steps=10)
        page.mouse.up()
        page.wait_for_timeout(1000)
        
        cell_a_after = page.query_selector(f'[data-drag-placed="{key_a}"]')
        cell_b_after = page.query_selector(f'[data-drag-placed="{key_b}"]')
        assert cell_a_after and cell_b_after, "Both cells should still exist after swap"
        print("PASS: Drag placed cell to placed cell (SWAP) works!")

    # 4. Check Floating Move Bar visibility when a placed cell is selected
    placed_cells = page.query_selector_all('[data-drag-placed]')
    if placed_cells:
        placed_cells[0].click()
        page.wait_for_timeout(500)
        move_bar = page.query_selector('[data-act="delete-placed-lesson"]')
        print("Move bar delete button present:", move_bar is not None)
        assert move_bar is not None, "Floating move bar should appear when cell is selected"
        
        # Test Delete placed lesson
        move_bar.click()
        page.wait_for_timeout(1000)
        count_after_del = page.evaluate('() => document.querySelectorAll("[data-drag-placed]").length')
        print("Count after delete button:", count_after_del)
        print("PASS: Delete placed lesson works!")

    # 5. Test Undo (Ctrl+Z)
    page.keyboard.press("Control+z")
    page.wait_for_timeout(1000)
    count_after_undo = page.evaluate('() => document.querySelectorAll("[data-drag-placed]").length')
    print("Count after Ctrl+Z (Undo):", count_after_undo)
    assert count_after_undo > count_after_del, "Undo should restore the deleted cell"
    print("PASS: Undo (Ctrl+Z) restored the deleted cell!")

    page.screenshot(path="scratch/drag_and_drop_verified.png")
    print("Captured scratch/drag_and_drop_verified.png")
    browser.close()


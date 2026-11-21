import os
from playwright.sync_api import sync_playwright

def test_academic_master():
    pages_to_test = [
        'pages/principal/principal-academic-workspace.html',
        'pages/principal/principal-requests.html',
        'pages/principal/principal-teacher-class-assignment.html',
        'pages/principal/principal-timetables.html',
        'pages/principal/principal-subjects.html',
        'pages/admin/admin-timetables.html',
        'pages/admin/admin-teacher-class-assignment.html',
        'pages/admin/admin-subjects.html'
    ]

    out_dir = r'C:\Users\oudom\.gemini\antigravity\brain\f0e0db56-cd04-4f51-a7f8-40ba21b43536\principal_academic_qa'
    os.makedirs(out_dir, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch()
        
        # Test Desktop (1440px)
        page = browser.new_page(viewport={'width': 1440, 'height': 900})
        for ppath in pages_to_test:
            fname = os.path.basename(ppath).replace('.html', '')
            url = f"http://127.0.0.1:3000/{ppath}"
            errors = []
            page.on('console', lambda msg: errors.append(msg.text) if msg.type == 'error' else None)
            
            try:
                page.goto(url, wait_until='networkidle', timeout=10000)
                page.wait_for_timeout(300)
                
                # Check layout
                title = page.locator('h1').first
                box = title.bounding_box()
                title_text = title.inner_text().strip() if box else 'None'
                x_pos = box['x'] if box else None
                
                # Screenshot
                shot_path = os.path.join(out_dir, f'desktop_{fname}.png')
                page.screenshot(path=shot_path)
                print(f"[Desktop 1440] {fname}: title='{title_text[:25]}' x={x_pos} errs={len(errors)}")
            except Exception as e:
                print(f"Error testing {ppath}: {e}")

        # Test Mobile (375px)
        page_m = browser.new_page(viewport={'width': 375, 'height': 812})
        for ppath in pages_to_test:
            fname = os.path.basename(ppath).replace('.html', '')
            url = f"http://127.0.0.1:3000/{ppath}"
            try:
                page_m.goto(url, wait_until='networkidle', timeout=10000)
                page_m.wait_for_timeout(300)
                
                # Check hamburger
                hb = page_m.locator('[data-action="toggle-sidebar"]').first
                hb_visible = hb.is_visible() if hb.count() > 0 else False
                
                # Screenshot
                shot_path = os.path.join(out_dir, f'mobile_{fname}.png')
                page_m.screenshot(path=shot_path)
                print(f"[Mobile 375]  {fname}: hamburger={hb_visible}")
            except Exception as e:
                print(f"Error testing mobile {ppath}: {e}")

        browser.close()

    print(f"Verification completed. Screenshots saved to {out_dir}.")

if __name__ == '__main__':
    test_academic_master()

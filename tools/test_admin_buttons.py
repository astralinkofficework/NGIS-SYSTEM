import os
from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto('http://127.0.0.1:3000/pages/admin/admin.html')
        page.wait_for_load_state('networkidle')
        
        elements = page.query_selector_all('button, a.btn, .btn, .ov-btn, [role="button"]')
        print(f"Found {len(elements)} clickable elements on admin.html")
        for i, el in enumerate(elements):
            text = (el.inner_text() or el.get_attribute('aria-label') or el.get_attribute('title') or el.get_attribute('class') or '').strip().replace('\n', ' ')[:30]
            tag = el.evaluate('el => el.tagName')
            cls = el.get_attribute('class') or ''
            
            # evaluate before
            cb = el.evaluate('el => window.getComputedStyle(el).color')
            bb = el.evaluate('el => window.getComputedStyle(el).backgroundColor')
            
            try:
                el.hover(timeout=500)
                page.wait_for_timeout(30)
            except:
                continue
            
            ca = el.evaluate('el => window.getComputedStyle(el).color')
            ba = el.evaluate('el => window.getComputedStyle(el).backgroundColor')
            oa = el.evaluate('el => window.getComputedStyle(el).opacity')
            
            print(f"[{tag}] '{text}' | before: color={cb}, bg={bb} | after hover: color={ca}, bg={ba}, op={oa}")
        browser.close()

if __name__ == '__main__':
    run()

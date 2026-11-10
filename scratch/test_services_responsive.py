from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    # Test mobile 375px
    page = browser.new_page(viewport={'width': 375, 'height': 812})
    page.goto('http://127.0.0.1:3000/pages/principal/principal-services.html')
    page.wait_for_timeout(600)
    page.screenshot(path='scratch/services_mobile_before.png', full_page=True)
    
    # Test tablet 768px
    page2 = browser.new_page(viewport={'width': 768, 'height': 1024})
    page2.goto('http://127.0.0.1:3000/pages/principal/principal-services.html')
    page2.wait_for_timeout(600)
    page2.screenshot(path='scratch/services_tablet_before.png')
    
    browser.close()
    print("Screenshots taken")


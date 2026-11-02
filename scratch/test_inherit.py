from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.set_content('''
        <div style="background: rgb(243, 243, 245); padding: 20px;">
            <div id="card" class="card" style="background: rgb(255, 255, 255);">
                Hello Card
            </div>
        </div>
        <style>
            .card:hover { background-color: inherit !important; }
        </style>
    ''')
    c = page.locator('#card')
    print('Before hover:', c.evaluate('el => window.getComputedStyle(el).backgroundColor'))
    c.hover()
    print('On hover with inherit:', c.evaluate('el => window.getComputedStyle(el).backgroundColor'))
    browser.close()


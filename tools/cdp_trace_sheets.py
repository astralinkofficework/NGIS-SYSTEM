from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={'width': 1366, 'height': 768})
    client = page.context.new_cdp_session(page)
    
    sheets = {}
    def on_sheet_added(event):
        header = event.get('header', {})
        sheets[header.get('styleSheetId')] = header.get('sourceURL') or 'inline'

    client.on('CSS.styleSheetAdded', on_sheet_added)
    client.send('CSS.enable')
    client.send('DOM.enable')
    
    page.goto('http://127.0.0.1:3000/pages/admin/admin-departments.html', wait_until='networkidle')
    
    doc = client.send('DOM.getDocument')
    node = client.send('DOM.querySelector', {'nodeId': doc['root']['nodeId'], 'selector': 'section.flex.flex-col'})
    matched = client.send('CSS.getMatchedStylesForNode', {'nodeId': node['nodeId']})
    
    print("--- DETAILED CSS RULE TRACE ---")
    for mr in matched.get('matchedCSSRules', []):
        rule = mr.get('rule', {})
        selector = rule.get('selectorList', {}).get('text')
        sheetId = rule.get('styleSheetId')
        url = sheets.get(sheetId, 'unknown')
        styles = rule.get('style', {}).get('cssProperties', [])
        for prop in styles:
            if 'flex-direction' in prop.get('name', ''):
                print(f"URL: {url}")
                print(f"  Selector: {selector} -> {prop.get('name')}: {prop.get('value')}, !imp: {prop.get('important')}")
    browser.close()

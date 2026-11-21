from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={'width': 1366, 'height': 768})
    client = page.context.new_cdp_session(page)
    page.goto('http://127.0.0.1:3000/pages/admin/admin-departments.html', wait_until='networkidle')
    client.send('DOM.enable')
    client.send('CSS.enable')
    doc = client.send('DOM.getDocument')
    node = client.send('DOM.querySelector', {'nodeId': doc['root']['nodeId'], 'selector': 'section.flex.flex-col'})
    matched = client.send('CSS.getMatchedStylesForNode', {'nodeId': node['nodeId']})
    
    print("--- MATCHED RULES FOR flex-direction ---")
    for mr in matched.get('matchedCSSRules', []):
        rule = mr.get('rule', {})
        selector = rule.get('selectorList', {}).get('text')
        styles = rule.get('style', {}).get('cssProperties', [])
        sheetId = rule.get('styleSheetId')
        
        has_fd = any('flex-direction' in prop.get('name', '') for prop in styles)
        if has_fd:
            sheet_info = client.send('CSS.getStyleSheetHeader', {'styleSheetId': sheetId})
            sourceURL = sheet_info.get('header', {}).get('sourceURL', 'inline')
            print(f"File: {sourceURL} | Selector: {selector}")
            for prop in styles:
                if 'flex-direction' in prop.get('name', ''):
                    print(f"   -> {prop.get('name')}: {prop.get('value')}, !important: {prop.get('important')}")
    browser.close()

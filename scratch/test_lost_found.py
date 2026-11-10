from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto('http://127.0.0.1:3000/pages/student/student-lost-found.html')
    page.wait_for_timeout(500)
    page.evaluate("() => { if (typeof window.switchRole === 'function') window.switchRole('staff'); if (typeof window.switchView === 'function') window.switchView('staff'); }")
    page.wait_for_timeout(500)
    btns = page.evaluate('''() => {
        const actionCells = document.querySelectorAll('td.table-actions, td .action-group');
        return Array.from(actionCells).map(c => ({
            html: c.innerHTML.trim(),
            text: c.innerText.trim(),
            hasIcon: !!c.querySelector('svg, [data-ngis-icon]')
        }));
    }''')
    print('Staff view action cells:', len(btns))
    for b in btns[:5]:
        print(b)
    browser.close()


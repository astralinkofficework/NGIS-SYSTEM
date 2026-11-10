from playwright.sync_api import sync_playwright

def test_removal():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto('http://127.0.0.1:3000/pages/principal/principal.html', wait_until='domcontentloaded')
        
        # Check title
        print('Page title:', page.title())
        
        # Check for any lingering approvals links in DOM
        links = page.eval_on_selector_all('a[href*="principal-approvals"]', 'elements => elements.length')
        print('Links to principal-approvals found on dashboard:', links)
        assert links == 0, 'Found lingering link to principal-approvals'
        
        # Check sidebar links
        sidebar_links = page.eval_on_selector_all('.sidebar-menu-item a[href*="principal-approvals"]', 'elements => elements.length')
        print('Sidebar links to principal-approvals:', sidebar_links)
        assert sidebar_links == 0, 'Found lingering sidebar link to principal-approvals'
        
        # Check 404 response when navigating directly to principal-approvals.html
        response = page.goto('http://127.0.0.1:3000/pages/principal/principal-approvals.html')
        print('Direct navigation to principal-approvals.html status:', response.status)
        assert response.status == 404, f'Expected 404 but got {response.status}'
        
        browser.close()
        print('ALL CHECKS PASSED: principal-approvals.html completely removed!')

if __name__ == '__main__':
    test_removal()


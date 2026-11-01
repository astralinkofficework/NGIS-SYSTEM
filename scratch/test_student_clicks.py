import asyncio
from playwright.async_api import async_playwright

async def test_student_sidebar():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        
        # 1. Start at student dashboard
        print("Navigating to student.html...")
        await page.goto("http://127.0.0.1:3000/pages/student/student.html", wait_until="networkidle")
        
        # Check current sidebar links
        links = await page.evaluate('''() => {
            const navLinks = Array.from(document.querySelectorAll('#sidebar .nav-link'));
            return navLinks.map(a => ({
                id: a.dataset.id,
                label: a.querySelector('.nav-link-label') ? a.querySelector('.nav-link-label').innerText.trim() : a.innerText.trim(),
                href: a.getAttribute('href'),
                resolvedHref: a.href
            }));
        }''')
        
        print(f"Found {len(links)} sidebar links in Student Dashboard:")
        for l in links:
            print(f"  [{l['id']}] {l['label']} -> {l['href']}")
            
        print("\nNow testing clicking each link from a clean student session:")
        for l in links:
            if l['id'] == 'logout':
                continue
            # Reset to student page
            await page.goto("http://127.0.0.1:3000/pages/student/student.html", wait_until="networkidle")
            
            # Click the link
            selector = f'#sidebar .nav-link[data-id="{l["id"]}"]'
            try:
                await page.click(selector)
                await page.wait_for_load_state("networkidle")
                current_url = page.url
                
                # Check what portal is rendered on the target page
                portal_info = await page.evaluate('''() => {
                    return {
                        bodyRole: document.body.dataset.role,
                        pageRole: window.PAGE ? window.PAGE.role : null,
                        sidebarBrand: document.querySelector('.side-brand-title') ? document.querySelector('.side-brand-title').innerText : null,
                        localStoragePortal: localStorage.getItem('ngis_active_portal')
                    };
                }''')
                
                is_teacher = 'teacher' in current_url or portal_info['bodyRole'] == 'teacher' or portal_info['pageRole'] == 'teacher'
                status = "FAIL (TEACHER REDIRECT!)" if is_teacher else "PASS (Student)"
                print(f"  Clicked [{l['label']}]: {status}")
                print(f"     URL: {current_url}")
                print(f"     BodyRole: {portal_info['bodyRole']}, PageRole: {portal_info['pageRole']}, Brand: {portal_info['sidebarBrand']}")
                
            except Exception as e:
                print(f"  Error clicking [{l['label']}]: {e}")
                
        await browser.close()

if __name__ == '__main__':
    asyncio.run(test_student_sidebar())


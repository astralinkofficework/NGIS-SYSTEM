import asyncio
from playwright.async_api import async_playwright

async def test_links():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        
        # 1. Start at student dashboard
        print("Navigating to student.html...", flush=True)
        await page.goto("http://127.0.0.1:3000/pages/student/student.html", wait_until="networkidle")
        
        # Get all sidebar links
        links = await page.evaluate('''() => {
            const navLinks = Array.from(document.querySelectorAll('#sidebar .nav-link'));
            return navLinks.map(a => ({
                id: a.dataset.id,
                label: a.querySelector('.nav-link-label') ? a.querySelector('.nav-link-label').innerText.trim() : a.innerText.trim(),
                href: a.getAttribute('href'),
                fullHref: a.href
            }));
        }''')
        
        print(f"Total Student Sidebar Links: {len(links)}", flush=True)
        
        for l in links:
            if l['id'] == 'logout':
                continue
            print(f"\n--- Testing [{l['label']}] ({l['href']}) ---", flush=True)
            try:
                # Navigate directly to the link href as the sidebar does
                await page.goto(l['fullHref'], wait_until="networkidle", timeout=6000)
                
                info = await page.evaluate('''() => {
                    const brand = document.querySelector('.side-brand-title');
                    return {
                        url: window.location.href,
                        pathname: window.location.pathname,
                        pageRole: window.PAGE ? window.PAGE.role : 'none',
                        bodyRole: document.body.dataset.role || 'none',
                        portalBrand: brand ? brand.innerText.trim() : 'none',
                        activePortalStore: localStorage.getItem('ngis_active_portal')
                    };
                }''')
                
                is_teacher = 'teacher' in info['pathname'] or info['pageRole'] == 'teacher' or info['bodyRole'] == 'teacher' or 'Teacher' in info['portalBrand']
                status = "FAILED -> REDIRECTED TO TEACHER!" if is_teacher else "PASSED -> Correct Student Role"
                print(f"Result: {status}", flush=True)
                print(f"  URL: {info['url']}", flush=True)
                print(f"  pageRole: {info['pageRole']} | bodyRole: {info['bodyRole']} | brand: {info['portalBrand']}", flush=True)
                
            except Exception as e:
                print(f"Result: ERROR -> {e}", flush=True)
                
        await browser.close()
        print("\nFinished Student Sidebar audit!", flush=True)

if __name__ == '__main__':
    asyncio.run(test_links())


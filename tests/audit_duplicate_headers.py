import asyncio, glob, os
from playwright.async_api import async_playwright

async def audit_headers():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        pages = glob.glob('pages/**/*.html', recursive=True) + glob.glob('*.html')
        pages = [p.replace('\\', '/') for p in pages if 'node_modules' not in p and 'scratch' not in p]
        
        viewports = [
            ("Desktop", 1440, 900),
            ("Mobile", 390, 844)
        ]
        
        duplicate_issues = []
        
        for vp_name, w, h in viewports:
            context = await browser.new_context(viewport={"width": w, "height": h})
            await context.add_init_script("""
                localStorage.setItem('auth_user', JSON.stringify({
                    id: 'admin-1',
                    name: 'Sok Panha Heng',
                    role: 'admin',
                    email: 'admin@ngis.edu'
                }));
                localStorage.setItem('token', 'fake-jwt-token');
                localStorage.setItem('ngis-theme', 'light');
            """)
            page = await context.new_page()
            
            for path in sorted(pages):
                url = f"http://127.0.0.1:3000/{path}"
                try:
                    await page.goto(url, wait_until="domcontentloaded", timeout=5000)
                    await page.wait_for_timeout(200)
                    
                    # Evaluate visible headers / topbars
                    visible_headers = await page.evaluate("""
                        () => {
                            const headers = Array.from(document.querySelectorAll('header, .hero-topbar, .topbar, #heroBanner .hero'));
                            const visible = headers.filter(h => {
                                const rect = h.getBoundingClientRect();
                                const style = window.getComputedStyle(h);
                                return style.display !== 'none' && style.visibility !== 'hidden' && rect.height > 10;
                            });
                            return visible.map(h => ({
                                tag: h.tagName,
                                id: h.id,
                                className: h.className,
                                text: h.innerText.slice(0, 40).replace(/\\n/g, ' '),
                                rect: { y: Math.round(h.getBoundingClientRect().y), height: Math.round(h.getBoundingClientRect().height) }
                            }));
                        }
                    """)
                    
                    # Check if there are overlapping or multiple visible top headers
                    top_headers = [h for h in visible_headers if h['rect']['y'] < 200]
                    # Also check for duplicate title sections
                    if len(top_headers) > 1:
                        duplicate_issues.append((path, vp_name, top_headers))
                except Exception as e:
                    # Ignore load errors for external or static templates
                    pass
            await context.close()
            
        await browser.close()
        
        print(f"\n=======================================================")
        print(f"PAGES WITH MULTIPLE VISIBLE HEADERS: {len(duplicate_issues)}")
        print(f"=======================================================")
        for path, vp, hdrs in duplicate_issues:
            print(f"\n[PAGE]: {path} on {vp}")
            for h in hdrs:
                safe_text = h['text'].encode('ascii', 'replace').decode('ascii')
            print(f"   - <{h['tag']} id='{h['id']}' class='{h['className'][:30]}'> y={h['rect']['y']}, h={h['rect']['height']} | '{safe_text}'")

if __name__ == '__main__':
    asyncio.run(audit_headers())

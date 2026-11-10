from playwright.sync_api import sync_playwright
import glob, re

pages = glob.glob('pages/**/*.html', recursive=True)
pages.extend(glob.glob('*.html'))

with sync_playwright() as p:
    browser = p.chromium.launch()
    
    runtime_no_header = []
    runtime_no_toggle = []
    
    for path in sorted(pages):
        norm_path = path.replace('\\', '/')
        # Skip concepts or non-page html if any
        if '_concepts' in norm_path:
            continue
            
        page = browser.new_page(viewport={'width': 1280, 'height': 800})
        try:
            page.goto(f'http://127.0.0.1:3000/{norm_path}', timeout=5000)
            page.wait_for_timeout(300)
            
            # Check for header
            # Look for <header>, .topbar, .hero-topbar, .mobile-appbar, header tag
            has_header = page.evaluate("""() => {
                const h = document.querySelector('header, .hero-topbar, .topbar, .mobile-appbar, [role=\"banner\"]');
                return !!h;
            }""")
            
            # Check for toggle button
            has_toggle = page.evaluate("""() => {
                const b = document.querySelector('[data-action=\"toggle-sidebar\"], .hamburger-btn, .mobile-hamburger-btn, #htbHamburger');
                return !!b;
            }""")
            
            if not has_header:
                runtime_no_header.append(norm_path)
            if not has_toggle:
                runtime_no_toggle.append(norm_path)
                
        except Exception as e:
            print(f"Error loading {norm_path}: {e}")
        finally:
            page.close()
            
    browser.close()

print(f"\n==========================================")
print(f"PAGES WITH NO HEADER AT RUNTIME ({len(runtime_no_header)}):")
for p in runtime_no_header:
    print('  NO HEADER:', p)

print(f"\n==========================================")
print(f"PAGES WITH NO TOGGLE BUTTON AT RUNTIME ({len(runtime_no_toggle)}):")
for p in runtime_no_toggle:
    print('  NO TOGGLE:', p)


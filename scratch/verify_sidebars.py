from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={'width': 1440, 'height': 900})
    
    urls = [
        ('/pages/principal/principal.html', 'principal_sidebar_fixed.png'),
        ('/pages/admin/admin.html', 'admin_sidebar_fixed.png'),
        ('/pages/teacher/teacher.html', 'teacher_sidebar_fixed.png'),
        ('/pages/student/student.html', 'student_sidebar_fixed.png'),
    ]
    
    for path, img_name in urls:
        page.goto('http://127.0.0.1:3000' + path, wait_until='domcontentloaded')
        page.wait_for_timeout(600)
        
        info = page.evaluate('''() => {
            const sb = document.querySelector('.sidebar, #sidebar');
            if (!sb) return { error: 'No sidebar' };
            const links = Array.from(sb.querySelectorAll('.nav-link, .nav-item')).slice(0, 8);
            return links.map(l => {
                const icon = l.querySelector('.nav-link-icon, .nav-icon, span.material-symbols-outlined, i, svg');
                const text = l.querySelector('.nav-link-label') || l;
                return {
                    label: text.textContent.trim(),
                    active: l.classList.contains('active'),
                    iconColor: icon ? window.getComputedStyle(icon).color : 'none',
                    iconSize: icon ? window.getComputedStyle(icon).fontSize : 'none',
                    iconWidth: icon ? window.getComputedStyle(icon).width : 'none',
                    iconOpacity: icon ? window.getComputedStyle(icon).opacity : 'none',
                    iconVisibility: icon ? window.getComputedStyle(icon).visibility : 'none',
                    textColor: window.getComputedStyle(text).color,
                    linkBg: window.getComputedStyle(l).backgroundColor
                };
            });
        }''')
        
        print(f"=== {path} ===")
        for item in info:
            print(f"  {item['label'][:25]:<25} | Active: {str(item['active']):<5} | Icon: {item['iconColor']} (size: {item['iconSize']}, opacity: {item['iconOpacity']}) | Text: {item['textColor']}")
            
        sb = page.locator('#sidebar')
        sb.screenshot(path=f'C:/Users/oudom/.gemini/antigravity/brain/8fd19b10-a09a-43d8-a122-cb4a75dc0ff6/{img_name}')
        print(f"  Saved screenshot: {img_name}")

    browser.close()


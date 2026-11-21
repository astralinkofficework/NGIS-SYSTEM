from playwright.sync_api import sync_playwright

def inspect():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={'width': 1440, 'height': 900})
        page.goto('http://127.0.0.1:3000/pages/student/student.html')
        page.wait_for_timeout(1000)
        
        # Take screenshot of top section
        page.screenshot(path='student_html_current_full.png', full_page=True)
        print("Captured student_html_current_full.png")
        
        # Check what badges exist on student.html
        badges = page.evaluate("""() => {
            const list = document.querySelectorAll('*');
            const res = [];
            list.forEach(el => {
                const text = (el.innerText || '').trim();
                const cls = el.className;
                const style = window.getComputedStyle(el);
                if (typeof cls === 'string' && (cls.includes('badge') || cls.includes('pill') || cls.includes('tag'))) {
                    res.push({
                        tag: el.tagName,
                        className: cls,
                        text: text,
                        bg: style.backgroundColor,
                        color: style.color
                    });
                }
            });
            return res;
        }""")
        print(f"Total badge/pill/tag elements on student.html: {len(badges)}")
        for b in badges:
            print(" ", b)
            
        browser.close()

if __name__ == '__main__':
    inspect()

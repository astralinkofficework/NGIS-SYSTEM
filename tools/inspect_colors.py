from playwright.sync_api import sync_playwright

def inspect_colors():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={'width': 1440, 'height': 900})
        page.goto('http://127.0.0.1:3000/pages/student/student-calendar.html')
        page.wait_for_timeout(1000)
        
        elements = page.evaluate("""() => {
            const all = document.querySelectorAll('*');
            const res = [];
            for (const el of all) {
                if (el.children.length > 2) continue; // skip large containers
                const style = window.getComputedStyle(el);
                const bg = style.backgroundColor;
                const br = style.borderRadius;
                if (bg && bg !== 'rgba(0, 0, 0, 0)' && bg !== 'rgb(255, 255, 255)' && bg !== 'rgb(248, 250, 252)') {
                    res.push({
                        tag: el.tagName,
                        className: el.className,
                        text: el.innerText.trim().slice(0, 40),
                        bg: bg,
                        color: style.color,
                        borderRadius: br
                    });
                }
            }
            return res;
        }""")
        print("Elements with colored backgrounds on student-calendar.html:")
        for e in elements:
            print(" ", e)
        browser.close()

if __name__ == '__main__':
    inspect_colors()

from playwright.sync_api import sync_playwright

def inspect():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={'width': 1440, 'height': 900})
        page.goto('http://127.0.0.1:3000/pages/student/student-calendar.html')
        page.wait_for_timeout(1000)
        
        chips = page.evaluate("""() => {
            return Array.from(document.querySelectorAll('.cal-event-chip, [class*="chip"], [class*="badge"], [class*="pill"]')).map(el => ({
                tag: el.tagName,
                class: el.className,
                text: el.innerText.trim(),
                bg: window.getComputedStyle(el).backgroundColor,
                color: window.getComputedStyle(el).color
            }));
        }""")
        print('Pills/Chips/Badges on student-calendar.html count:', len(chips))
        for c in chips:
            print(' ', c)
            
        print("\n--- Also inspecting student.html ---")
        page.goto('http://127.0.0.1:3000/pages/student/student.html')
        page.wait_for_timeout(1000)
        dash_chips = page.evaluate("""() => {
            return Array.from(document.querySelectorAll('[class*="badge"], [class*="pill"], [class*="tag"]')).map(el => ({
                tag: el.tagName,
                class: el.className,
                text: el.innerText.trim(),
                bg: window.getComputedStyle(el).backgroundColor,
                color: window.getComputedStyle(el).color
            }));
        }""")
        print('Pills/Badges on student.html count:', len(dash_chips))
        for c in dash_chips[:15]:
            print(' ', c)
            
        browser.close()

if __name__ == '__main__':
    inspect()

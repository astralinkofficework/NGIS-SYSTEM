from playwright.sync_api import sync_playwright
from PIL import Image

def verify():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={'width': 1440, 'height': 900})
        page.goto('http://127.0.0.1:3000/pages/student/student.html')
        page.wait_for_timeout(1000)
        
        # Screenshot the top header section
        header = page.locator('header.workspace-hero')
        header.screenshot(path='student_hero_spacing_after.png')
        print("Captured student_hero_spacing_after.png")
        
        # Check computed styles of .workspace-hero-body and text
        styles = page.evaluate("""() => {
            const body = document.querySelector('.workspace-hero-body');
            const date = document.querySelector('#workspaceHeroDate');
            const h1 = document.querySelector('#workspaceHeroGreeting');
            const sub = document.querySelector('#workspaceHeroSub');
            return {
                bodyPaddingTop: window.getComputedStyle(body).paddingTop,
                dateTop: date.getBoundingClientRect().top,
                h1Top: h1.getBoundingClientRect().top,
                subTop: sub.getBoundingClientRect().top
            };
        }""")
        print("Computed spacing:", styles)
        
        browser.close()

if __name__ == '__main__':
    verify()

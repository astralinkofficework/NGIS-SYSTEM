from playwright.sync_api import sync_playwright

urls = [
    ("teacher-class-assignment", "http://127.0.0.1:3000/pages/principal/principal-teacher-class-assignment.html"),
    ("timetable-builder", "http://127.0.0.1:3000/pages/principal/principal-timetable-builder.html"),
    ("timetables", "http://127.0.0.1:3000/pages/principal/principal-timetables.html"),
    ("subjects", "http://127.0.0.1:3000/pages/principal/principal-subjects.html"),
    ("records", "http://127.0.0.1:3000/pages/principal/principal-records.html")
]

with sync_playwright() as p:
    browser = p.chromium.launch()
    for name, u in urls:
        page = browser.new_page(viewport={'width': 1280, 'height': 800})
        page.goto(u)
        page.wait_for_timeout(1000)
        data = page.evaluate("""() => {
            var body = document.body;
            var ks = document.getElementById('ks-root');
            var sidebar = document.querySelector('.sidebar') || document.querySelector('aside') || document.querySelector('#sidebar') || document.querySelector('[data-role="sidebar"]');
            return {
                title: document.title,
                bodyTextLen: body.innerText.length,
                bodySnippet: body.innerText.substring(0, 300).replace(/\\n+/g, ' | '),
                ksChildren: ks ? ks.children.length : 0,
                hasSidebar: !!sidebar,
                sidebarLinks: Array.from(document.querySelectorAll('a')).map(a => a.getAttribute('href')).filter(h => h && h.includes('principal')).slice(0, 10)
            };
        }""")
        print(f"=== {name} ===")
        print("Title:", data['title'])
        print("Text len:", data['bodyTextLen'])
        print("Snippet:", data['bodySnippet'])
        print("KS Children:", data['ksChildren'])
        print("Has Sidebar:", data['hasSidebar'])
        print("Sidebar Links:", data['sidebarLinks'])
        page.close()
    browser.close()

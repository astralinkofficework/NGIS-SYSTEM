from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    page.goto("http://127.0.0.1:3000/pages/principal/principal-timetable-builder.html")
    page.wait_for_timeout(500)
    
    topbar = page.locator(".hero-topbar")
    print("Topbar HTML preview:")
    print(topbar.inner_html()[:300])

    brand = page.locator(".htb-brand-wrap")
    print("Brand logo visible:", brand.is_visible())
    
    search = page.locator(".htb-search-wrap")
    print("Search input visible:", search.is_visible())
    
    profile = page.locator("#htbProfile")
    print("Profile chip visible:", profile.is_visible(), "Text:", profile.inner_text().replace('\n', ' '))

    browser.close()


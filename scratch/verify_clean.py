from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={'width': 1280, 'height': 900})
    
    # 1. Builder page
    page.goto('http://127.0.0.1:3000/pages/principal/principal-timetable-builder.html', wait_until='networkidle')
    page.wait_for_timeout(1000)
    page.screenshot(path='scratch/cleaned_builder.png')
    
    has_switcher = page.evaluate('() => !!document.getElementById("viewSwitcher")')
    has_guidelines = page.evaluate('() => document.body.innerText.includes("Cambodian MoEYS Guidelines")')
    print("Builder - Has viewSwitcher:", has_switcher)
    print("Builder - Has MoEYS Guidelines:", has_guidelines)
    assert not has_switcher, "viewSwitcher should not be present"
    assert not has_guidelines, "MoEYS Guidelines should not be present"
    
    # 2. Subjects page
    page.goto('http://127.0.0.1:3000/pages/principal/principal-subjects.html', wait_until='networkidle')
    page.wait_for_timeout(1000)
    page.screenshot(path='scratch/cleaned_subjects.png')
    
    has_school_name = page.evaluate('() => document.body.innerText.includes("វិទ្យាល័យ ហ្គេតវេ អន្តរជាតិថ្មី")')
    has_curriculum = page.evaluate('() => document.body.innerText.includes("Standard Cambodian National Curriculum (MoEYS)")')
    print("Subjects - Has school name:", has_school_name)
    print("Subjects - Has curriculum text:", has_curriculum)
    assert not has_school_name, "School name should not be present"
    assert not has_curriculum, "Curriculum text should not be present"
    
    print("ALL ASSERTIONS PASSED!")
    browser.close()


with open('tools/test_teacher_portal_master.py', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace(
    'desktop_page.click("button:has-text(\'New Request\')")',
    'desktop_page.locator("button:has-text(\'New Request\'):visible").first.click()'
)
text = text.replace(
    'desktop_page.click("button:has-text(\'Report Item\')")',
    'desktop_page.locator("button:has-text(\'Report Item\'):visible").first.click()'
)

with open('tools/test_teacher_portal_master.py', 'w', encoding='utf-8') as f:
    f.write(text)

print("Updated with :visible selector.")

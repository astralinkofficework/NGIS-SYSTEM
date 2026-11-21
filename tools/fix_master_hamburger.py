with open('tools/test_teacher_portal_master.py', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace(
    'hamburger = mobile_page.locator("button[data-action=\'toggle-sidebar\'], .hamburger-btn").first',
    'hamburger = mobile_page.locator("button[data-action=\'toggle-sidebar\']:visible, .hamburger-btn:visible").first'
)

with open('tools/test_teacher_portal_master.py', 'w', encoding='utf-8') as f:
    f.write(text)

print("Updated hamburger selector with :visible.")

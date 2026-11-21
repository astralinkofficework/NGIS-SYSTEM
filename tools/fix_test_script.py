with open('tools/test_teacher_portal_master.py', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace("button:has-text('Done')", "button:has-text('Dismiss')")

with open('tools/test_teacher_portal_master.py', 'w', encoding='utf-8') as f:
    f.write(text)

print("Updated button text to Dismiss.")

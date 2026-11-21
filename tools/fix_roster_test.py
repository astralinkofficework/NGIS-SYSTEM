with open('tools/test_teacher_portal_master.py', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace("desktop_page.locator(\"#detailModalName\").inner_text()", "desktop_page.locator(\"#modalStudentName\").inner_text()")

with open('tools/test_teacher_portal_master.py', 'w', encoding='utf-8') as f:
    f.write(text)

print("Updated #detailModalName to #modalStudentName.")

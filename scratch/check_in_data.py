with open('all_pages_data.js', 'r', encoding='utf-8') as f:
    text = f.read()

print("teacher-lost-found in all_pages_data.js?", "teacher-lost-found.html" in text)
print("teacher-services in all_pages_data.js?", "teacher-services.html" in text)


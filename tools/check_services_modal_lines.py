with open('pages/student/student-services.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(845, min(len(lines), 1050)):
    if '<!-- ' in lines[i] or '<script' in lines[i] or 'id="requestDetailsModal"' in lines[i]:
        print(f'{i+1}: {lines[i]}')

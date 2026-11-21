with open('pages/student/student-assignments.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(585, min(len(lines), 815)):
    if 'tasksList' in lines[i] or 'RIGHT COLUMN' in lines[i] or 'col-span-5' in lines[i] or 'lg:col-span-5' in lines[i]:
        print(f'{i+1}: {lines[i]}')

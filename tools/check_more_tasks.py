with open('pages/student/student-assignments.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(745, min(len(lines), 950)):
    if 'task-card' in lines[i] or 'id="tasksList"' in lines[i] or '</div>' in lines[i] and 'tasksList' in lines[max(0, i-20)]:
        print(f'{i+1}: {lines[i].strip()[:90]}')

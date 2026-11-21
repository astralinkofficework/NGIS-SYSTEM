with open('pages/student/student-assignments.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'window.setCourseFilter = function' in l:
        for j in range(max(0, i-5), min(len(lines), i+80)):
            print(f'{j+1}: {lines[j]}', end='')
        break

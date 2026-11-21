with open('pages/student/student-lost-found.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'function openReportModal' in l:
        for j in range(max(0, i-5), min(len(lines), i+30)):
            print(f'{j+1}: {lines[j]}', end='')
        break

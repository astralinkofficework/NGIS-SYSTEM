with open('pages/principal/principal-classes.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'editClassModal' in l or 'Edit Class' in l:
        start = max(0, i-5)
        end = min(len(lines), i+60)
        print(f'=== Lines {start+1}-{end} in principal-classes.html ===')
        for j in range(start, end):
            print(f'{j+1}: {lines[j].strip()}'.encode('ascii', 'replace').decode('ascii'))
        break


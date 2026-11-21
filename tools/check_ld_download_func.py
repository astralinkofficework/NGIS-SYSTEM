with open('pages/shared/js/lesson-details.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'function ldDownload' in l:
        for j in range(max(0, i-5), min(len(lines), i+25)):
            print(f'{j+1}: {lines[j]}', end='')
        break

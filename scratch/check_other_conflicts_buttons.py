with open('assets/js/khmer-suite-ui.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for line_num in [1511, 1746, 2010]:
    print(f'--- Line {line_num} ---')
    for i in range(max(0, line_num - 5), min(len(lines), line_num + 6)):
        print(f'{i+1}: {lines[i]}', end='')


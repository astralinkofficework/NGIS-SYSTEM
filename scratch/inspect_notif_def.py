with open('server.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if '@app.route(\'/api/notifications\'' in l:
        print(f'=== Line {i+1} ===')
        for j in range(i, i+50):
            print(f'{j+1}: {lines[j]}', end='')
        break


with open('assets/js/khmer-suite-ui.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print('wizardHtml lines:', 516, 'to', 938)
# Print the return statement and its structure
for i in range(714, 755):
    print(f'{i+1}: {lines[i]}', end='')


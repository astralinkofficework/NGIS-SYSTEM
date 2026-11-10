with open('assets/js/khmer-suite-ui.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

start = None
end = None
for i, l in enumerate(lines):
    if 'function wizardHtml()' in l:
        start = i
    if start and 'function attachWizardInteractions()' in l:
        end = i
        break

print(f'wizardHtml is from line {start+1} to {end+1}')
for i in range(start, end):
    line = lines[i]
    if 'border' in line or 'rounded' in line or 'shadow' in line:
        print(f'{i+1}: {line.strip()}')


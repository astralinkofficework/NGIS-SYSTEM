with open('assets/js/khmer-suite-ui.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

def print_fn(name, max_l=100):
    for i, line in enumerate(lines):
        if line.strip().startswith('function ' + name + '('):
            print(f'=== FUNCTION {name} (line {i+1}) ===')
            print(''.join(lines[i:i+max_l]))
            return

print_fn('pageHeadHtml', 60)
print_fn('wizardHtml', 80)


import re

with open('assets/js/khmer-suite-ui.js', 'r', encoding='utf-8') as f:
    text = f.read()

acts = re.findall(r'data-act=[\'"]([^\'"]+)[\'"]', text)
print('Unique data-act count:', len(set(acts)))
teacher_acts = [a for a in set(acts) if any(k in a.lower() for k in ['teacher', 'excel', 'paste', 'sheet', 'cell', 'row'])]
print('Teacher/Sheet acts:', sorted(teacher_acts))


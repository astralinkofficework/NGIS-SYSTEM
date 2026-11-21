import re

with open('pages/student/student-assignments.html', 'r', encoding='utf-8') as f:
    text = f.read()

cards = re.findall(r'<div class="task-card[^"]*"([^>]*)>', text)
print(f'Total task cards: {len(cards)}')
for i, c in enumerate(cards):
    print(f'Card {i+1}: {c}')

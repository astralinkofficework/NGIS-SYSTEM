with open('pages/student/student-assignments.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
cards = re.findall(r'<div class="task-card[^"]*"', text)
print(f'Total task cards now: {len(cards)}')
print('Has tasksPagination:', 'id="tasksPagination"' in text)
print('Has changeTasksPage:', 'changeTasksPage' in text)

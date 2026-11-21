with open('pages/student/student-assignments.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Let's inspect tasksList end in HTML
import re
idx = text.find('id="tasksList"')
print('tasksList starts at index:', idx)
# Find the closing </div> of tasksList
# Count divs after idx
depth = 0
found_end = -1
for i in range(idx, len(text)):
    if text[i:i+4] == '<div':
        depth += 1
    elif text[i:i+5] == '</div':
        depth -= 1
        if depth == 0:
            found_end = i + 6
            break

print('tasksList ends at index:', found_end)
print('After tasksList:', repr(text[found_end:found_end+300]))

with open('pages/student/student-services.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
idx = text.find('id="mobileNewRequestModal"')
if idx != -1:
    print('mobileNewRequestModal starts at line:', text[:idx].count('\n') + 1)
    end_idx = text.find('<!-- View Request Details Modal', idx)
    if end_idx != -1:
        print('Ends before View Request Details Modal at line:', text[:end_idx].count('\n') + 1)
        print('Length of modal block:', end_idx - idx)
    else:
        print('End marker not found, snippet:')
        print(text[idx:idx+800])

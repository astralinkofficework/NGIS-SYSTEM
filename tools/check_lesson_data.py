with open('pages/shared/js/lesson-data.js', 'r', encoding='utf-8') as f:
    text = f.read()

import re
pos = text.find('NGISBookmarks')
print(text[pos:pos+600])

with open('pages/shared/js/lesson-details.js', 'r', encoding='utf-8') as f:
    code = f.read()

import re
print('Has ngisDownloadFile defined?', 'function ngisDownloadFile' in code)

# Search across all project files for ngisDownloadFile
import glob
found = []
for p in glob.glob('assets/js/*.js') + glob.glob('pages/**/*.js', recursive=True):
    with open(p, 'r', encoding='utf-8', errors='ignore') as fp:
        if 'ngisDownloadFile' in fp.read():
            found.append(p)
print('Found ngisDownloadFile in:', found)

with open('pages/shared/js/lesson-details.js', 'r', encoding='utf-8') as f:
    text = f.read()

import re
funcs = re.findall(r'function\s+(ld[a-zA-Z0-9_]+)\s*\([^\)]*\)', text)
print("Functions in lesson-details.js:", funcs)

for fn in ['ldDownload', 'ldOpenInNewTab', 'ldBookmark', 'ldToggleExpand', 'ldPageStep', 'ldZoom', 'ldGoRelative', 'ldFullscreen']:
    pos = text.find(f'function {fn}')
    if pos != -1:
        print(f"\n--- {fn} ---")
        print(text[pos:pos+500])
    else:
        print(f"\n--- {fn}: NOT FOUND! ---")

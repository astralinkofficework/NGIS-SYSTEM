with open('scratch/user_prompt_10.html', 'r', encoding='utf-8') as f:
    html = f.read()

import re

tbody_end = html.find('</tbody>')
if tbody_end != -1:
    print(html[tbody_end:tbody_end+2500])


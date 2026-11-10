with open('scratch/user_prompt_10.html', 'r', encoding='utf-8') as f:
    html = f.read()

import re

tbody_match = re.search(r'<tbody[^>]*>(.*?)</tbody>', html, re.DOTALL)
if tbody_match:
    trs = re.findall(r'<tr[^>]*>.*?</tr>', tbody_match.group(1), re.DOTALL)
    for idx, tr in enumerate(trs):
        tds = re.findall(r'<td[^>]*>(.*?)</td>', tr, re.DOTALL)
        print(f"\nRow {idx+1} Col 2:")
        print(tds[1].strip())


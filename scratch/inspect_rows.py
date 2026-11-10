with open('scratch/user_prompt_10.html', 'r', encoding='utf-8') as f:
    html = f.read()

import re

tbody_match = re.search(r'<tbody[^>]*>(.*?)</tbody>', html, re.DOTALL)
if tbody_match:
    trs = re.findall(r'<tr[^>]*>.*?</tr>', tbody_match.group(1), re.DOTALL)
    for idx, tr in enumerate(trs):
        tds = re.findall(r'<td[^>]*>(.*?)</td>', tr, re.DOTALL)
        if len(tds) >= 8:
            print(f"\n================ ROW {idx+1} ================")
            print("--- Col 5 (Flow) ---")
            print(tds[4].strip())
            print("--- Col 6 (Auditor) ---")
            print(tds[5].strip())
            print("--- Col 7 (Status) ---")
            print(tds[6].strip())
            print("--- Col 8 (Actions) ---")
            print(tds[7].strip())


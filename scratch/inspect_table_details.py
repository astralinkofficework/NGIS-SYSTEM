with open('scratch/user_prompt_10.html', 'r', encoding='utf-8') as f:
    html = f.read()

import re

# Let's inspect the filters
filters_match = re.search(r'data-purpose="table-filters"[^>]*>(.*?)</section>', html, re.DOTALL)
if filters_match:
    print("=== Filters section ===")
    print(filters_match.group(1)[:1500])

# Let's inspect the entire table tag and header
table_match = re.search(r'<table[^>]*>(.*?)</table>', html, re.DOTALL)
if table_match:
    print("\n=== Table thead ===")
    thead_match = re.search(r'<thead[^>]*>(.*?)</thead>', table_match.group(1), re.DOTALL)
    if thead_match:
        print(thead_match.group(1))

# Let's inspect all 7 rows
tbody_match = re.search(r'<tbody[^>]*>(.*?)</tbody>', html, re.DOTALL)
if tbody_match:
    trs = re.findall(r'<tr[^>]*>.*?</tr>', tbody_match.group(1), re.DOTALL)
    for idx, tr in enumerate(trs):
        print(f"\n--- Row {idx+1} ---")
        tds = re.findall(r'<td[^>]*>(.*?)</td>', tr, re.DOTALL)
        for cidx, td in enumerate(tds):
            print(f"  Col {cidx+1}: {td.strip()[:180]}")


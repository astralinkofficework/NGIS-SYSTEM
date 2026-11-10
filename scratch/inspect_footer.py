with open('scratch/user_prompt_10.html', 'r', encoding='utf-8') as f:
    html = f.read()

import re

table_match = re.search(r'data-purpose="arrival-verification-table"[^>]*>(.*?)</section>', html, re.DOTALL)
if table_match:
    table_sec = table_match.group(1)
    # find footer
    footer_match = re.search(r'<div class="px-4 py-3[^>]*>(.*)', table_sec, re.DOTALL)
    if footer_match:
        print("=== Footer ===")
        print(footer_match.group(0)[:1500])


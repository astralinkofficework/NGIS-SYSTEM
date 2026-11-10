import re

with open('scratch/user_prompt_10.html', 'r', encoding='utf-8') as f:
    content = f.read()

print("Title:", re.findall(r'<title>(.*?)</title>', content))
purposes = re.findall(r'data-purpose="([^"]+)"', content)
print("Data purposes:", purposes)

# Extract table structure
table_match = re.search(r'<table[^>]*>(.*?)</table>', content, re.DOTALL)
if table_match:
    table_content = table_match.group(1)
    ths = re.findall(r'<th[^>]*>(.*?)</th>', table_content, re.DOTALL)
    print("\nTable THs count:", len(ths))
    for i, th in enumerate(ths):
        clean_th = re.sub(r'<[^>]+>', ' ', th).strip()
        clean_th = ' '.join(clean_th.split())
        print(f"  TH {i+1}: {clean_th}")

# Extract sample row
tbody_match = re.search(r'<tbody[^>]*>(.*?)</tbody>', content, re.DOTALL)
if tbody_match:
    tbody_content = tbody_match.group(1)
    trs = re.findall(r'<tr[^>]*>(.*?)</tr>', tbody_content, re.DOTALL)
    print(f"\nRows count: {len(trs)}")
    if trs:
        print("\nFirst row sample:")
        tds = re.findall(r'<td[^>]*>(.*?)</td>', trs[0], re.DOTALL)
        for i, td in enumerate(tds):
            clean_td = re.sub(r'<[^>]+>', ' ', td).strip()
            clean_td = ' '.join(clean_td.split())
            print(f"  TD {i+1}: {clean_td[:80]}")

# Check any scripts in prompt
scripts = re.findall(r'<script[^>]*>(.*?)</script>', content, re.DOTALL)
print(f"\nScripts found: {len(scripts)}")
for i, s in enumerate(scripts):
    if len(s.strip()) > 50:
        print(f"Script {i+1} preview: {s.strip()[:100]}...")


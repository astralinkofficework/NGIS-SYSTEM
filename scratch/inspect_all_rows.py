with open('scratch/user_prompt_10.html', 'r', encoding='utf-8') as f:
    html = f.read()

import re

tbody_match = re.search(r'<tbody[^>]*>(.*?)</tbody>', html, re.DOTALL)
if tbody_match:
    trs = re.findall(r'<tr[^>]*>.*?</tr>', tbody_match.group(1), re.DOTALL)
    for idx, tr in enumerate(trs):
        tds = re.findall(r'<td[^>]*>(.*?)</td>', tr, re.DOTALL)
        name = re.search(r'<div class="font-medium text-slate-900">(.*?)</div>', tds[1])
        sid = re.search(r'<div class="text-\[10px\][^>]*font-mono[^>]*>(.*?)</div>', tds[1])
        room = re.search(r'<div class="font-medium text-slate-800">(.*?)</div>\s*<div class="text-\[11px\] text-slate-500">(.*?)</div>', tds[2])
        time = re.search(r'<div class="font-mono text-[^"]*">(.*?)</div>\s*<div class="text-\[10px\][^"]*">(.*?)</div>', tds[3])
        print(f"Row {idx+1}: {name.group(1) if name else 'N/A'} ({sid.group(1) if sid else 'N/A'})")
        if room: print(f"  Room: {room.group(1)} - {room.group(2)}")
        if time: print(f"  Time: {time.group(1)} [{time.group(2)}]")


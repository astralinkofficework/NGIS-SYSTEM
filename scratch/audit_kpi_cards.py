import glob
import re

html_files = glob.glob('pages/**/*.html', recursive=True) + glob.glob('*.html')
js_files = glob.glob('assets/js/*.js')

print("Auditing KPI Metric Cards...")

kpi_patterns = re.compile(r'class=["\'][^"\']*\b(?:kpi|metric|stat-card|ov-kpi)\b[^"\']*["\'][^>]*>(.*?)(?:</div>|</a>)', re.IGNORECASE | re.DOTALL)

for fpath in html_files[:50]:
    with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # check if there are colorful kpis
    found = re.findall(r'class=["\'][^"\']*\b(?:bg-(?:emerald|blue|purple|indigo|amber|rose|red|pink|cyan|teal|yellow)-[0-9]{2,3})[^"\']*\b(?:kpi|metric|stat|card)\b[^"\']*["\']', content)
    if found:
        print(f"\nColorful cards in {fpath}:")
        for m in found[:5]:
            print(f"  {m}")

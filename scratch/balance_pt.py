import re

src = open('pages/principal/principal-teachers.html', encoding='utf-8').read()
print('div', src.count('<div'), '/', src.count('</div>'),
      '| main', src.count('<main'), '/', src.count('</main>'),
      '| form', src.count('<form'), '/', src.count('</form>'),
      '| button', src.count('<button'), '/', src.count('</button>'),
      '| select', src.count('<select'), '/', src.count('</select>'))
ids = re.findall(r'id="([^"]+)"', src)
dups = sorted({i for i in ids if ids.count(i) > 1})
print('duplicate ids:', dups or 'NONE')

# handler vs defined functions
calls = set()
for m in re.finditer(r'(?:onclick|onsubmit|onchange|oninput)="([^"]+)"', src):
    for f in re.finditer(r'([A-Za-z_]\w*)\s*\(', m.group(1)):
        calls.add(f.group(1))
defined = set(re.findall(r'function\s+([A-Za-z_]\w*)', src))
missing = sorted(c for c in calls if c not in defined and c not in ('if',))
print('undefined handlers:', missing or 'NONE')

bold = re.findall(r'font-bold|font-extrabold|font-black|font-weight:\s*[78]\d\d', src)
print('bold class violations:', len(bold))

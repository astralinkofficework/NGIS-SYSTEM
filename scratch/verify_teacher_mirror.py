import re

for p in ['pages/teacher/teacher-lost-found.html', 'pages/teacher/teacher-services.html']:
    src = open(p, encoding='utf-8').read()
    calls = set()
    for m in re.finditer(r'(?:onclick|oninput|onchange|onsubmit|onblur)="([^"]+)"', src):
        for f in re.finditer(r'([A-Za-z_]\w*)\s*\(', m.group(1)):
            calls.add(f.group(1))
    defined = set(re.findall(r'function\s+([A-Za-z_]\w*)', src))
    defined |= set(re.findall(r'(?:const|let|var)\s+([A-Za-z_]\w*)\s*=\s*(?:async\s*)?(?:function|\()', src))
    builtins = {'if', 'event', 'target'}
    missing = sorted(c for c in calls if c not in defined and c not in builtins)
    print(p)
    print('  undefined handlers:', missing or 'NONE')
    print('  div', src.count('<div'), '/', src.count('</div>'),
          '| main', src.count('<main'), '/', src.count('</main>'),
          '| button', src.count('<button'), '/', src.count('</button>'),
          '| select', src.count('<select'), '/', src.count('</select>'),
          '| form', src.count('<form'), '/', src.count('</form>'))
    ids = re.findall(r'\bid="([^"]+)"', src)
    dups = sorted({i for i in ids if ids.count(i) > 1})
    print('  duplicate ids:', dups or 'NONE')
    # bold rule check
    bold = re.findall(r'font-bold|font-extrabold|font-black|font-weight:\s*[78]\d\d', src)
    print('  bold violations:', len(bold) or 'NONE')
    # hamburger on mobile
    print('  hamburger attr:', 'toggle-sidebar' in src)
    # hero wiring
    print('  heroBanner div:', 'id="heroBanner"' in src, '| hero.js:', 'js/hero.js' in src, '| HERO_CONFIG:', 'HERO_CONFIG' in src)

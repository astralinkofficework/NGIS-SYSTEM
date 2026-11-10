"""Check font/icon-library links across principal pages + live ligature health."""
import glob, re

for f in sorted(glob.glob('pages/principal/*.html')):
    s = open(f, encoding='utf-8').read()
    name = f.replace('\\', '/').split('/')[-1]
    mat = 'Material+Symbols' in s or 'material+symbols' in s.lower()
    phos = 'phosphor' in s.lower()
    mat_spans = len(re.findall(r'class="[^"]*material-symbols-outlined', s))
    lig_words = len(re.findall(r'>\s*(search|edit|delete|visibility|close|check)\s*<', s))
    print('%-34s matLink=%-5s phosphor=%-5s matSpans=%-4d' % (name, mat, phos, mat_spans))

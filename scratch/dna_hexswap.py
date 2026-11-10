import re, sys, glob, os
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

MAP = {
  '#176B45': '#F77442', '#125638': '#E0521F', '#1E4D38': '#C24E1F',
  '#1B4533': '#C24E1F', '#235941': '#C24E1F', '#133526': '#8A3A1A',
  '#0A1D15': '#3A2418',
  '#29352E': '#1D1D1B', '#64746A': '#757371', '#8FA095': '#9D9A97',
  '#A5B4AA': '#9D9A97',
  '#E8F3ED': '#FDEBDF', '#F7F9F7': '#FBFBFB', '#E1E9E3': '#ECE7E2',
  '#EEF4F0': '#F1EDE9',
  '#F28C28': '#F77442', '#D9771A': '#E0521F', '#FFF4EB': '#FDF3EC',
}
pat = re.compile('|'.join(re.escape(k) for k in MAP), re.I)

files = sorted(glob.glob('pages/admin/*.html')) + ['assets/css/admin-view.css']
for f in files:
    t = open(f, encoding='utf-8').read()
    hits = {}
    def sub(m):
        h = m.group(0).upper()
        hits[h] = hits.get(h, 0) + 1
        return MAP[h]
    new = pat.sub(sub, t)
    if new != t:
        open(f, 'w', encoding='utf-8').write(new)
        print(f'{os.path.basename(f):38} {sum(hits.values()):>3} swaps  {hits}')
    else:
        print(f'{os.path.basename(f):38}   0')

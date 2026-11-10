import shutil
p = 'assets/css/app.css'
shutil.copyfile(p, 'scratch/app.css.state2.bak')
src = open(p, encoding='utf-8').read()
lines = src.split('\n')
start = None
for i, l in enumerate(lines):
    if 'MASTER RESPONSIVE SIDEBAR DRAWER' in l:
        start = i - 1
        assert lines[start].strip().startswith('/*'), repr(lines[start])
        break
j = None
for i, l in enumerate(lines):
    if 'html body #sidebar .sidebar-close-btn,' in l:
        j = i
assert j is not None and j > start
closes = 0
end = None
for k in range(j, len(lines)):
    if lines[k].rstrip() == '}':
        closes += 1
        if closes == 2:
            end = k
            break
assert end is not None
region = '\n'.join(lines[start:end + 1])
assert '.sidebar-close-btn' in region and '.sidebar {' in region
del lines[start:end + 1]
open(p, 'w', encoding='utf-8', newline='\n').write('\n'.join(lines))
print('removed', end - start + 1, 'lines; new total', len(lines))

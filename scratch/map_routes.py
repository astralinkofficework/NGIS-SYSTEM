import io, re

src = io.open('server.py', encoding='utf-8').read()
routes = re.findall(r"@app\.route\('([^']+)'(?:,\s*methods=(\[[^\]]*\]))?\)", src)
keys = ('academic', 'oversight', 'request', 'submission', 'document', 'certificate',
        'transcript', 'lost', 'audit', 'behavior', 'approval', 'publish', 'grade')
out = io.open('scratch/route_map.txt', 'w', encoding='utf-8')
for path, methods in routes:
    if any(k in path.lower() for k in keys):
        out.write(f'{path}  {methods}\n')
out.write('---ALL ROUTES---\n')
for path, methods in routes:
    out.write(f'{path}  {methods}\n')
out.close()
print('done', len(routes))

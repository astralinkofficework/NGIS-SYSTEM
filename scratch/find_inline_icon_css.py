import glob, re
pages = sorted(glob.glob('pages/**/*.html', recursive=True)) + ['index.html']
hits = []
for p in pages:
    s = open(p, encoding='utf-8').read()
    # inline CSS rules targeting data-ngis-icon or action-icon classes inside <style>
    for blk in re.findall(r'<style[^>]*>(.*?)</style>', s, re.S):
        for rule in re.finditer(r'([^{}]*data-ngis-icon[^{}]*|[^{}]*\.action-icon-btn[^{}]*|[^{}]*\.action-group[^{}]*|[^{}]*\.icon-btn[^{}]*)\{([^{}]*)\}', blk):
            sel = re.sub(r'\s+', ' ', rule.group(1)).strip()
            body = re.sub(r'\s+', ' ', rule.group(2)).strip()
            if 'data-ngis-icon' in sel or 'action' in sel or 'icon-btn' in sel:
                hits.append((p, sel[:60], body[:90]))
from collections import Counter
c = Counter(h[1] for h in hits)
print('distinct inline selectors touching icon system:', len(c))
for sel, n in c.most_common(30):
    print('%3d  %s' % (n, sel))
print('\nsample full rules:')
for h in hits[:20]:
    print(' ', h[0], '::', h[1], '{', h[2], '}')

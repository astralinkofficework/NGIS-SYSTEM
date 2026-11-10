import glob, re
pages = sorted(glob.glob('pages/**/*.html', recursive=True)) + ['index.html']
# a button/anchor with an action-ish class OR action onclick, containing a material/phosphor glyph
btn_re = re.compile(
    r'<(button|a)\b[^>]*?(?:class="[^"]*(?:action-icon|icon-btn|row-action|table-action|kebab|btn-(?:danger|ghost|soft|primary|sm))[^"]*"|onclick="[^"]*(?:edit|delete|view|export|download|print|close|approve|reject|toggle)[^"]*")[^>]*>(?:(?!</(?:button|a)>).)*?'
    r'<(?:span|i)\b[^>]*class="[^"]*(?:material-symbols(?:-outlined)?|ph(?:-\w+)? ph-[\w-]+)[^"]*"[^>]*>\s*([A-Za-z0-9_ -]+)\s*</(?:span|i)>'
    r'(?:(?!</(?:button|a)>).)*?</\1>', re.I | re.S)
for p in pages:
    s = open(p, encoding='utf-8').read()
    for m in btn_re.finditer(s):
        glyph = m.group(2).strip()
        snippet = re.sub(r'\s+', ' ', m.group(0))[:180]
        print('%-44s glyph=%-16s | %s' % (p, glyph, snippet))

import sys, re
p = sys.argv[1] if len(sys.argv) > 1 else 'pages/shared/exams.html'
s = open(p, encoding='utf-8').read()
mi = s.find('<!-- NGIS global action-icon engine -->')
print('file:', p)
print('marker at char', mi, 'line', s[:mi].count(chr(10)) + 1)
# context around marker
ctx = s[mi-400:mi+200]
print('---- around injected marker ----')
print(ctx)
print('=====================================')
# how many </head>, </script>, </body> and their line numbers
for tok in ['</head>', '<script', '</script>', '</body>']:
    idxs = [m.start() for m in re.finditer(re.escape(tok), s)]
    lines = [s[:i].count(chr(10)) + 1 for i in idxs]
    print('%-12s count=%d lines=%s' % (tok, len(idxs), lines[:12]))
# is marker before or after last </script>?
last_script_close = s.rfind('</script>')
print('marker < last </script>?', mi < last_script_close)

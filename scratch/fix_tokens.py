with open('assets/css/design-tokens.css', 'r', encoding='utf-8') as f:
    c = f.read()

target = """  /* ── 2. Typography System (NO BOLD: Max 500) ──────────────── */
  --token-font-family: 'Manrope', system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
  --token-font-khmer:  'Kantumruy Pro', 'Manrope', sans-serif;
  --token-font-mono:   'JetBrains Mono', ui-monospace, SFMono-Regular, monospace;

  /* Strict Two Weights: 400 (regular) and 500 (medium) */
  --token-weight-normal: 400;
  --token-weight-medium: 500;"""

replacement = """  /* ── 2. Typography System (Strict Google Fonts Suite) ─────── */
  --token-font-family: 'Manrope', 'Plus Jakarta Sans', 'Inter', system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
  --token-font-khmer:  'Kantumruy Pro', 'Manrope', sans-serif;
  --token-font-ui:     'Plus Jakarta Sans', 'Inter', 'Manrope', sans-serif;
  --token-font-supporting: 'Inter', 'Plus Jakarta Sans', 'Manrope', sans-serif;
  --token-font-mono:   ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;

  /* Weights: Regular (400) & Medium (500) for normal content; 600/700 for titles */
  --token-weight-light:  300;
  --token-weight-normal: 400;
  --token-weight-medium: 500;
  --token-weight-semibold: 600;
  --token-weight-bold:   700;

  /* Primary Button Tokens (Burgundy #92243D with White #FFFFFF text) */
  --token-btn-primary-bg:           #92243D;
  --token-btn-primary-color:        #FFFFFF;
  --token-btn-primary-border:       #92243D;
  --token-btn-primary-hover-bg:     #7A1D32;
  --token-btn-primary-hover-border: #7A1D32;
  --token-btn-primary-active-bg:    #631728;"""

target_crlf = target.replace('\r\n', '\n').replace('\n', '\r\n')
replacement_crlf = replacement.replace('\r\n', '\n').replace('\n', '\r\n')

if target in c:
    c = c.replace(target, replacement)
    print('Replaced in design-tokens.css (LF)')
elif target_crlf in c:
    c = c.replace(target_crlf, replacement_crlf)
    print('Replaced in design-tokens.css (CRLF)')
else:
    print('Target not found in design-tokens.css')

with open('assets/css/design-tokens.css', 'w', encoding='utf-8') as f:
    f.write(c)


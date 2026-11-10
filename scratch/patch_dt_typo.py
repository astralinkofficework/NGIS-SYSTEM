with open('assets/css/design-tokens.css', 'r', encoding='utf-8') as f:
    text = f.read()

old_section = """  /* ── 2. Typography System (Strict Google Fonts Suite) ─────── */
  --token-font-family: 'Manrope', 'Plus Jakarta Sans', 'Inter', system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
  --token-font-khmer:  'Kantumruy Pro', 'Manrope', sans-serif;
  --token-font-ui:     'Plus Jakarta Sans', 'Inter', 'Manrope', sans-serif;
  --token-font-supporting: 'Inter', 'Plus Jakarta Sans', 'Manrope', sans-serif;
  --token-font-mono:   ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;

  /* Weights: Regular (400) & Medium (500) per AGENTS.md */
  --token-weight-light:  300;
  --token-weight-normal: 400;
  --token-weight-medium: 500;
  --token-weight-semibold: 500;
  --token-weight-bold:   500;"""

new_section = """  /* ── 2. Global Typography System (Manrope + Plus Jakarta Sans) ── */
  --font-heading: 'Manrope', sans-serif;
  --font-body:    'Plus Jakarta Sans', sans-serif;
  --font-primary: 'Plus Jakarta Sans', sans-serif;

  --font-size-h1: 28px;
  --font-size-h2: 22px;
  --font-size-h3: 18px;
  --font-size-h4: 16px;

  --font-size-body:  14px;
  --font-size-small: 13px;
  --font-size-label: 12px;

  --token-font-family:     'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
  --token-font-heading:    'Manrope', sans-serif;
  --token-font-body:       'Plus Jakarta Sans', sans-serif;
  --token-font-ui:         'Plus Jakarta Sans', sans-serif;
  --token-font-supporting: 'Plus Jakarta Sans', sans-serif;
  --token-font-khmer:      'Kantumruy Pro', 'Plus Jakarta Sans', sans-serif;
  --token-font-mono:       ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;

  /* Approved Weights: Normal (400), Medium (500), Semi-bold (600) */
  --token-weight-light:    400;
  --token-weight-normal:   400;
  --token-weight-medium:   500;
  --token-weight-semibold: 600;
  --token-weight-bold:     600;

  /* Line Heights */
  --lh-h1: 1.25;
  --lh-h2: 1.30;
  --lh-h3: 1.35;
  --lh-h4: 1.40;
  --lh-body: 1.50;"""

if old_section in text:
    text = text.replace(old_section, new_section)
    with open('assets/css/design-tokens.css', 'w', encoding='utf-8') as f:
        f.write(text)
    print('Updated design-tokens.css typography successfully.')
else:
    print('Old section not found!')


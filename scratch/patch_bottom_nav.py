with open('assets/css/bottom-nav.css', 'r', encoding='utf-8') as f:
    bn = f.read().replace('\r\n', '\n')

old_glow = '''  .mob-bn-glow {
    position: absolute;
    inset: 6px 14px -8px 14px;
    border-radius: 999px;
    background: linear-gradient(90deg, rgba(19,130,155,0.18), rgba(184,219,217,0.28), rgba(19,130,155,0.18));
    filter: blur(18px);
    opacity: 0.7;
    pointer-events: none;
    z-index: -1;
  }'''

new_glow = '''  .mob-bn-glow {
    display: none !important; /* Rule V4: Removed gratuitous blurred glow gradient */
  }'''

if old_glow in bn:
    bn = bn.replace(old_glow, new_glow)
    print("bottom-nav.css glow updated")
else:
    print("old_glow not found")

old_slider = '''  .mob-bn-slider {
    position: absolute;
    top: 4px;
    height: 44px;
    left: 0;
    border-radius: 999px;
    background: linear-gradient(135deg, rgba(19,130,155,0.12), rgba(184,219,217,0.22));
    border: 1px solid rgba(19,130,155,0.14);
    box-shadow: inset 0 1px 1px 0 rgba(255,255,255,0.85);
    pointer-events: none;
    z-index: 1;
  }'''

new_slider = '''  .mob-bn-slider {
    position: absolute;
    top: 4px;
    height: 44px;
    left: 0;
    border-radius: 999px;
    background: #F3F3F5 !important;
    border: 1px solid #E5E5E8 !important;
    box-shadow: none !important;
    pointer-events: none;
    z-index: 1;
  }'''

if old_slider in bn:
    bn = bn.replace(old_slider, new_slider)
    print("bottom-nav.css slider updated")
else:
    print("old_slider not found")

with open('assets/css/bottom-nav.css', 'w', encoding='utf-8', newline='\n') as f:
    f.write(bn)

# Also update app.css
with open('assets/css/app.css', 'r', encoding='utf-8') as f:
    app = f.read().replace('\r\n', '\n')

if old_glow in app:
    app = app.replace(old_glow, new_glow)
    print("app.css glow updated")
if old_slider in app:
    app = app.replace(old_slider, new_slider)
    print("app.css slider updated")

with open('assets/css/app.css', 'w', encoding='utf-8', newline='\n') as f:
    f.write(app)

print("Finished updating bottom-nav styles")


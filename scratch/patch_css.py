with open('assets/css/design-system.css', 'r', encoding='utf-8') as f:
    ds = f.read().replace('\r\n', '\n')

old_ds = '''/* Page titles and section headings allowed 600 or 700 */
h1, .page-title, .dash-hero-title, [data-purpose="page-title"], .masthead-title {
  font-family: 'Manrope', 'Plus Jakarta Sans', sans-serif !important;
  font-weight: 600;
}

h2, h3, .section-title, [data-purpose="section-title"] {
  font-family: 'Manrope', 'Plus Jakarta Sans', sans-serif !important;
  font-weight: 600;
}'''

new_ds = '''/* Page titles and section headings standard 500 (NO BOLD FONTS per AGENTS.md) */
h1, .page-title, .dash-hero-title, [data-purpose="page-title"], .masthead-title {
  font-family: 'Manrope', 'Plus Jakarta Sans', sans-serif !important;
  font-weight: 500;
}

h2, h3, .section-title, [data-purpose="section-title"] {
  font-family: 'Manrope', 'Plus Jakarta Sans', sans-serif !important;
  font-weight: 500;
}'''

if old_ds in ds:
    ds = ds.replace(old_ds, new_ds)
    with open('assets/css/design-system.css', 'w', encoding='utf-8', newline='\n') as f:
        f.write(ds)
    print("design-system.css updated (weights 600 -> 500)")
else:
    print("old_ds NOT found")

with open('assets/css/interactions.css', 'r', encoding='utf-8') as f:
    inter = f.read().replace('\r\n', '\n')

old_inter = ''') :not(:disabled):not(.disabled):not([aria-disabled="true"]):active {
  translate: none !important;
  scale: 1 !important;
}'''

# Also try without the space before colon
old_inter2 = '''):not(:disabled):not(.disabled):not([aria-disabled="true"]):active {
  translate: none !important;
  scale: 1 !important;
}'''

new_inter = '''):not(:disabled):not(.disabled):not([aria-disabled="true"]):active {
  transform: scale(0.98) !important;
  opacity: 0.9 !important;
  transition: transform 60ms ease, opacity 60ms ease !important;
}'''

if old_inter in inter:
    inter = inter.replace(old_inter, new_inter)
    with open('assets/css/interactions.css', 'w', encoding='utf-8', newline='\n') as f:
        f.write(inter)
    print("interactions.css updated (:active scale 0.98)")
elif old_inter2 in inter:
    inter = inter.replace(old_inter2, new_inter)
    with open('assets/css/interactions.css', 'w', encoding='utf-8', newline='\n') as f:
        f.write(inter)
    print("interactions.css updated (inter2)")
else:
    print("old_inter NOT found")


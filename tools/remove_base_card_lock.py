with open('assets/css/ui-cleanup.css', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace the base card lockdown lines
old_base_props = """  filter: none !important;
  text-shadow: none !important;
  transition: none !important;
  transform: none !important;
  translate: none !important;
  scale: 1 !important;"""

new_base_props = """  filter: none !important;
  text-shadow: none !important;"""

if old_base_props in text:
    text = text.replace(old_base_props, new_base_props, 1)
    print("Removed transform/scale/transition lockdown from base card rule in ui-cleanup.css")
else:
    print("old_base_props not found in ui-cleanup.css")

with open('assets/css/ui-cleanup.css', 'w', encoding='utf-8') as f:
    f.write(text)

print("Saved assets/css/ui-cleanup.css successfully!")

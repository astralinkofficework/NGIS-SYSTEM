import re

path = "pages/principal/principal-classes.html"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# Check for font-bold, font-semibold, 700, 800
bolds = re.findall(r'(?:font-bold|font-semibold|font-extrabold|font-black|font-weight:\s*[678]00|fontWeight:\s*[\'"][678]00[\'"])', content)
print(f"Bolds found in principal-classes.html: {len(bolds)}")
for b in bolds:
    print("  ", b)

# Check for hamburger button
has_hamb = 'data-action="toggle-sidebar"' in content
print(f"Has hamburger button: {has_hamb}")


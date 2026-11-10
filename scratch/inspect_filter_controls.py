with open("pages/principal/principal-departments.html", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if "filtering-controls" in l:
        print("".join(lines[i-1:i+45]))
        break


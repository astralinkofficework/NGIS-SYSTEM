import re

path = "assets/css/shared-components.css"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# Replace old hexes with the new palette
content = content.replace("#F3F3F5", "#EAF6FF")
content = content.replace("#202F63", "#052659")
content = content.replace("#92243D", "#052659")
content = content.replace("#E5E5E8", "#DCE8F3")
content = content.replace("#1E4D38", "#052659")
content = content.replace("#18234D", "#021024")
content = content.replace("#7A1D32", "#021024")
content = content.replace("#7E1E34", "#021024")

with open(path, "w", encoding="utf-8") as f:
    f.write(content)

print("Updated assets/css/shared-components.css successfully!")


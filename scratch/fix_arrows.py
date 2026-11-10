import re

path = "pages/principal/principal-classes.html"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# In filtering-controls, remove the duplicate expand_more spans and keep the crisp @tailwindcss/forms chevron
pattern = r'(<select id="(?:gradeFilter|campusFilter|statusFilter)"[^>]*>.*?</select>)\s*<span class="material-symbols-outlined[^>]*>expand_more</span>'
content = re.sub(pattern, r'\1', content, flags=re.DOTALL)

with open(path, "w", encoding="utf-8") as f:
    f.write(content)

print("Cleaned duplicate arrows in principal-classes.html")


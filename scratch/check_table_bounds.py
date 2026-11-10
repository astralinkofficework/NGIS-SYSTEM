with open(r'c:\Users\oudom\OneDrive\Desktop\NGIS-SYSTEM\assets\js\ngis-profiles.js', 'r', encoding='utf-8') as f:
    text = f.read()

idx_start = text.find("  function renderTable() {")
idx_end = text.find("  function renderPager() {")

print("renderTable start:", idx_start, "end:", idx_end)
print(text[idx_start:idx_start+200])


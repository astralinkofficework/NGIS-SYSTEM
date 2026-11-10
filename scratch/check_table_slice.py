with open(r'c:\Users\oudom\OneDrive\Desktop\NGIS-SYSTEM\assets\js\ngis-profiles.js', 'r', encoding='utf-8') as f:
    text = f.read()

idx_start = text.find("  function renderTable() {")
idx_end = text.find("  function renderPager() {")

print(f"renderTable to renderPager length: {idx_end - idx_start}")
print(text[idx_start:idx_start+250])
print("...")
print(text[idx_end-250:idx_end])


profiles_path = r'c:\Users\oudom\OneDrive\Desktop\NGIS-SYSTEM\assets\js\ngis-profiles.js'

with open(profiles_path, 'r', encoding='utf-8') as f:
    text = f.read()

idx_start = text.find("  function mountModals() {")
idx_end = text.find("  function boot() {")

print("mountModals start:", idx_start, "end:", idx_end)
print(text[idx_start:idx_start+300])
print("...")
print(text[idx_end-200:idx_end])


with open("assets/js/system-management.js", "r", encoding="utf-8") as f:
    text = f.read()

print("File length:", len(text))
print("First 100 lines:")
print('\n'.join(text.splitlines()[:100]))


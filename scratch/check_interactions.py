with open('assets/css/interactions.css', 'r', encoding='utf-8') as f:
    text = f.read()

print("interactions.css length:", len(text))
print("First 100 lines:")
for l in text.splitlines()[:100]:
    print(l)


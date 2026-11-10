with open('academic_store.py', 'r', encoding='utf-8') as f:
    text = f.read()

print("academic_store.py length:", len(text))
print("First 80 lines:")
print('\n'.join(text.splitlines()[:80]))


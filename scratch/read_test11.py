with open('tests/test_khmer_suite.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()
for i, line in enumerate(lines[314:330]):
    print(f"{i+315}: {line.strip()}")


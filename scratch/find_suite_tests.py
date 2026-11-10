with open('tests/test_khmer_suite.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()
for i, line in enumerate(lines):
    if line.strip().startswith('def test_'):
        print(f"{i+1}: {line.strip()}")


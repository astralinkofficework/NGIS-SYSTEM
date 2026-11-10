with open('server.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()
print(f"Total lines: {len(lines)}")
print("End of server.py:")
print(''.join(lines[-40:]))


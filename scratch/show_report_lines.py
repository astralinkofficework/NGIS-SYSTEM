with open(r'C:\Users\oudom\.gemini\antigravity\brain\c3bf1c11-3155-48a6-b3ee-4e74d6713af7\VISUAL_TIMETABLE_SCHEDULER_REPORT.md', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(35, 55):
    if i < len(lines):
        print(f'{i+1}: {repr(lines[i])}')


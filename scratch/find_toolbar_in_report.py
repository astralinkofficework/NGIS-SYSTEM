with open(r'C:\Users\oudom\.gemini\antigravity\brain\c3bf1c11-3155-48a6-b3ee-4e74d6713af7\VISUAL_TIMETABLE_SCHEDULER_REPORT.md', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('Top toolbar controls')
if pos != -1:
    print(text[pos-20:pos+300])


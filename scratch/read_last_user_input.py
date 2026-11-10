import json

with open(r'C:\Users\oudom\.gemini\antigravity\brain\c3bf1c11-3155-48a6-b3ee-4e74d6713af7\.system_generated\logs\transcript.jsonl', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(len(lines)-1, -1, -1):
    data = json.loads(lines[i])
    if data.get('type') == 'USER_INPUT':
        print(f"Last USER_INPUT index={i}, step_index={data.get('step_index')}")
        print("Content:")
        print(data.get('content'))
        print("Media:")
        print(data.get('media'))
        break


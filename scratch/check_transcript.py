import json

with open(r'C:\Users\oudom\.gemini\antigravity-ide\brain\59282cff-0290-49eb-9c4b-245deb1bb4a6\.system_generated\logs\transcript.jsonl', 'r', encoding='utf-8') as f:
    lines = f.readlines()

d = json.loads(lines[431])
print('Step 431 tool call:')
print(json.dumps(d.get('tool_calls'), indent=2))

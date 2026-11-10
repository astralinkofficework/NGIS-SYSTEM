import json
path = r'C:\Users\oudom\.gemini\antigravity\brain\c3bf1c11-3155-48a6-b3ee-4e74d6713af7\.system_generated\logs\transcript_full.jsonl'
with open(path, 'r', encoding='utf-8') as f:
    for line in f:
        data = json.loads(line)
        if data.get('step_index') in (5378, 5379, 5380, 5381, 5382, 5383):
            print(f"Step {data.get('step_index')} [{data.get('type')}]: {data.get('content')[:300]}")


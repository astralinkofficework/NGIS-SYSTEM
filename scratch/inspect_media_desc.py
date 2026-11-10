import json
path = r'C:\Users\oudom\.gemini\antigravity\brain\c3bf1c11-3155-48a6-b3ee-4e74d6713af7\.system_generated\logs\transcript_full.jsonl'
with open(path, 'r', encoding='utf-8') as f:
    for line in f:
        data = json.loads(line)
        idx = data.get('step_index')
        if idx in (5379, 5383, 5384):
            print(f"--- Step {idx} ---")
            print((data.get('content') or data.get('thinking') or '')[:800])


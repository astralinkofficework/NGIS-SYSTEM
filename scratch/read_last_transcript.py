import json

with open(r'C:\Users\oudom\.gemini\antigravity\brain\c3bf1c11-3155-48a6-b3ee-4e74d6713af7\.system_generated\logs\transcript.jsonl', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(f"Total lines: {len(lines)}")
for i, line in enumerate(lines[-5:]):
    data = json.loads(line)
    print(f"Line {len(lines)-5+i}: type={data.get('type')}, source={data.get('source')}, step_index={data.get('step_index')}")
    if 'content' in data:
        content_preview = str(data['content'])[:300]
        print(f"   content: {content_preview}")
    if 'media' in data:
        print(f"   media: {data['media']}")


import json

target_step = None
last_content = None

with open('C:/Users/oudom/.gemini/antigravity/brain/f0e0db56-cd04-4f51-a7f8-40ba21b43536/.system_generated/logs/transcript_full.jsonl', 'r', encoding='utf-8') as f:
    for line in f:
        obj = json.loads(line)
        for tc in obj.get('tool_calls', []):
            if 'admin-security.html' in str(tc.get('args', {})):
                step = obj.get('step_index')
                name = tc.get('name')
                print(f"Found {name} at step {step}")
                if name == 'write_file' and 'admin-security.html' in tc.get('args', {}).get('Path', ''):
                    target_step = step
                    last_content = tc['args']['Content']

if last_content:
    print(f"Writing content from step {target_step}, len: {len(last_content)}")
    with open('pages/admin/admin-security.html', 'w', encoding='utf-8') as out:
        out.write(last_content)

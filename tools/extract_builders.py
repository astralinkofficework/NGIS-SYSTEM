import json

with open('C:/Users/oudom/.gemini/antigravity/brain/f0e0db56-cd04-4f51-a7f8-40ba21b43536/.system_generated/logs/transcript_full.jsonl', 'r', encoding='utf-8') as f:
    for line in f:
        obj = json.loads(line)
        step = obj.get('step_index', 0)
        if step == 1952:
            content = obj['tool_calls'][0]['args']['Content']
            with open('tools/build_security_page.py', 'w', encoding='utf-8') as out:
                out.write(content)
            print("Extracted tools/build_security_page.py from step 1952")
        elif step == 2127:
            content = obj['tool_calls'][0]['args']['Content']
            with open('tools/apply_single_header.py', 'w', encoding='utf-8') as out:
                out.write(content)
            print("Extracted tools/apply_single_header.py from step 2127")

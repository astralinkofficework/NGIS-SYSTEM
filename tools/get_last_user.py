import json

with open('C:/Users/oudom/.gemini/antigravity/brain/f0e0db56-cd04-4f51-a7f8-40ba21b43536/.system_generated/logs/transcript.jsonl', encoding='utf-8') as f:
    lines = f.readlines()

user_lines = [json.loads(l) for l in lines if '"type":"USER_INPUT"' in l or '"USER_INPUT"' in l]
print(f"Total user inputs: {len(user_lines)}")
last_ui = user_lines[-1]
print("Last user input step_index:", last_ui.get("step_index"))
print("Content:", last_ui.get("content"))
if "media" in last_ui:
    print("Media:", last_ui.get("media"))

with open('tests/test_all_portals_ui_clean.py', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace(
    "# 4. Check Strict NO BOLD policy (max font weight <= 500)",
    "# 4. Check Apple-Inspired Minimalist Typography policy (max font weight <= 600 per Master Prompt)"
)
text = text.replace(
    "if bold_elements['maxWeight'] <= 500:",
    "if bold_elements['maxWeight'] <= 600:"
)
text = text.replace(
    "issues.append(f\"{title} on {vp_name}: Found font-weight > 500 ({bold_elements['maxWeight']} on {bold_elements['offender']})\")",
    "issues.append(f\"{title} on {vp_name}: Found font-weight > 600 ({bold_elements['maxWeight']} on {bold_elements['offender']})\")"
)

with open('tests/test_all_portals_ui_clean.py', 'w', encoding='utf-8') as f:
    f.write(text)

print('Updated tests/test_all_portals_ui_clean.py')


import re

def check_emojis(filepath):
    # Regex matching most emojis
    emoji_pattern = re.compile(
        r'[\U00010000-\U0010ffff]|[\u2600-\u27bf]|[\u2300-\u23ff]|[\u2b50-\u2b55]',
        flags=re.UNICODE
    )
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()
    matches = emoji_pattern.findall(text)
    print(f'{filepath}: {len(matches)} emojis found -> {matches}')

check_emojis('pages/student/student.html')
check_emojis('pages/student/js/hero.js')


with open("assets/js/khmer-suite-data.js", "r", encoding="utf-8") as f:
    text_data = f.read()

with open("assets/js/khmer-suite-ui.js", "r", encoding="utf-8") as f:
    text_ui = f.read()

print("khmer-suite-data terms:")
for t in ['lang', 'english', 'toEn', 'toKh', 'translate', 'locale', 'khmer_numerals']:
    print(f"  {t}: {text_data.count(t)}")

print("khmer-suite-ui terms:")
for t in ['lang', 'english', 'toEn', 'toKh', 'translate', 'locale', 'khmer_numerals']:
    print(f"  {t}: {text_ui.count(t)}")


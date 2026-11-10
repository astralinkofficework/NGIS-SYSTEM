with open(r"assets/js/khmer-suite-ui.js", "r", encoding="utf-8") as f:
    text = f.read()

idx = 0
while True:
    idx = text.find("distribute-all", idx)
    if idx == -1:
        break
    print("Found 'distribute-all' at index:", idx)
    print(text[idx-200:idx+300])
    print("="*60)
    idx += len("distribute-all")


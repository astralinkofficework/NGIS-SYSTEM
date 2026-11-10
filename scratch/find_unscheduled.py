with open(r"assets/js/khmer-suite-ui.js", "r", encoding="utf-8") as f:
    text = f.read()

idx = 0
while True:
    idx = text.find("Unscheduled Classes", idx)
    if idx == -1:
        break
    print("Found at index:", idx)
    print(text[idx-150:idx+350])
    print("="*60)
    idx += len("Unscheduled Classes")


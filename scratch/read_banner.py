with open(r"assets/css/khmer-suite.css", "r", encoding="utf-8") as f:
    text = f.read()

idx = text.find(".ks-workflow-bar")
print(text[idx:idx+350])

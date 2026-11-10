with open(r"assets/js/khmer-suite-ui.js", "r", encoding="utf-8") as f:
    text = f.read()

idx = text.find("Build weekly class")
print("Found in khmer-suite-ui.js:", idx)
if idx != -1:
    print(text[idx-100:idx+200])

import glob
for fn in glob.glob("pages/**/*.html", recursive=True):
    with open(fn, "r", encoding="utf-8") as f:
        c = f.read()
    if "Build weekly class" in c:
        print("Found in", fn)


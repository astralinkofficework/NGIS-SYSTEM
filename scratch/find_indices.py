with open(r"assets/js/khmer-suite-ui.js", "r", encoding="utf-8") as f:
    text = f.read()

idx_viewmode = text.find("case 'set-view-mode':")
idx_subadd = text.find("case 'subject-add':")
print("Builder onClick start:", idx_viewmode)
print("Builder onClick end:", idx_subadd)
print(text[idx_viewmode:idx_viewmode+400])


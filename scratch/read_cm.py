with open(r"assets/js/khmer-suite-ui.js", "r", encoding="utf-8") as f:
    text = f.read()

idx = text.find("function classMasterModernHtml(")
idx_ret = text.find("return '<div class=\"grid grid-cols-1 xl:grid-cols-4 gap-4\">", idx)
print(text[idx_ret:idx_ret+1200])

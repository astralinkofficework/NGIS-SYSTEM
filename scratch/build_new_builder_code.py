import re

# Read current khmer-suite-ui.js
with open(r"assets/js/khmer-suite-ui.js", "r", encoding="utf-8") as f:
    content = f.read()

print("Original content length:", len(content))


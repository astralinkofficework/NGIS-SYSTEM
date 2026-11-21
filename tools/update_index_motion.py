with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Update portal-card:hover
old_hover = ".portal-card:hover { background:#ffffff !important; border-color:#176B45 !important; transform:none !important; box-shadow:0 2px 8px rgba(23,107,69,0.06) !important; }"
new_hover = """@media (hover: hover) and (pointer: fine) {
  .portal-card:hover {
    background: #ffffff !important;
    border-color: #176B45 !important;
    transform: translateY(-2.5px) scale(1.007) !important;
    box-shadow: 0 8px 24px -4px rgba(15, 23, 20, 0.08), 0 2px 6px -2px rgba(15, 23, 20, 0.04) !important;
    transition: transform 180ms cubic-bezier(0.16, 1, 0.3, 1), box-shadow 180ms cubic-bezier(0.16, 1, 0.3, 1), border-color 180ms ease !important;
  }
}"""

if old_hover in text:
    text = text.replace(old_hover, new_hover, 1)
    print("Updated .portal-card:hover in index.html")
else:
    print("old_hover not found in index.html")

# Add motion.js script before </body>
script_tag = '<script src="assets/js/motion.js"></script>'
if script_tag not in text:
    target = '<script src="assets/components/ngis-ui-kit.js"></script>'
    if target in text:
        text = text.replace(target, target + '\n' + script_tag, 1)
        print("Added motion.js script to index.html")
    else:
        print("ngis-ui-kit.js target not found in index.html")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Saved index.html successfully!")

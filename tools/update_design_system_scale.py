with open('assets/css/design-system.css', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace("transform: translateY(8px) scale(0.98) !important;", "transform: translateY(8px) scale(0.97) !important;")
text = text.replace("transform: translateY(6px) scale(0.985) !important;", "transform: translateY(6px) scale(0.97) !important;")

with open('assets/css/design-system.css', 'w', encoding='utf-8') as f:
    f.write(text)

print("Updated design-system.css modal entrance/exit scale to 0.97!")

from PIL import Image

for name in ["dept_cards_after", "classes_cards_after", "principal_cards_after"]:
    img = Image.open(f"scratch/{name}.png")
    # crop roughly y=80 to y=340
    w, h = img.size
    crop_img = img.crop((0, 70, w, 320))
    crop_img.save(f"scratch/{name}_crop.png")
    crop_img.save(f"C:/Users/oudom/.gemini/antigravity/brain/8fd19b10-a09a-43d8-a122-cb4a75dc0ff6/{name}_crop.png")
    print(f"Saved {name}_crop.png")


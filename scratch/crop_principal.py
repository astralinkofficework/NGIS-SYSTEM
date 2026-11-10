from PIL import Image

img = Image.open("scratch/principal_cards_after.png")
# let's crop around y=400 to y=650
w, h = img.size
crop_img = img.crop((0, 400, w, min(700, h)))
crop_img.save("C:/Users/oudom/.gemini/antigravity/brain/8fd19b10-a09a-43d8-a122-cb4a75dc0ff6/principal_cards_after_crop.png")
print("Saved principal_cards_after_crop.png")


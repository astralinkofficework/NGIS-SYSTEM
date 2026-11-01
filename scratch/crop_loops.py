from PIL import Image

img = Image.open('C:/Users/oudom/.gemini/antigravity/brain/c1474b77-901e-4dd2-adfd-07d8d29f0999/.user_uploaded/media_1793525557001_c608a9ac.jpg')
w, h = img.size
print(f"Image size: {w}x{h}")

# Upcoming card is in the center, Deadlines on the right
# Crop around Upcoming header and Deadlines
crop_upcoming = img.crop((int(w * 0.25), int(h * 0.3), int(w * 0.72), int(h * 0.55)))
crop_upcoming.save('scratch/crop_upcoming.png')

crop_deadlines = img.crop((int(w * 0.70), int(h * 0.3), int(w * 0.92), int(h * 0.8)))
crop_deadlines.save('scratch/crop_deadlines.png')

print("Cropped successfully!")


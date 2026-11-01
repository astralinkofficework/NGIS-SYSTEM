from PIL import Image

img = Image.open('C:/Users/oudom/.gemini/antigravity/brain/c1474b77-901e-4dd2-adfd-07d8d29f0999/.user_uploaded/media_1793522800957_a2fd55d2.jpg')
w, h = img.size

# Upcoming card is in the center, Deadlines on the right
crop_upcoming = img.crop((int(w * 0.23), int(h * 0.28), int(w * 0.76), int(h * 0.77)))
crop_upcoming.save('scratch/ref_upcoming.png')

crop_deadlines = img.crop((int(w * 0.76), int(h * 0.28), int(w * 0.98), int(h * 0.93)))
crop_deadlines.save('scratch/ref_deadlines.png')

print("Reference cropped successfully!")


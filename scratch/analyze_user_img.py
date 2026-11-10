from PIL import Image

im = Image.open('C:/Users/oudom/.gemini/antigravity/brain/c3bf1c11-3155-48a6-b3ee-4e74d6713af7/.user_uploaded/media_1794221447158_029eeb05.jpg')
w, h = im.size
print('Width:', w, 'Height:', h)

# Let's inspect the bottom of the image
# What color are pixels at the bottom?
bottom_strip = im.crop((0, h-30, w, h))
bottom_strip.save('scratch/user_bottom_strip.png')

# What color are the card borders?
# The card borders at x=10, y=50
print('Pixel at (10, 50):', im.getpixel((10, 50)))
print('Pixel at (250, 50):', im.getpixel((250, 50)))
print('Pixel at (500, 50):', im.getpixel((500, 50)))
print('Pixel at (10, h-5):', im.getpixel((10, h-5)))
print('Pixel at (w//2, h-5):', im.getpixel((w//2, h-5)))


import os
from PIL import Image

img_path = 'C:/Users/oudom/.gemini/antigravity/brain/c3bf1c11-3155-48a6-b3ee-4e74d6713af7/.user_uploaded/media_1794221447158_029eeb05.jpg'
im = Image.open(img_path)
print('Image format:', im.format, 'size:', im.size)

from PIL import Image

im = Image.open('scratch/assignment_3_cols_crop.png')
print('Size of crop:', im.size)
# Check pixels at corners of the cards to verify rounded corners
# Column 1 starts near x=0, Column 2 starts near x=im.size[0]*0.25, Column 3 starts near x=im.size[0]*0.75
print('Pixel at (5, 5):', im.getpixel((5, 5)))
print('Pixel at (50, 50):', im.getpixel((50, 50)))


from PIL import Image

im = Image.open('scratch/teacher_test.png')
# Crop around y=400 to 650, x=300 to 1260
crop = im.crop((300, 450, 1260, 650))
crop.save('scratch/banner_overlap_check.png')
print('Saved scratch/banner_overlap_check.png')


import os
from PIL import Image

fpath = 'scratch/teacher_test.png'
print('teacher_test.png exists:', os.path.exists(fpath))
if os.path.exists(fpath):
    im = Image.open(fpath)
    print('Size:', im.size)
    # Save a crop of the top cards and banner
    crop = im.crop((0, 0, im.width, min(im.height, 700)))
    crop.save('scratch/teacher_test_top.png')
    print('Saved scratch/teacher_test_top.png')


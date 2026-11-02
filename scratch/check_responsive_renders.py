import os
from PIL import Image

for fpath in ['scratch/teacher_tablet_850.png', 'scratch/teacher_mobile_390_new.png']:
    print(fpath, 'exists:', os.path.exists(fpath))
    if os.path.exists(fpath):
        im = Image.open(fpath)
        print('  Size:', im.size)


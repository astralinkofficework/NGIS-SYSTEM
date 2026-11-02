from PIL import Image
import numpy as np

im = Image.open('scratch/teacher_test.png')
arr = np.array(im)

# Let's inspect along y from 400 to 700 at x=750 (middle of upcoming card):
for y in range(450, 600, 10):
    val = arr[y, 750, :3]
    # Check whether it's inside Upcoming card or Banner or page background
    if np.all(val > 240):
        desc = 'WHITE (Card)'
    elif val[0] < 70 and val[2] > 70:
        desc = 'TEAL/BLUE (Banner)'
    else:
        desc = f'OTHER RGB {val.tolist()}'
    print(f'y={y}: {desc}')


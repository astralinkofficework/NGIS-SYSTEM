from PIL import Image
import numpy as np

im = Image.open('scratch/upcoming_card_rendered.png')
arr = np.array(im)

# Let's inspect the bottom 50 pixels (y from 320 to 370 in crop):
# In the original problem, the bottom 150px was a completely empty white void.
# Let's check where the content ends in the 3 columns of upcoming_card_rendered:
# Column 1 (Classes Today): x from 20 to 120
# Column 2 (Grading Queue): x from 140 to 240
# Column 3 (Activity Feed): x from 260 to 380

for col_name, (x1, x2) in [('Classes Today', (20, 120)), ('Grading Queue', (140, 240)), ('Activity Feed', (260, 380))]:
    # Find lowest y where text/content exists (non-white pixel):
    sub = arr[:, x1:x2, :3]
    # non-white pixels: mean < 235
    non_white_y = [y for y in range(sub.shape[0]) if np.any(np.mean(sub[y], axis=1) < 235)]
    if non_white_y:
        print(f'{col_name}: lowest content at y = {max(non_white_y)} / total height {im.height} (gap to bottom: {im.height - max(non_white_y)}px)')


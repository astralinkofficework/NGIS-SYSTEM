from PIL import Image
import numpy as np

im = Image.open('scratch/teacher_test.png')
arr = np.array(im)

# Let's inspect the cards:
# Profile: x from 305 to 540
# Upcoming: x from 560 to 950
# Deadlines: x from 970 to 1250

# Let's check card tops and bottoms:
for name, x in [('Profile', 400), ('Upcoming', 750), ('Deadlines', 1100)]:
    col = arr[:, x, :3]
    # Card is white (mean > 245)
    in_card = [y for y in range(100, 600) if np.all(col[y] > 240)]
    if in_card:
        print(f'{name} card (at x={x}): top y = {min(in_card)}, bottom y = {max(in_card)}, height = {max(in_card) - min(in_card)}')

# And where is the banner vertically?
# Sample at x=750:
banner_y = [y for y in range(400, 750) if arr[y, 750, 0] < 70 and arr[y, 750, 2] > 70]
if banner_y:
    print(f'Banner at x=750: top y = {min(banner_y)}, bottom y = {max(banner_y)}, height = {max(banner_y) - min(banner_y)}')


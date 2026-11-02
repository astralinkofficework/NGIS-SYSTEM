from PIL import Image
import numpy as np

im = Image.open('scratch/teacher_test.png')
arr = np.array(im)

# Let's inspect a vertical column through the middle of the Upcoming card:
# Where is the upcoming card horizontally?
# Let's find white card pixels at y=250:
for x in range(0, 1280, 20):
    val = arr[250, x, :3]
    if np.all(val > 240):
        print(f'White at x={x}')


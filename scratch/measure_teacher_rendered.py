from PIL import Image
import numpy as np

im = Image.open('scratch/teacher_test.png')
arr = np.array(im)

# Let's inspect:
# 1. Row 1 cards (at y=200):
# Find card boundaries:
cards_x = [x for x in range(100, 1280) if np.all(arr[200, x, :3] > 240)]
# Cluster
intervals = []
start = cards_x[0]
for i in range(1, len(cards_x)):
    if cards_x[i] > cards_x[i-1] + 5:
        intervals.append((start, cards_x[i-1]))
        start = cards_x[i]
intervals.append((start, cards_x[-1]))

print('Cards at y=200:')
for s, e in intervals:
    print(f'  Card [{s}, {e}], width = {e-s}')

# Where do the cards end vertically? (Find bottom of cards)
# Sample along x=500 (middle of upcoming card) and x=1100 (middle of deadlines card)
for x, name in [(300, 'Profile'), (600, 'Upcoming'), (1100, 'Deadlines')]:
    bottom_y = None
    for y in range(150, 500):
        if not np.all(arr[y, x, :3] > 240): # Exited white card
            bottom_y = y
            break
    print(f'{name} bottom y = {bottom_y}')

# 2. Banner (below cards, y ~ 450 to 650)
banner_pts = []
for y in range(350, 700):
    for x in range(100, 1280):
        r, g, b = [int(v) for v in arr[y, x][:3]]
        # Banner is blue/teal background
        if r < 70 and b > 70:
            banner_pts.append((x, y))

if banner_pts:
    xs = [p[0] for p in banner_pts]
    ys = [p[1] for p in banner_pts]
    print(f'Banner bounds: x [{min(xs)}, {max(xs)}] (width {max(xs)-min(xs)}), y [{min(ys)}, {max(ys)}]')
else:
    print('No banner found!')


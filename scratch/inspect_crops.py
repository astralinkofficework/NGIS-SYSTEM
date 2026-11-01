from PIL import Image

for name in ['dept_curr_desktop', 'dept_curr_tablet', 'dept_curr_mobile']:
    im = Image.open(f'scratch/{name}.png')
    print(f'{name} size: {im.size}')


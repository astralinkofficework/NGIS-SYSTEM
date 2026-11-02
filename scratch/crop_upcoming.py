from PIL import Image

im = Image.open('scratch/teacher_test.png')
# Crop Upcoming card: x from 550 to 960, y from 200 to 570
crop = im.crop((550, 200, 960, 570))
crop.save('scratch/upcoming_card_rendered.png')
print('Saved scratch/upcoming_card_rendered.png')


from PIL import Image

img = Image.open('scratch/student_no_lines.png')
w, h = img.size

crop_upcoming = img.crop((int(w * 0.23), int(h * 0.22), int(w * 0.76), int(h * 0.72)))
crop_upcoming.save('scratch/check_upcoming.png')

crop_deadlines = img.crop((int(w * 0.76), int(h * 0.22), int(w * 0.98), int(h * 0.93)))
crop_deadlines.save('scratch/check_deadlines.png')

print("Cropped check images successfully!")


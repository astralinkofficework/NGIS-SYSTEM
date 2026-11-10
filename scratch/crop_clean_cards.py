from PIL import Image
import os

artifact_dir = r"C:\Users\oudom\.gemini\antigravity\brain\8fd19b10-a09a-43d8-a122-cb4a75dc0ff6"

for name in ["teacher_profiles_clean_cards.png", "student_profiles_clean_cards.png"]:
    src = os.path.join(artifact_dir, name)
    if os.path.exists(src):
        im = Image.open(src)
        # Crop to the top telemetry cards region (approx y: 150 to 380, x: 0 to 1440)
        crop_box = (0, 150, 1440, 380)
        cropped = im.crop(crop_box)
        out_name = name.replace(".png", "_crop.png")
        out_path = os.path.join(artifact_dir, out_name)
        cropped.save(out_path)
        print(f"Saved cropped shot -> {out_path}")


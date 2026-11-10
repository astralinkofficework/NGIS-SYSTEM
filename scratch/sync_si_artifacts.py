import shutil, os

art_dir = r"C:\Users\oudom\.gemini\antigravity\brain\c3bf1c11-3155-48a6-b3ee-4e74d6713af7"

files = [
    "school_info_desktop_1440.png",
    "school_info_mobile_390.png",
    "principal_school_info_390.png"
]

for f in files:
    src = os.path.join("scratch", f)
    if os.path.exists(src):
        dst = os.path.join(art_dir, f)
        shutil.copyfile(src, dst)
        print(f"Copied {f} to artifacts directory.")

print("Artifact image sync complete!")


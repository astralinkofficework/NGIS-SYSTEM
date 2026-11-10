with open("pages/principal/principal-classes.html", "r", encoding="utf-8") as f:
    c_lines = f.readlines()

print("CLASSES LINES 195-285:")
print("".join(c_lines[195:285]))

with open("pages/principal/principal-departments.html", "r", encoding="utf-8") as f:
    d_lines = f.readlines()

print("\n" + "="*50 + "\nDEPTS LINES 175-260:")
print("".join(d_lines[175:260]))

with open("pages/principal/principal.html", "r", encoding="utf-8") as f:
    p_lines = f.readlines()

print("\n" + "="*50 + "\nPRINCIPAL.HTML LINES 355-435:")
print("".join(p_lines[355:435]))


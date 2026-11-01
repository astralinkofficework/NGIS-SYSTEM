import zipfile
import xml.etree.ElementTree as ET

wb_path = r'C:/Users/oudom/.gemini/antigravity/brain/42e7f2c5-dd76-4874-84f0-090ddb400de9/.user_uploaded/media_1793519165129_18aed4c0.xlsx'
with zipfile.ZipFile(wb_path) as z:
    for name in z.namelist():
        if 'workbook.xml' in name:
            tree = ET.fromstring(z.read(name))
            sheets = [s.attrib['name'] for s in tree.iter('{http://schemas.openxmlformats.org/spreadsheetml/2006/main}sheet')]
            with open("scratch/sheet_names.txt", "w", encoding="utf-8") as f:
                for s in sheets:
                    f.write(s + "\n")
print("Done listing sheets")

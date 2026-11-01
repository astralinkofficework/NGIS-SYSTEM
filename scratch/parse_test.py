import zipfile
import xml.etree.ElementTree as ET
import json
import re

wb_path = r'C:/Users/oudom/.gemini/antigravity/brain/42e7f2c5-dd76-4874-84f0-090ddb400de9/.user_uploaded/media_1793519165129_18aed4c0.xlsx'

with zipfile.ZipFile(wb_path) as z:
    # 1. Shared Strings
    shared_strings = []
    if 'xl/sharedStrings.xml' in z.namelist():
        tree = ET.fromstring(z.read('xl/sharedStrings.xml'))
        ns = {'ns': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
        for si in tree.findall('ns:si', ns):
            # concatenate all t tags inside si
            t_elems = si.findall('.//ns:t', ns)
            val = "".join(t.text or "" for t in t_elems)
            shared_strings.append(val)
    print(f"Total shared strings: {len(shared_strings)}")

    # 2. Workbook rels
    rels_tree = ET.fromstring(z.read('xl/_rels/workbook.xml.rels'))
    rel_map = {}
    for rel in rels_tree:
        rel_map[rel.attrib['Id']] = rel.attrib['Target']

    # 3. Workbook sheet list
    wb_tree = ET.fromstring(z.read('xl/workbook.xml'))
    sheets_info = []
    for s in wb_tree.find('{http://schemas.openxmlformats.org/spreadsheetml/2006/main}sheets'):
        name = s.attrib['name']
        rId = s.attrib['{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id']
        target = rel_map[rId]
        # target might be "worksheets/sheet1.xml" or "/xl/worksheets/sheet1.xml"
        if not target.startswith('xl/'):
            target = 'xl/' + target
        sheets_info.append((name, target))

    print(f"Found {len(sheets_info)} sheets.")
    for name, target in sheets_info[:5]:
        print(f"  {name} -> {target}")

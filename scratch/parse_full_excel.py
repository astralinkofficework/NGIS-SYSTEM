import zipfile
import xml.etree.ElementTree as ET
import json
import re

wb_path = r'C:/Users/oudom/.gemini/antigravity/brain/42e7f2c5-dd76-4874-84f0-090ddb400de9/.user_uploaded/media_1793519165129_18aed4c0.xlsx'

def col2num(col_str):
    num = 0
    for c in col_str:
        num = num * 26 + (ord(c.upper()) - ord('A')) + 1
    return num - 1

def parse_cell_ref(ref):
    m = re.match(r"^([A-Z]+)([0-9]+)$", ref)
    if m:
        col_str, row_str = m.groups()
        return col2num(col_str), int(row_str) - 1
    return None, None

with zipfile.ZipFile(wb_path) as z:
    shared_strings = []
    if 'xl/sharedStrings.xml' in z.namelist():
        tree = ET.fromstring(z.read('xl/sharedStrings.xml'))
        ns = {'ns': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
        for si in tree.findall('ns:si', ns):
            t_elems = si.findall('.//ns:t', ns)
            val = "".join(t.text or "" for t in t_elems)
            shared_strings.append(val)

    rels_tree = ET.fromstring(z.read('xl/_rels/workbook.xml.rels'))
    rel_map = {}
    for rel in rels_tree:
        rel_map[rel.attrib['Id']] = rel.attrib['Target']

    wb_tree = ET.fromstring(z.read('xl/workbook.xml'))
    sheets_info = []
    for s in wb_tree.find('{http://schemas.openxmlformats.org/spreadsheetml/2006/main}sheets'):
        name = s.attrib['name']
        rId = s.attrib['{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id']
        target = rel_map[rId]
        if not target.startswith('xl/'):
            target = 'xl/' + target
        sheets_info.append((name, target))

    all_sheets = {}
    for sheet_name, sheet_path in sheets_info:
        xml_data = z.read(sheet_path)
        s_tree = ET.fromstring(xml_data)
        ns = {'ns': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
        
        sheet_rows = []
        rows_elem = s_tree.find('ns:sheetData', ns)
        if rows_elem is not None:
            for row in rows_elem.findall('ns:row', ns):
                row_idx = int(row.attrib.get('r', 1)) - 1
                row_cells = {}
                for c in row.findall('ns:c', ns):
                    r_ref = c.attrib.get('r', '')
                    col_idx, _ = parse_cell_ref(r_ref)
                    t = c.attrib.get('t', '')
                    v_elem = c.find('ns:v', ns)
                    val = v_elem.text if v_elem is not None else ''
                    if t == 's' and val.isdigit():
                        val = shared_strings[int(val)]
                    elif t == 'b':
                        val = True if val == '1' else False
                    elif t == 'inlineStr':
                        is_elem = c.find('ns:is/ns:t', ns)
                        val = is_elem.text if is_elem is not None else ''
                    row_cells[col_idx] = val
                
                # convert to array up to max col
                if row_cells:
                    max_col = max(row_cells.keys())
                    row_arr = [row_cells.get(c_idx, '') for c_idx in range(max_col + 1)]
                    sheet_rows.append({'row_idx': row_idx, 'cells': row_arr})
        
        all_sheets[sheet_name] = sheet_rows

with open('scratch/all_sheets.json', 'w', encoding='utf-8') as f:
    json.dump(all_sheets, f, ensure_ascii=False, indent=2)

print(f"Exported {len(all_sheets)} sheets successfully!")

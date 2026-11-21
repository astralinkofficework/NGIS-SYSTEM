"""
============================================================================
 Khmer School Admin Suite — dependency-free XLSX writer / reader
============================================================================
The runtime has no openpyxl, so this module writes real OOXML .xlsx files with
nothing but the standard library.  Khmer text is stored as inline strings, which
keeps the file readable in Excel, LibreOffice and Google Sheets without a shared
string table.  Colours come straight from the per-subject palette.

Public API
----------
    Sheet(name)                     -> builder
    Workbook()                      -> collection of sheets
    build_xlsx(sheets)              -> bytes
    read_xlsx(data, sheet_index=0)  -> list[list[str]]
============================================================================
"""

from __future__ import annotations

import io
import re
import zipfile
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple
from xml.etree import ElementTree as ET
from xml.sax.saxutils import escape

NS_MAIN = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
NS_REL = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
NS_PKG_REL = "http://schemas.openxmlformats.org/package/2006/relationships"

FONT_NAME = "Noto Sans Khmer"


# ── helpers ────────────────────────────────────────────────────────────────

def _a1(row: int, col: int) -> str:
    """1-based (row, col) -> A1 reference."""
    letters = ""
    n = col
    while n > 0:
        n, rem = divmod(n - 1, 26)
        letters = chr(65 + rem) + letters
    return f"{letters}{row}"


def _clean(value: Any) -> str:
    if value is None:
        return ""
    text = str(value)
    # Excel rejects XML 1.0 control characters.
    return "".join(ch for ch in text if ch in "\t\n\r" or ord(ch) >= 32)


def _rgb(color: Optional[str]) -> str:
    """Accept #RRGGBB / RRGGBB and always return an ARGB string."""
    if not color:
        return "FFFFFFFF"
    hexpart = color.lstrip("#").upper()
    if len(hexpart) == 6 and re.fullmatch(r"[0-9A-F]{6}", hexpart):
        return "FF" + hexpart
    if len(hexpart) == 8 and re.fullmatch(r"[0-9A-F]{8}", hexpart):
        return hexpart
    return "FFFFFFFF"


def _is_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


# ── Style registry ─────────────────────────────────────────────────────────

class StyleRegistry:
    """Builds styles.xml from styles requested lazily by cells."""

    def __init__(self) -> None:
        self.fonts: List[Tuple[int, bool, str]] = [(11, False, "FF1F2937")]
        self.fills: List[str] = ["", ""]          # 0 none, 1 gray125 (Excel defaults)
        self.borders: List[bool] = [False, True]  # 0 none, 1 thin
        self.xfs: List[Dict[str, Any]] = []
        self._font_keys = {(11, False, "FF1F2937"): 0}
        self._fill_keys: Dict[str, int] = {}
        self._xf_keys: Dict[str, int] = {}

    def style(self, *, fill: Optional[str] = None, bold: bool = False,
              size: int = 11, color: str = "FF1F2937",
              align: str = "center", border: bool = True,
              wrap: bool = True, vertical: str = "center") -> int:
        key = f"{fill}|{bold}|{size}|{color}|{align}|{border}|{wrap}|{vertical}"
        if key in self._xf_keys:
            return self._xf_keys[key]

        fkey = (size, bold, color)
        if fkey not in self._font_keys:
            self._font_keys[fkey] = len(self.fonts)
            self.fonts.append(fkey)

        fill_id = 0
        if fill:
            rgb = _rgb(fill)
            if rgb not in self._fill_keys:
                self._fill_keys[rgb] = len(self.fills)
                self.fills.append(rgb)
            fill_id = self._fill_keys[rgb]

        border_id = 1 if border else 0
        xf_id = len(self.xfs)
        self.xfs.append({
            "fontId": self._font_keys[fkey], "fillId": fill_id,
            "borderId": border_id, "applyFill": 1 if fill else 0,
            "applyBorder": 1 if border else 0, "applyFont": 1, "applyAlignment": 1,
            "align": align, "wrap": wrap, "vertical": vertical,
        })
        self._xf_keys[key] = xf_id
        return xf_id

    def xml(self) -> str:
        fonts = "".join(
            f'<font><sz val="{size}"/><color rgb="{color}"/>'
            f'<name val="{FONT_NAME}"/><family val="2"/>'
            f'{"<b/>" if bold else ""}</font>'
            for size, bold, color in self.fonts
        )
        fills = (
            '<fill><patternFill patternType="none"/></fill>'
            '<fill><patternFill patternType="gray125"/></fill>'
            + "".join(
                f'<fill><patternFill patternType="solid">'
                f'<fgColor rgb="{c}"/><bgColor indexed="64"/>'
                f'</patternFill></fill>' if c else
                '<fill><patternFill patternType="none"/></fill>'
                for c in self.fills[2:]
            )
        )
        thin = (
            '<border><left style="thin"><color rgb="FFD8DEE9"/></left>'
            '<right style="thin"><color rgb="FFD8DEE9"/></right>'
            '<top style="thin"><color rgb="FFD8DEE9"/></top>'
            '<bottom style="thin"><color rgb="FFD8DEE9"/></bottom>'
            '<diagonal/></border>'
        )
        borders = '<border><left/><right/><top/><bottom/><diagonal/></border>' + thin
        xfs = "".join(
            f'<xf numFmtId="0" fontId="{x["fontId"]}" fillId="{x["fillId"]}" '
            f'borderId="{x["borderId"]}" xfId="0" applyFont="{x["applyFont"]}" '
            f'applyFill="{x["applyFill"]}" applyBorder="{x["applyBorder"]}" '
            f'applyAlignment="1"><alignment horizontal="{x["align"]}" '
            f'vertical="{x["vertical"]}" wrapText="{1 if x["wrap"] else 0}"/></xf>'
            for x in self.xfs
        )
        return (
            f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            f'<styleSheet xmlns="{NS_MAIN}">'
            f'<fonts count="{len(self.fonts)}">{fonts}</fonts>'
            f'<fills count="{len(self.fills)}">{fills}</fills>'
            f'<borders count="{len(self.borders)}">{borders}</borders>'
            f'<cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs>'
            f'<cellXfs count="{len(self.xfs)}">{xfs}</cellXfs>'
            f'<cellStyles count="1"><cellStyle name="Normal" xfId="0" builtinId="0"/></cellStyles>'
            f'<dxfs count="0"/><tableStyles count="0" defaultTableStyle="TableStyleMedium2"/>'
            f'</styleSheet>'
        )


# ── Sheet builder ──────────────────────────────────────────────────────────

class Sheet:
    def __init__(self, name: str, *, landscape: bool = True,
                 paper_size: int = 9, freeze_rows: int = 0) -> None:
        self.name = (name or "Sheet")[:31].replace("/", "-").replace("\\", "-")
        self.landscape = landscape
        self.paper_size = paper_size       # 9 = A4, 8 = A3
        self.freeze_rows = freeze_rows
        self.rows: List[List[Dict[str, Any]]] = []
        self.col_widths: Dict[int, float] = {}
        self.merges: List[str] = []
        self.row_heights: Dict[int, float] = {}
        self.auto_filter: Optional[str] = None
        self._styles = StyleRegistry()

    # -- configuration ------------------------------------------------------
    def columns(self, widths: Sequence[float]) -> "Sheet":
        for i, width in enumerate(widths, 1):
            self.col_widths[i] = width
        return self

    def title(self, text: str, span: int, *, fill: str = "1E3A5F",
              color: str = "FFFFFFFF", height: float = 32) -> "Sheet":
        idx = len(self.rows) + 1
        s = self._styles.style(fill=fill, bold=True, size=15, color=color, border=False)
        self.rows.append([{"value": text, "style": s, "col": 1}])
        for c in range(2, max(2, span) + 1):
            self.rows[-1].append({"value": "", "style": s, "col": c})
        if span > 1:
            self.merges.append(f"A{idx}:{_a1(idx, span)}")
        self.row_heights[idx] = height
        return self

    def subtitle(self, text: str, span: int, *, fill: str = "EAF0F7",
                 color: str = "FF334155", height: float = 22) -> "Sheet":
        idx = len(self.rows) + 1
        s = self._styles.style(fill=fill, bold=False, size=10, color=color,
                               border=False, align="left")
        self.rows.append([{"value": text, "style": s, "col": 1}])
        for c in range(2, max(2, span) + 1):
            self.rows[-1].append({"value": "", "style": s, "col": c})
        if span > 1:
            self.merges.append(f"A{idx}:{_a1(idx, span)}")
        self.row_heights[idx] = height
        return self

    def blank(self, height: float = 8) -> "Sheet":
        idx = len(self.rows) + 1
        s = self._styles.style(border=False)
        self.rows.append([{"value": "", "style": s, "col": 1}])
        self.row_heights[idx] = height
        return self

    def headers(self, labels: Sequence[str], *, fill: str = "274C77",
                color: str = "FFFFFFFF", height: float = 30) -> "Sheet":
        idx = len(self.rows) + 1
        s = self._styles.style(fill=fill, bold=True, size=10, color=color)
        self.rows.append([
            {"value": label, "style": s, "col": i}
            for i, label in enumerate(labels, 1)
        ])
        self.row_heights[idx] = height
        return self

    def add(self, values: Sequence[Any], *, fill: Optional[str] = None,
            bold: bool = False, align: str = "center",
            color: str = "FF1F2937", number: bool = False) -> "Sheet":
        """Add a data row. `fill` colours the whole row (subject palette)."""
        s = self._styles.style(fill=fill, bold=bold, align=align, color=color)
        row = [
            {"value": v, "style": s, "col": i, "number": number or _is_number(v)}
            for i, v in enumerate(values, 1)
        ]
        self.rows.append(row)
        return self

    def cell_fill(self, row_index: int, col_index: int, color: str,
                  *, bold: bool = False, color_text: str = "FF1F2937") -> "Sheet":
        """Recolour a single already-added cell (1-based row/col)."""
        row = self.rows[row_index - 1]
        if col_index - 1 >= len(row):
            return self
        cell = row[col_index - 1]
        cell["style"] = self._styles.style(fill=color, bold=bold, color=color_text)
        return self

    def xml(self) -> str:
        pane = ""
        if self.freeze_rows:
            pane = (
                f'<pane ySplit="{self.freeze_rows}" '
                f'topLeftCell="A{self.freeze_rows + 1}" activePane="bottomLeft" state="frozen"/>'
                f'<selection pane="bottomLeft" activeCell="A{self.freeze_rows + 1}" '
                f'sqref="A{self.freeze_rows + 1}"/>'
            )
        cols = ""
        if self.col_widths:
            cols = "<cols>" + "".join(
                f'<col min="{i}" max="{i}" width="{w}" customWidth="1"/>'
                for i, w in sorted(self.col_widths.items())
            ) + "</cols>"

        body = []
        for r, row in enumerate(self.rows, 1):
            attrs = f' r="{r}"'
            if r in self.row_heights:
                attrs += f' ht="{self.row_heights[r]}" customHeight="1"'
            cells = []
            for cell in row:
                ref = _a1(r, cell["col"])
                style = cell["style"]
                value = _clean(cell["value"])
                if value == "":
                    cells.append(f'<c r="{ref}" s="{style}"/>')
                elif cell.get("number") and _is_number(cell["value"]):
                    cells.append(f'<c r="{ref}" s="{style}"><v>{cell["value"]}</v></c>')
                else:
                    cells.append(
                        f'<c r="{ref}" s="{style}" t="inlineStr">'
                        f'<is><t xml:space="preserve">{escape(value)}</t></is></c>'
                    )
            body.append(f'<row{attrs}>{"".join(cells)}</row>')

        merges = ""
        if self.merges:
            merges = (
                f'<mergeCells count="{len(self.merges)}">'
                + "".join(f'<mergeCell ref="{m}"/>' for m in self.merges)
                + "</mergeCells>"
            )
        auto_filter = f'<autoFilter ref="{self.auto_filter}"/>' if self.auto_filter else ""
        dimension = f'A1:{_a1(max(1, len(self.rows)), max(1, max((len(r) for r in self.rows), default=1)))}'

        return (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            f'<worksheet xmlns="{NS_MAIN}">'
            f'<dimension ref="{dimension}"/>'
            f'<sheetViews><sheetView workbookViewId="0" showGridLines="0">{pane}</sheetView></sheetViews>'
            '<sheetFormatPr defaultRowHeight="18"/>'
            f'{cols}<sheetData>{"".join(body)}</sheetData>'
            f'{merges}{auto_filter}'
            '<pageMargins left="0.3" right="0.3" top="0.5" bottom="0.5" header="0.2" footer="0.2"/>'
            f'<pageSetup paperSize="{self.paper_size}" orientation="{"landscape" if self.landscape else "portrait"}" '
            'fitToWidth="1" fitToHeight="0"/>'
            '<headerFooter><oddFooter>&amp;C&amp;P / &amp;N</oddFooter></headerFooter>'
            '</worksheet>'
        )


# ── Workbook assembly ──────────────────────────────────────────────────────

class Workbook:
    def __init__(self) -> None:
        self.sheets: List[Sheet] = []

    def sheet(self, name: str, **kwargs: Any) -> Sheet:
        s = Sheet(name, **kwargs)
        self.sheets.append(s)
        return s

    def bytes(self) -> bytes:
        if not self.sheets:
            self.sheet("Sheet1").add([""])
        content_types = (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
            '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
            '<Default Extension="xml" ContentType="application/xml"/>'
            '<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>'
            '<Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>'
            + "".join(
                f'<Override PartName="/xl/worksheets/sheet{i}.xml" '
                'ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
                for i in range(1, len(self.sheets) + 1)
            )
            + '</Types>'
        )
        root_rels = (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            f'<Relationships xmlns="{NS_PKG_REL}">'
            '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>'
            '</Relationships>'
        )
        sheet_tags = "".join(
            f'<sheet name="{escape(_clean(s.name))}" sheetId="{i}" r:id="rId{i}"/>'
            for i, s in enumerate(self.sheets, 1)
        )
        workbook = (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            f'<workbook xmlns="{NS_MAIN}" xmlns:r="{NS_REL}">'
            f'<sheets>{sheet_tags}</sheets></workbook>'
        )
        rel_tags = "".join(
            f'<Relationship Id="rId{i}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet{i}.xml"/>'
            for i in range(1, len(self.sheets) + 1)
        )
        styles_id = len(self.sheets) + 1
        rel_tags += (
            f'<Relationship Id="rId{styles_id}" '
            'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" '
            'Target="styles.xml"/>'
        )
        workbook_rels = (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            f'<Relationships xmlns="{NS_PKG_REL}">{rel_tags}</Relationships>'
        )

        # One shared style table: merge every sheet's lazy style registry into a
        # single global table, then rewrite cell style indices to the global ids.
        global_styles = StyleRegistry()
        global_xf_keys: Dict[str, int] = {}
        for s in self.sheets:
            local = s._styles
            font_map: Dict[int, int] = {}
            fill_map: Dict[int, int] = {}
            for key, idx in local._font_keys.items():
                if key not in global_styles._font_keys:
                    global_styles._font_keys[key] = len(global_styles.fonts)
                    global_styles.fonts.append(key)
                font_map[idx] = global_styles._font_keys[key]
            for rgb, idx in local._fill_keys.items():
                if rgb not in global_styles._fill_keys:
                    global_styles._fill_keys[rgb] = len(global_styles.fills)
                    global_styles.fills.append(rgb)
                fill_map[idx] = global_styles._fill_keys[rgb]

            xf_map: List[int] = []
            for xf in local.xfs:
                gfont = font_map.get(xf["fontId"], 0)
                gfill = fill_map.get(xf["fillId"], 0) if xf["fillId"] else 0
                resolved = {**xf, "fontId": gfont, "fillId": gfill}
                gkey = "|".join(str(resolved[k]) for k in
                                ("fontId", "fillId", "borderId", "applyFont", "applyFill",
                                 "applyBorder", "align", "wrap", "vertical"))
                if gkey not in global_xf_keys:
                    global_xf_keys[gkey] = len(global_styles.xfs)
                    global_styles.xfs.append(resolved)
                xf_map.append(global_xf_keys[gkey])
            for row in s.rows:
                for cell in row:
                    cell["style"] = xf_map[cell["style"]]

        buf = io.BytesIO()
        with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
            zf.writestr("[Content_Types].xml", content_types)
            zf.writestr("_rels/.rels", root_rels)
            zf.writestr("xl/workbook.xml", workbook)
            zf.writestr("xl/_rels/workbook.xml.rels", workbook_rels)
            zf.writestr("xl/styles.xml", global_styles.xml())
            for i, s in enumerate(self.sheets, 1):
                zf.writestr(f"xl/worksheets/sheet{i}.xml", s.xml())
        return buf.getvalue()


def build_xlsx(sheets: Iterable[Sheet]) -> bytes:
    wb = Workbook()
    wb.sheets = list(sheets)
    return wb.bytes()


# ── Reader (for Excel import) ──────────────────────────────────────────────

def _col_index(ref: str) -> int:
    letters = re.match(r"[A-Z]+", ref.upper())
    if not letters:
        return 1
    n = 0
    for ch in letters.group(0):
        n = n * 26 + (ord(ch) - 64)
    return n


def _cell_text(cell: ET.Element, shared: List[str]) -> str:
    ctype = cell.get("t", "")
    if ctype == "inlineStr":
        node = cell.find(f"{{{NS_MAIN}}}is")
        return "".join(t.text or "" for t in node.iter(f"{{{NS_MAIN}}}t")) if node is not None else ""
    v = cell.find(f"{{{NS_MAIN}}}v")
    raw = v.text if v is not None and v.text else ""
    if ctype == "s":
        try:
            return shared[int(raw)]
        except (ValueError, IndexError):
            return ""
    if ctype == "b":
        return "TRUE" if raw == "1" else "FALSE"
    return raw


def read_xlsx(data: bytes, sheet_index: int = 0) -> List[List[str]]:
    """Return all rows of one worksheet as a rectangular list of strings."""
    with zipfile.ZipFile(io.BytesIO(data)) as zf:
        shared: List[str] = []
        if "xl/sharedStrings.xml" in zf.namelist():
            root = ET.fromstring(zf.read("xl/sharedStrings.xml"))
            for si in root.findall(f"{{{NS_MAIN}}}si"):
                shared.append("".join(t.text or "" for t in si.iter(f"{{{NS_MAIN}}}t")))

        names = sorted(
            (n for n in zf.namelist()
             if re.fullmatch(r"xl/worksheets/sheet\d+\.xml", n)),
            key=lambda n: int(re.search(r"(\d+)", n).group(1)),
        )
        if not names:
            return []
        sheet_path = names[min(sheet_index, len(names) - 1)]
        root = ET.fromstring(zf.read(sheet_path))
        rows: List[List[str]] = []
        for row in root.iter(f"{{{NS_MAIN}}}row"):
            cells: Dict[int, str] = {}
            for cell in row.findall(f"{{{NS_MAIN}}}c"):
                ref = cell.get("r", "A1")
                cells[_col_index(ref)] = _cell_text(cell, shared)
            width = max(cells.keys(), default=0)
            rows.append([cells.get(i, "") for i in range(1, width + 1)])
        return rows

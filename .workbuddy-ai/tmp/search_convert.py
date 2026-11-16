# -*- coding: utf-8 -*-
"""One-shot source-level refactor: raw Tailwind absolute-positioned search bars
-> shared .ngis-search flexbox pattern (no JS dependency, no icon/placeholder
overlap even before enhancer runs or when icon fonts load slowly)."""
import io
import re
import sys

FILES = [
    "pages/shared/departments.html",
    "pages/student/student-assignments.html",
    "pages/admin/admin-absence-stats.html",
    "pages/admin/admin-attendance.html",
    "pages/principal/principal-activity.html",
    "pages/principal/principal-lost-found.html",
    "pages/principal/principal-services.html",
    "pages/teacher/teacher-lessons.html",
    "pages/teacher/teacher-roster.html",
    "pages/admin/admin-timetables.html",
    "pages/admin/admin-lost-found.html",
    "pages/admin/admin-news.html",
    "pages/admin/admin-campuses.html",
    "pages/admin/admin-classes.html",
]

ICON_RE = re.compile(r'<span class="material-symbols-outlined ([^"]*)">\s*search\s*</span>')
INPUT_RE = re.compile(r'<input\b[^>]*>')
KBD_RE = re.compile(r'<kbd\b[^>]*>.*?</kbd>', re.S)
CLEAR_RE = re.compile(r'<button\b[^>]*aria-label="[^"]*"[^>]*>')

# classes allowed to survive on the input (responsive widths only)
INPUT_KEEP = re.compile(r'^(w-full|[sml][gr]?:(w-\S+|flex-1))$')
# wrapper utilities that must go (padding + relative positioning)
WRAPPER_DROP = re.compile(r'^(relative|p-\S+|px-\S+|py-\S+|pt-\S+|pb-\S+|pl-\S+|pr-\S+)$')
KBD_DROP = re.compile(r'^(absolute|right-\S+|left-\S+|top-\S+|bottom-\S+|-?translate-y-\S+|-?translate-x-\S+|text-\S+|font-\S+|px-\S+|py-\S+|p-\S+|rounded\S*|bg-\S+|border\S*)$')
CLEAR_DROP = re.compile(r'^(absolute|right-\S+|left-\S+|top-\S+|bottom-\S+|-?translate-\S+|text-\S+|hover:\S+|p-\S+|px-\S+|py-\S+|rounded\S*|bg-\S+|border\S*|shadow\S*)$')


def strip_class(cls, drop_re, add):
    parts = [c for c in cls.split() if not drop_re.match(c)]
    if add not in parts:
        parts.append(add)
    return " ".join(parts)


def convert_block(block, compact):
    """Rewrite one wrapper div (icon + input [+ kbd/clear]) to ngis-search."""
    # -- wrapper opening tag ------------------------------------------------
    wend = block.find(">")
    wtag = block[: wend + 1]
    wcls_m = re.search(r'class="([^"]*)"', wtag)
    wcls = wcls_m.group(1)
    new_wcls = [c for c in wcls.split() if not WRAPPER_DROP.match(c)]
    new_wcls.append("ngis-search")
    if compact:
        new_wcls.append("ngis-search--compact")
    new_wtag = wtag.replace(wcls_m.group(0), 'class="%s"' % " ".join(new_wcls), 1)

    body = block[wend + 1:]

    # -- icon(s) ------------------------------------------------------------
    icon_html = '<span class="material-symbols-outlined ngis-search-icon" aria-hidden="true">search</span>'
    icons = list(ICON_RE.finditer(body))
    if not icons:
        return None, "no absolute search icon"
    # -- input ---------------------------------------------------------------
    inputs = list(INPUT_RE.finditer(body))
    if not inputs:
        return None, "no input"
    inp = inputs[0]
    itag = inp.group(0)
    # drop inline padding styles (legacy !important padding-left)
    itag = re.sub(r'\s+style="[^"]*padding[^"]*"', "", itag)
    icls_m = re.search(r'class="([^"]*)"', itag)
    if icls_m:
        keep = [c for c in icls_m.group(1).split() if INPUT_KEEP.match(c)]
        keep.append("ngis-search-input")
        itag = itag.replace(icls_m.group(0), 'class="%s"' % " ".join(keep), 1)
    else:
        itag = itag[:-1] + ' class="ngis-search-input">'

    # -- optional kbd / clear button ----------------------------------------
    kbd_m = KBD_RE.search(body)
    kbd_html = None
    if kbd_m:
        kcls_m = re.search(r'class="([^"]*)"', kbd_m.group(0))
        kbd_html = kbd_m.group(0).replace(
            kcls_m.group(0), 'class="%s"' % strip_class(kcls_m.group(1), KBD_DROP, "ngis-search-kbd"), 1)

    clear_html = None
    clear_full = None
    cbtn_re = re.compile(r'<button\b([^>]*)>((?:(?!</button>).)*)</button>', re.S)
    for bm in cbtn_re.finditer(body):
        attrs = bm.group(1)
        if re.search(r'aria-label="[^"]*[Cc]lear[^"]*"', attrs) and "Clear search" in attrs:
            ccls_m = re.search(r'class="([^"]*)"', attrs)
            new_attrs = attrs.replace(
                ccls_m.group(0), 'class="%s"' % strip_class(ccls_m.group(1), CLEAR_DROP, "ngis-search-clear"), 1)
            clear_full = '<button' + new_attrs + '>' + bm.group(2) + '</button>'
            break

    # -- reassemble: icon, input, kbd, clear ---------------------------------
    new_body = icon_html + itag
    if kbd_html:
        new_body += kbd_html
    if clear_full:
        new_body += clear_full
    new_block = new_wtag + new_body + "</div>"
    return new_block, None


def main():
    dry = "--dry" in sys.argv
    total = 0
    for path in FILES:
        src = io.open(path, encoding="utf-8").read()
        # locate wrapper blocks containing an absolute search icon
        out, pos, converted, errors = [], 0, 0, []
        for m in ICON_RE.finditer(src):
            cls = m.group(1)
            if "absolute" not in cls.split():
                continue
            wstart = src.rfind("<div", 0, m.start())
            if wstart < pos and out:
                # wrapper start before last processed region -> skip (already handled)
                continue
            close = src.find("</div>", m.start())
            block = src[wstart: close + 6]
            icls = re.search(r'<input\b[^>]*class="([^"]*)"', block)
            compact = bool(icls and "py-1" in icls.group(1).split())
            new_block, err = convert_block(block, compact)
            if err:
                errors.append((src[:m.start()].count("\n") + 1, err))
                continue
            out.append(src[pos:wstart])
            out.append(new_block)
            pos = close + 6
            converted += 1
        out.append(src[pos:])
        if converted:
            print("%-46s %d converted%s" % (path, converted, (" ERRORS %s" % errors) if errors else ""))
            total += converted
            if not dry:
                io.open(path, "w", encoding="utf-8", newline="\n").write("".join(out))
        elif errors:
            print("%-46s ERRORS %s" % (path, errors))
    print("TOTAL:", total)


if __name__ == "__main__":
    main()

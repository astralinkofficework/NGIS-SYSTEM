"""Phase 1 audit: inventory principal pages' CSS/JS, container widths, table classes,
toolbar patterns, and inline spacing values."""
import glob, re, json

report = {}
for f in sorted(glob.glob('pages/principal/*.html')):
    s = open(f, encoding='utf-8').read()
    name = f.replace('\\', '/').split('/')[-1]
    css = list(dict.fromkeys(re.findall(r'href="[^"]*?css/([^"]+)"', s)))
    js = list(dict.fromkeys(re.findall(r'src="[^"]*?js/([^"]+)"', s)))
    # main container classes
    containers = re.findall(r'<(?:div|main)[^>]*class="([^"]*(?:max-w|px-|mx-auto)[^"]*)"', s)
    # tables
    tables = len(re.findall(r'<table', s))
    thead_cls = re.findall(r'<thead[^>]*class="([^"]*)"', s)
    th_cls = list(dict.fromkeys(re.findall(r'<th[^>]*class="([^"]*)"', s)))[:6]
    td_pad = list(dict.fromkeys(re.findall(r'<td[^>]*class="([^"]*p-[xy]?[^"]*)"', s)))[:6]
    tr_cls = list(dict.fromkeys(re.findall(r'<tr[^>]*class="([^"]*)"', s)))[:6]
    # dynamic row templates (JS-generated tables)
    dyn_tr = len(re.findall(r'<tr', s))
    # inline style padding/margin/gap values
    inline_sp = re.findall(r'(?:padding|margin|gap)\s*:\s*[\d.]+px', s)
    # search / filter controls
    inputs = len(re.findall(r'<input', s))
    selects = len(re.findall(r'<select', s))
    buttons = len(re.findall(r'<button', s))
    # data source: api fetches
    apis = list(dict.fromkeys(re.findall(r'/api/[a-zA-Z0-9_/\-\.\{\}\$]+', s)))
    report[name] = dict(css=css, js=js, containers=containers[:4], tables=tables,
                        thead_cls=thead_cls[:3], th_cls=th_cls, td_pad=td_pad,
                        tr_cls=tr_cls, inline_sp=len(inline_sp),
                        inputs=inputs, selects=selects, buttons=buttons, apis=apis[:12])
print(json.dumps(report, indent=1))

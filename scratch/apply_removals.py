with open(r"assets/js/khmer-suite-ui.js", "r", encoding="utf-8") as f:
    text = f.read()

# 1. Update workflowStepperHtml to return empty string
wf_start = "function workflowStepperHtml() {"
wf_end = "function headHtml() {"
idx_wf_start = text.find(wf_start)
idx_wf_end = text.find(wf_end)

assert idx_wf_start != -1 and idx_wf_end != -1, "Cannot find workflowStepperHtml"

new_wf_func = "function workflowStepperHtml() {\n    return '';\n  }\n\n  "
text = text[:idx_wf_start] + new_wf_func + text[idx_wf_end:]

# 2. In classMasterModernHtml, remove the duplicate Class Identity Header Banner
banner_start = "'<!-- Class Identity Header Banner -->'"
banner_end = "'<!-- Timetable Matrix Grid -->'"

idx_b_start = text.find(banner_start)
idx_b_end = text.find(banner_end)

assert idx_b_start != -1 and idx_b_end != -1, "Cannot find class banner"
text = text[:idx_b_start] + text[idx_b_end:]

# 3. In teacherViewModernHtml, remove the duplicate Teacher Header Banner
t_banner_start = "'<!-- Teacher Header Banner -->'"
t_banner_end = "'<!-- Timetable Matrix Grid -->'"

idx_tb_start = text.find(t_banner_start)
idx_tb_end = text.find(t_banner_end)

assert idx_tb_start != -1 and idx_tb_end != -1, "Cannot find teacher banner"
text = text[:idx_tb_start] + text[idx_tb_end:]

with open(r"assets/js/khmer-suite-ui.js", "w", encoding="utf-8") as f:
    f.write(text)

print("Successfully applied removals to assets/js/khmer-suite-ui.js")


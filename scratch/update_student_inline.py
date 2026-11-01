with open('pages/student/student.html', 'r', encoding='utf-8') as f:
    c = f.read()

target = "</style>"
extra_style = """
  /* Keep all inner panels completely transparent with no border lines */
  .ov-inner-panel,
  .ov-deadline-panel,
  .ov-panel-feed {
    background: transparent !important;
    background-color: transparent !important;
    border: none !important;
    border-top: none !important;
    border-bottom: none !important;
    border-left: none !important;
    border-right: none !important;
    box-shadow: none !important;
    outline: none !important;
  }

  .ov-inner-head,
  .ov-deadline-head {
    border-bottom: none !important;
    border-top: none !important;
    border: none !important;
  }

  .ov-inner-item,
  .ov-deadline-item {
    border-bottom: none !important;
    border-top: none !important;
    border: none !important;
  }
</style>"""

if target in c:
    c = c.replace(target, extra_style, 1)
    with open('pages/student/student.html', 'w', encoding='utf-8') as f:
        f.write(c)
    print("Updated student.html with transparent rules")
else:
    print("Target not found")


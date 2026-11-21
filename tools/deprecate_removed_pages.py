def make_redirect_page(title, target_url, target_name):
    return f"""<!doctype html>
<html lang="en" data-theme="light">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>NGIS — Redirecting to {target_name}</title>
  <meta http-equiv="refresh" content="1;url={target_url}">
  <link rel="stylesheet" href="../../assets/css/app.css?v=3.2">
  <script>window.location.replace('{target_url}');</script>
</head>
<body class="min-h-screen bg-[#F7F9F7] flex items-center justify-center p-4 font-sans text-slate-800">
  <div class="max-w-md w-full bg-white rounded-2xl border border-slate-200 p-6 text-center shadow-sm">
    <div class="w-12 h-12 rounded-full bg-emerald-50 text-[#0F5132] mx-auto flex items-center justify-center mb-3">
      <svg class="w-6 h-6 stroke-current animate-spin" fill="none" viewBox="0 0 24 24">
        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
      </svg>
    </div>
    <h2 class="text-base font-medium text-slate-900 mb-1">{title} Consolidated</h2>
    <p class="text-xs text-slate-500 mb-4">This section has been unified into <span class="font-medium text-slate-700">{target_name}</span>. Redirecting you automatically...</p>
    <a href="{target_url}" class="inline-flex items-center px-4 py-2 rounded-lg bg-[#0F5132] text-white text-xs font-medium hover:bg-[#0a3d25] transition-colors">
      Go to {target_name} &rarr;
    </a>
  </div>
</body>
</html>"""

with open('pages/teacher/teacher-departments.html', 'w', encoding='utf-8') as f:
    f.write(make_redirect_page("Department Management", "teacher.html", "Teacher Dashboard"))

with open('pages/teacher/teacher-gradebook.html', 'w', encoding='utf-8') as f:
    f.write(make_redirect_page("Gradebook Evaluation", "teacher-reports.html", "Academic Reports"))

with open('pages/teacher/teacher-documents.html', 'w', encoding='utf-8') as f:
    f.write(make_redirect_page("Course Documents", "teacher-lessons.html", "Learning Materials"))

print("Deprecation redirects created successfully.")

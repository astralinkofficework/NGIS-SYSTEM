import re

# Test sample string
sample = """
<span class="px-2.5 py-1 text-xs rounded-full bg-emerald-50 text-emerald-700 border border-emerald-200 font-bold">Active</span>
<span class="px-2 py-0.5 rounded text-xs bg-amber-50 text-amber-700 border border-amber-200">Pending Review</span>
<span class="px-2 py-0.5 rounded text-xs bg-rose-50 text-rose-600 border border-rose-200">Overdue</span>
<button class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 font-bold">Create User</button>
<a class="nav-item active bg-blue-600 text-white">Dashboard</a>
<div style="background-color: #2455D6; color: #FFFFFF;">Banner</div>
<div style="background: #EAF2FF; border: 1px solid #E5EAF2; color: #243247;">Card</div>
"""

# Let's verify our replacements
print("Original:")
print(sample)


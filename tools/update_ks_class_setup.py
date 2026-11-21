file_path = 'assets/js/khmer-suite-ui.js'
with open(file_path, 'r', encoding='utf-8') as f:
    code = f.read()

target = """                  '</tbody>' +
                '</table>' +
              '</div>'"""

replacement = """                  '</tbody>' +
                '</table>' +
                (classAssignments.length > 6 ? (
                  '<div class="py-2.5 px-4 bg-slate-50/70 border-t border-slate-200/60 flex items-center justify-center">' +
                    '<button type="button" class="text-xs font-medium text-[#176B45] hover:text-[#14532D] flex items-center gap-1.5 transition-colors cursor-pointer py-1.5 px-3 rounded-lg hover:bg-emerald-50/60" data-act="toggle-class-setup-rows">' +
                      '<span>' + (isClassSetupExp ? 'Show Less (Showing all ' + classAssignments.length + ' allocations)' : 'Show More (' + (classAssignments.length - 6) + ' more allocations)') + '</span>' +
                      '<span class="material-symbols-outlined text-[16px]">' + (isClassSetupExp ? 'expand_less' : 'expand_more') + '</span>' +
                    '</button>' +
                  '</div>'
                ) : '') +
              '</div>'"""

if target in code:
    code = code.replace(target, replacement, 1)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(code)
    print("Successfully replaced table tail!")
else:
    print("Target not found.")

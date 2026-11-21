with open('pages/teacher/teacher-reports.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Insert pagination HTML after </table> in AcademicReportsDataGrid
table_end_tag = '</table>\n      </div>\n    </div>\n    <!-- END: AcademicReportsDataGrid -->'
pagination_html = """</table>
      </div>
      <!-- Pagination Controls Bar (Section 7) -->
      <div id="reportsPaginationContainer" class="px-4 py-3 bg-slate-50/80 border-t border-slate-200 flex flex-col sm:flex-row items-center justify-between gap-3 text-xs text-slate-500">
        <span id="reportsPaginationSummary">Showing 1 to 8 of 17 reports</span>
        <div class="flex items-center gap-2">
          <button type="button" id="reportsPrevBtn" onclick="window.reportsPrevPage()" class="px-3 py-1.5 rounded-lg border border-slate-200 bg-white hover:bg-slate-50 text-slate-700 text-xs font-normal transition disabled:opacity-40 disabled:cursor-not-allowed cursor-pointer">
            Previous
          </button>
          <span id="reportsPageIndicator" class="px-2 text-slate-600 font-medium">Page 1 of 3</span>
          <button type="button" id="reportsNextBtn" onclick="window.reportsNextPage()" class="px-3 py-1.5 rounded-lg border border-slate-200 bg-white hover:bg-slate-50 text-slate-700 text-xs font-normal transition disabled:opacity-40 disabled:cursor-not-allowed cursor-pointer">
            Next
          </button>
        </div>
      </div>
    </div>
    <!-- END: AcademicReportsDataGrid -->"""

assert table_end_tag in text, "Could not find table_end_tag"
text = text.replace(table_end_tag, pagination_html, 1)

# 2. Add pagination variables and selectReportStudent logic
js_additions = """
  let reportsCurrentPage = 1;
  const REPORTS_PER_PAGE = 8;
  let selectedReportStudentId = '2026-STD-0142';

  window.selectReportStudent = function(studentId) {
    selectedReportStudentId = studentId;
    setModalTargetStudent(studentId, true);
    renderTable();
  };

  window.reportsPrevPage = function() {
    if (reportsCurrentPage > 1) {
      reportsCurrentPage--;
      renderTable();
    }
  };

  window.reportsNextPage = function() {
    const filtered = getFilteredReports();
    const maxPages = Math.max(1, Math.ceil(filtered.length / REPORTS_PER_PAGE));
    if (reportsCurrentPage < maxPages) {
      reportsCurrentPage++;
      renderTable();
    }
  };
"""

target_script_start = "let reportsData = ["
assert target_script_start in text, "Could not find target_script_start"
text = text.replace(target_script_start, js_additions + "\n  " + target_script_start, 1)

# 3. Update renderTable to paginate and apply selected-row
old_render_body = """    if (totalCount === 0) {
      tbody.innerHTML = `
        <tr>
          <td colspan="9" class="py-8 text-center text-slate-400 font-sans">
            No matching academic reports found for "${searchQuery}".
          </td>
        </tr>
      `;
    } else {
      tbody.innerHTML = filtered.map((r, idx) => {"""

new_render_body = """    const maxPages = Math.max(1, Math.ceil(totalCount / REPORTS_PER_PAGE));
    if (reportsCurrentPage > maxPages) reportsCurrentPage = maxPages;

    const startIdx = (reportsCurrentPage - 1) * REPORTS_PER_PAGE;
    const endIdx = Math.min(startIdx + REPORTS_PER_PAGE, totalCount);
    const pageRows = filtered.slice(startIdx, endIdx);

    // Update pagination UI
    const sumEl = document.getElementById('reportsPaginationSummary');
    const indEl = document.getElementById('reportsPageIndicator');
    const prevBtn = document.getElementById('reportsPrevBtn');
    const nextBtn = document.getElementById('reportsNextBtn');

    if (sumEl) sumEl.textContent = totalCount > 0 ? `Showing ${startIdx + 1} to ${endIdx} of ${totalCount} reports` : 'Showing 0 reports';
    if (indEl) indEl.textContent = `Page ${reportsCurrentPage} of ${maxPages}`;
    if (prevBtn) prevBtn.disabled = reportsCurrentPage <= 1;
    if (nextBtn) nextBtn.disabled = reportsCurrentPage >= maxPages;

    if (totalCount === 0) {
      tbody.innerHTML = `
        <tr>
          <td colspan="9" class="py-8 text-center text-slate-400 font-sans">
            No matching academic reports found for "${searchQuery}".
          </td>
        </tr>
      `;
    } else {
      tbody.innerHTML = pageRows.map((r, idx) => {
        const isSelected = r.id === selectedReportStudentId;
        const selectedIndicator = isSelected ? 'selected-row border-l-4 border-[#0F5132]' : '';"""

assert old_render_body in text, "Could not find old_render_body"
text = text.replace(old_render_body, new_render_body, 1)

# Update tr row in renderTable
old_tr_ret = 'return `\n          <tr class="${rowBg} transition-colors" data-student-id="${r.id}">'
new_tr_ret = 'return `\n          <tr onclick="window.selectReportStudent(\'${r.id}\')" class="transition-colors cursor-pointer ${selectedIndicator}" data-student-id="${r.id}">'
assert old_tr_ret in text, "Could not find old_tr_ret"
text = text.replace(old_tr_ret, new_tr_ret, 1)

# 4. In search filter onSearchInput, reset reportsCurrentPage to 1
old_search_fn = """  window.onSearchInput = function(val) {
    searchQuery = val;
    renderTable();
  };"""

new_search_fn = """  window.onSearchInput = function(val) {
    searchQuery = val;
    reportsCurrentPage = 1;
    renderTable();
  };"""

if old_search_fn in text:
    text = text.replace(old_search_fn, new_search_fn, 1)

# 5. In submitTranscriptUpload, invoke window.NGIS_showOperationSuccess
old_success_handling = """      // Automatically reload persistent server transcripts to update state
      await loadServerTranscripts();
      renderTable();
      renderStudentUploadedView();
      closeUploadTranscriptModal();"""

new_success_handling = """      // Automatically reload persistent server transcripts to update state
      await loadServerTranscripts();
      renderTable();
      renderStudentUploadedView();
      closeUploadTranscriptModal();

      if (window.NGIS_showOperationSuccess) {
        window.NGIS_showOperationSuccess({
          title: 'Report Uploaded Successfully',
          message: `Official transcript document for ${studentName} (${studentId}) has been uploaded and submitted for Principal review.`
        });
      }"""

if old_success_handling in text:
    text = text.replace(old_success_handling, new_success_handling, 1)

with open('pages/teacher/teacher-reports.html', 'w', encoding='utf-8') as f:
    f.write(text)

print('Updated teacher-reports.html successfully!')

with open('pages/student/student-assignments.html', 'r', encoding='utf-8') as f:
    code = f.read()

target_block = '''// Coursework Filtering & Search Controller
(function() {
  window.setCourseFilter = function(courseKey) {
    var activeCourse = (courseKey || 'all').toLowerCase();

    // Update filter buttons
    document.querySelectorAll('.course-filter-btn').forEach(function(btn) {
      var match = btn.getAttribute('data-course') === activeCourse;
      btn.classList.toggle('active', match);
      btn.setAttribute('aria-selected', match ? 'true' : 'false');
    });

    // Filter Task Cards
    var tasks = document.querySelectorAll('.task-card');
    var visibleTasks = 0;
    tasks.forEach(function(card) {
      var c = (card.getAttribute('data-course') || '').toLowerCase();
      var show = (activeCourse === 'all');
      if (!show) {
        if (activeCourse === 'english' && (c.includes('english') || c.includes('literature'))) show = true;
        else if (activeCourse === 'math' && (c.includes('math') || c.includes('calculus'))) show = true;
        else if (activeCourse === 'physics' && (c.includes('physics') || c.includes('mechanics'))) show = true;
        else if (activeCourse === 'history' && c.includes('history')) show = true;
        else if (activeCourse === 'cs' && (c.includes('computer') || c.includes('python'))) show = true;
        else if (c.includes(activeCourse)) show = true;
      }
      card.style.display = show ? '' : 'none';
      if (show) visibleTasks++;
    });

    // Empty state for tasks
    var noTasks = document.getElementById('noTasksState');
    if (noTasks) noTasks.style.display = (visibleTasks === 0) ? 'block' : 'none';

    var tasksBadge = document.getElementById('tasksBadge');
    if (tasksBadge) {
      tasksBadge.textContent = visibleTasks + ' Task' + (visibleTasks === 1 ? '' : 's');
    }

    // Filter Desktop Graded Table Rows
    var tableRows = document.querySelectorAll('#gradedTableBody tr');
    var visibleRows = 0;
    tableRows.forEach(function(row) {
      var subj = (row.getAttribute('data-course') || row.querySelector('td:nth-child(2)')?.textContent || '').toLowerCase();
      var show = (activeCourse === 'all');
      if (!show) {
        if (activeCourse === 'english' && (subj.includes('english') || subj.includes('lit'))) show = true;
        else if (activeCourse === 'math' && (subj.includes('math') || subj.includes('differentiation'))) show = true;
        else if (activeCourse === 'physics' && subj.includes('physics')) show = true;
        else if (activeCourse === 'history' && subj.includes('history')) show = true;
        else if (activeCourse === 'cs' && (subj.includes('computer') || subj.includes('science'))) show = true;
        else if (subj.includes(activeCourse)) show = true;
      }
      row.style.display = show ? '' : 'none';
      if (show) visibleRows++;
    });

    // Filter Mobile Graded Cards
    var mobileItems = document.querySelectorAll('#gradedMobileList .graded-item');
    mobileItems.forEach(function(item) {
      var subj = (item.getAttribute('data-course') || '').toLowerCase();
      var show = (activeCourse === 'all');
      if (!show) {
        if (activeCourse === 'english' && (subj.includes('english') || subj.includes('lit'))) show = true;
        else if (activeCourse === 'math' && (subj.includes('math') || subj.includes('differentiation'))) show = true;
        else if (activeCourse === 'physics' && subj.includes('physics')) show = true;
        else if (activeCourse === 'history' && subj.includes('history')) show = true;
        else if (activeCourse === 'cs' && (subj.includes('computer') || subj.includes('science'))) show = true;
        else if (subj.includes(activeCourse)) show = true;
      }
      item.style.display = show ? '' : 'none';
    });

    // Update footer count text
    var footerCount = document.getElementById('gradedCountText');
    if (footerCount) {
      footerCount.textContent = (activeCourse === 'all')
        ? 'Displaying 4 of 14 graded records'
        : ('Displaying ' + visibleRows + ' record' + (visibleRows === 1 ? '' : 's') + ' for ' + (activeCourse.charAt(0).toUpperCase() + activeCourse.slice(1)));
    }

    // Sync URL search param
    try {
      var u = new URL(window.location.href);
      if (activeCourse === 'all') {
        u.searchParams.delete('dept');
        u.searchParams.delete('subject');
      } else {
        u.searchParams.set('dept', activeCourse);
      }
      window.history.replaceState({}, '', u.toString());
    } catch(e) {}
  };

  // Wire search input
  var searchInput = document.getElementById('asgnSearch');
  if (searchInput) {
    searchInput.addEventListener('input', function(e) {
      var q = (e.target.value || '').toLowerCase().trim();
      var tasks = document.querySelectorAll('.task-card');
      var visibleTasks = 0;
      tasks.forEach(function(card) {
        var text = (card.textContent || '').toLowerCase();
        var show = !q || text.includes(q);
        card.style.display = show ? '' : 'none';
        if (show) visibleTasks++;
      });
      var noTasks = document.getElementById('noTasksState');
      if (noTasks) noTasks.style.display = (visibleTasks === 0) ? 'block' : 'none';
      var tasksBadge = document.getElementById('tasksBadge');
      if (tasksBadge) {
        tasksBadge.textContent = visibleTasks + ' Task' + (visibleTasks === 1 ? '' : 's');
      }
    });
  }'''

replacement_block = '''// Coursework Filtering, Pagination & Search Controller
(function() {
  var currentTasksPage = 1;
  var TASKS_PER_PAGE = 4;
  var currentActiveCourse = 'all';
  var currentSearchQuery = '';

  function getMatchingTasks() {
    var allCards = Array.prototype.slice.call(document.querySelectorAll('.task-card'));
    return allCards.filter(function(card) {
      var c = (card.getAttribute('data-course') || '').toLowerCase();
      var courseMatch = (currentActiveCourse === 'all');
      if (!courseMatch) {
        if (currentActiveCourse === 'english' && (c.includes('english') || c.includes('literature'))) courseMatch = true;
        else if (currentActiveCourse === 'math' && (c.includes('math') || c.includes('calculus') || c.includes('algebra'))) courseMatch = true;
        else if (currentActiveCourse === 'physics' && (c.includes('physics') || c.includes('mechanics'))) courseMatch = true;
        else if (currentActiveCourse === 'history' && c.includes('history')) courseMatch = true;
        else if (currentActiveCourse === 'cs' && (c.includes('computer') || c.includes('python') || c.includes('structures'))) courseMatch = true;
        else if (c.includes(currentActiveCourse)) courseMatch = true;
      }
      if (!courseMatch) return false;

      if (currentSearchQuery) {
        var text = (card.textContent || '').toLowerCase();
        if (!text.includes(currentSearchQuery)) return false;
      }
      return true;
    });
  }

  function updateTasksPagination() {
    var matching = getMatchingTasks();
    var totalTasks = matching.length;
    var totalPages = Math.max(1, Math.ceil(totalTasks / TASKS_PER_PAGE));

    if (currentTasksPage > totalPages) currentTasksPage = totalPages;
    if (currentTasksPage < 1) currentTasksPage = 1;

    var startIdx = (currentTasksPage - 1) * TASKS_PER_PAGE;
    var endIdx = Math.min(startIdx + TASKS_PER_PAGE, totalTasks);

    // Hide all task cards first
    var allCards = document.querySelectorAll('.task-card');
    allCards.forEach(function(card) { card.style.display = 'none'; });

    // Show only the page slice
    matching.slice(startIdx, endIdx).forEach(function(card) {
      card.style.display = '';
    });

    // Empty state & badge
    var noTasks = document.getElementById('noTasksState');
    var paginationBox = document.getElementById('tasksPagination');
    var tasksBadge = document.getElementById('tasksBadge');

    if (noTasks) noTasks.style.display = (totalTasks === 0) ? 'block' : 'none';
    if (paginationBox) paginationBox.style.display = (totalTasks === 0) ? 'none' : 'flex';
    if (tasksBadge) tasksBadge.textContent = totalTasks + ' Task' + (totalTasks === 1 ? '' : 's');

    // Update pagination controls
    var summaryEl = document.getElementById('tasksPaginationSummary');
    var indicatorEl = document.getElementById('tasksPageIndicator');
    var prevBtn = document.getElementById('tasksPrevBtn');
    var nextBtn = document.getElementById('tasksNextBtn');

    if (summaryEl) {
      if (totalTasks === 0) {
        summaryEl.textContent = 'Showing 0 assignments';
      } else {
        summaryEl.textContent = 'Showing ' + (startIdx + 1) + '–' + endIdx + ' of ' + totalTasks + ' assignments';
      }
    }
    if (indicatorEl) {
      indicatorEl.textContent = 'Page ' + currentTasksPage + ' of ' + totalPages;
    }
    if (prevBtn) prevBtn.disabled = (currentTasksPage <= 1);
    if (nextBtn) nextBtn.disabled = (currentTasksPage >= totalPages);
  }

  window.changeTasksPage = function(delta) {
    currentTasksPage += delta;
    updateTasksPagination();
    var list = document.getElementById('tasksList');
    if (list && list.getBoundingClientRect().top < 0) {
      list.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  };

  window.setCourseFilter = function(courseKey) {
    currentActiveCourse = (courseKey || 'all').toLowerCase();
    currentTasksPage = 1; // Reset to page 1 on filter change

    // Update filter buttons
    document.querySelectorAll('.course-filter-btn').forEach(function(btn) {
      var match = btn.getAttribute('data-course') === currentActiveCourse;
      btn.classList.toggle('active', match);
      btn.setAttribute('aria-selected', match ? 'true' : 'false');
    });

    // Update active tasks pagination & display
    updateTasksPagination();

    // Filter Desktop Graded Table Rows (independent completed section)
    var tableRows = document.querySelectorAll('#gradedTableBody tr');
    var visibleRows = 0;
    tableRows.forEach(function(row) {
      var subj = (row.getAttribute('data-course') || row.querySelector('td:nth-child(2)')?.textContent || '').toLowerCase();
      var show = (currentActiveCourse === 'all');
      if (!show) {
        if (currentActiveCourse === 'english' && (subj.includes('english') || subj.includes('lit'))) show = true;
        else if (currentActiveCourse === 'math' && (subj.includes('math') || subj.includes('differentiation'))) show = true;
        else if (currentActiveCourse === 'physics' && subj.includes('physics')) show = true;
        else if (currentActiveCourse === 'history' && subj.includes('history')) show = true;
        else if (currentActiveCourse === 'cs' && (subj.includes('computer') || subj.includes('science'))) show = true;
        else if (subj.includes(currentActiveCourse)) show = true;
      }
      row.style.display = show ? '' : 'none';
      if (show) visibleRows++;
    });

    // Filter Mobile Graded Cards
    var mobileItems = document.querySelectorAll('#gradedMobileList .graded-item');
    mobileItems.forEach(function(item) {
      var subj = (item.getAttribute('data-course') || '').toLowerCase();
      var show = (currentActiveCourse === 'all');
      if (!show) {
        if (currentActiveCourse === 'english' && (subj.includes('english') || subj.includes('lit'))) show = true;
        else if (currentActiveCourse === 'math' && (subj.includes('math') || subj.includes('differentiation'))) show = true;
        else if (currentActiveCourse === 'physics' && subj.includes('physics')) show = true;
        else if (currentActiveCourse === 'history' && subj.includes('history')) show = true;
        else if (currentActiveCourse === 'cs' && (subj.includes('computer') || subj.includes('science'))) show = true;
        else if (subj.includes(currentActiveCourse)) show = true;
      }
      item.style.display = show ? '' : 'none';
    });

    // Update footer count text
    var footerCount = document.getElementById('gradedCountText');
    if (footerCount) {
      footerCount.textContent = (currentActiveCourse === 'all')
        ? 'Displaying 4 of 14 graded records'
        : ('Displaying ' + visibleRows + ' record' + (visibleRows === 1 ? '' : 's') + ' for ' + (currentActiveCourse.charAt(0).toUpperCase() + currentActiveCourse.slice(1)));
    }

    // Sync URL search param
    try {
      var u = new URL(window.location.href);
      if (currentActiveCourse === 'all') {
        u.searchParams.delete('dept');
        u.searchParams.delete('subject');
      } else {
        u.searchParams.set('dept', currentActiveCourse);
      }
      window.history.replaceState({}, '', u.toString());
    } catch(e) {}
  };

  // Wire search input with page reset
  var searchInput = document.getElementById('asgnSearch');
  if (searchInput) {
    searchInput.addEventListener('input', function(e) {
      currentSearchQuery = (e.target.value || '').toLowerCase().trim();
      currentTasksPage = 1;
      updateTasksPagination();
    });
  }

  // Initial pagination load
  updateTasksPagination();'''

if target_block in code:
    new_code = code.replace(target_block, replacement_block)
    with open('pages/student/student-assignments.html', 'w', encoding='utf-8') as f:
        f.write(new_code)
    print('Successfully updated filter and pagination script in student-assignments.html')
else:
    print('Could not find target_block for replacement')

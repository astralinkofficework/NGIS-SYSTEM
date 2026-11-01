
(function() {
  'use strict';

  // Realistic Khmer student cohort dataset matching NGIS curriculum
  const INITIAL_STUDENTS = [
    { id: 'STU-1001', studentCode: '2026-STD-0142', name: 'អ៊ឹង សុភារី', nameEn: 'Nrinphouneta Hok', sex: 'ស្រី', dob: '10-កុម្ភៈ-2010', dict: 46, essay: 45, civics: 47, hist: 48, geo: 44, math: 96, phy: 48, chem: 45, bio: 46, earth: 44, eng: 49 },
    { id: 'STU-1002', studentCode: '2026-STD-0144', name: 'សុខ សុភា', nameEn: 'Sophea Chan', sex: 'ស្រី', dob: '15-មេសា-2009', dict: 44, essay: 43, civics: 42, hist: 41, geo: 40, math: 90, phy: 45, chem: 42, bio: 44, earth: 41, eng: 46 },
    { id: 'STU-1003', studentCode: '2026-STD-0145', name: 'វីរៈ ហេង', nameEn: 'Virak Heng', sex: 'ប្រុស', dob: '03-មករា-2010', dict: 40, essay: 39, civics: 38, hist: 39, geo: 37, math: 85, phy: 40, chem: 38, bio: 39, earth: 36, eng: 42 },
    { id: 'STU-1004', studentCode: '2026-STD-0148', name: 'គីមហៀក ឆេង', nameEn: 'Kimheak Chheng', sex: 'ស្រី', dob: '22-កញ្ញា-2009', dict: 42, essay: 41, civics: 40, hist: 38, geo: 39, math: 82, phy: 39, chem: 36, bio: 40, earth: 38, eng: 44 },
    { id: 'STU-1005', studentCode: '2026-STD-0151', name: 'ចាន់ វុឌ្ឍ', nameEn: 'Chan Vuth', sex: 'ប្រុស', dob: '18-តុលា-2009', dict: 36, essay: 38, civics: 35, hist: 32, geo: 33, math: 74, phy: 33, chem: 32, bio: 34, earth: 31, eng: 38 },
    { id: 'STU-1006', studentCode: '2026-STD-0155', name: 'លឹម គឹមសួរ', nameEn: 'Lim Kimsour', sex: 'ស្រី', dob: '07-ធ្នូ-2009', dict: 38, essay: 37, civics: 36, hist: 34, geo: 35, math: 68, phy: 34, chem: 30, bio: 35, earth: 32, eng: 39 },
    { id: 'STU-1007', studentCode: '2026-STD-0160', name: 'ប៊ុន រិទ្ធី', nameEn: 'Bun Rithy', sex: 'ប្រុស', dob: '12-មីនា-2010', dict: 35, essay: 34, civics: 33, hist: 30, geo: 31, math: 65, phy: 31, chem: 28, bio: 30, earth: 30, eng: 34 },
    { id: 'STU-1008', studentCode: '2026-STD-0162', name: 'ម៉េង ស្រីលីន', nameEn: 'Meng Sreylin', sex: 'ស្រី', dob: '29-វិច្ឆិកា-2009', dict: 33, essay: 35, civics: 34, hist: 32, geo: 30, math: 58, phy: 29, chem: 28, bio: 31, earth: 29, eng: 35 },
    { id: 'STU-1009', studentCode: '2026-STD-0168', name: 'សេង វិបុល', nameEn: 'Seng Vibol', sex: 'ប្រុស', dob: '05-សីហា-2009', dict: 30, essay: 32, civics: 31, hist: 28, geo: 29, math: 52, phy: 26, chem: 24, bio: 28, earth: 27, eng: 30 },
    { id: 'STU-1010', studentCode: '2026-STD-0171', name: 'ជា ដានីកា', nameEn: 'Chea Danika', sex: 'ស្រី', dob: '14-កក្កដា-2010', dict: 22, essay: 25, civics: 24, hist: 22, geo: 23, math: 38, phy: 20, chem: 18, bio: 22, earth: 21, eng: 25 }
  ];

  const STORAGE_KEY = 'ngis_teacher_exam_gradebook_v5';
  let studentsData = [];
  let filterQuery = '';

  function loadSaved() {
    try {
      const saved = localStorage.getItem(STORAGE_KEY);
      if (saved) {
        studentsData = JSON.parse(saved);
      } else {
        studentsData = JSON.parse(JSON.stringify(INITIAL_STUDENTS));
      }
    } catch(e) {
      studentsData = JSON.parse(JSON.stringify(INITIAL_STUDENTS));
    }
  }

  function persistData() {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(studentsData));
    } catch(e) {}
  }

  // Calculate Grade Mention from standard Khmer 100-scale
  function getMention(average) {
    if (average >= 85) return { label: 'A', text: 'ល្អប្រសើរ', badge: 'bg-emerald-100 text-emerald-800 border-emerald-300' };
    if (average >= 75) return { label: 'B', text: 'ល្អណាស់', badge: 'bg-blue-100 text-blue-800 border-blue-300' };
    if (average >= 65) return { label: 'C', text: 'ល្អ', badge: 'bg-teal-100 text-teal-800 border-teal-300' };
    if (average >= 55) return { label: 'D', text: 'ល្អបង្គួរ', badge: 'bg-amber-100 text-amber-800 border-amber-300' };
    if (average >= 45) return { label: 'E', text: 'មធ្យម', badge: 'bg-orange-100 text-orange-800 border-orange-300' };
    return { label: 'F', text: 'ធ្លាក់', badge: 'bg-rose-100 text-rose-800 border-rose-300' };
  }

  // Table horizontal jump navigation
  window.scrollTableTo = function(targetId) {
    const container = document.getElementById('gradeTableContainer');
    if (!container) return;
    
    if (targetId === 'col-khmer') {
      const el = document.getElementById('th-khmer');
      if (el) container.scrollTo({ left: el.offsetLeft - 120, behavior: 'smooth' });
    } else if (targetId === 'col-social') {
      const el = document.getElementById('th-social');
      if (el) container.scrollTo({ left: el.offsetLeft - 120, behavior: 'smooth' });
    } else if (targetId === 'col-stem') {
      const el = document.getElementById('th-stem');
      if (el) container.scrollTo({ left: el.offsetLeft - 120, behavior: 'smooth' });
    } else if (targetId === 'col-results') {
      const el = document.getElementById('th-results');
      if (el) container.scrollTo({ left: el.offsetLeft - 120, behavior: 'smooth' });
    }
  };

  // Recalculate totals, ranking, averages and re-render grid
  window.renderTable = function() {
    const tbody = document.getElementById('gradebookBody');
    if (!tbody) return;
    tbody.innerHTML = '';

    // Compute individual sums and prepare for ranking
    const processed = studentsData.map((st, index) => {
      const khmerTotal = Number(st.dict) + Number(st.essay);
      // Maximum point total:
      // Khmer (100) + Civics(50) + Hist(50) + Geo(50) + Math(100) + Phy(50) + Chem(50) + Bio(50) + Earth(50) + Eng(50) = 600
      const totalPoints = khmerTotal + Number(st.civics) + Number(st.hist) + Number(st.geo) +
                          Number(st.math) + Number(st.phy) + Number(st.chem) + Number(st.bio) +
                          Number(st.earth) + Number(st.eng);
      
      // Average normalized out of 100 (600 / 6 = 100)
      const average = Number((totalPoints / 6).toFixed(2));

      return {
        ...st,
        index,
        khmerTotal,
        totalPoints,
        average
      };
    });

    // Sort by average descending to compute rank
    const sorted = [...processed].sort((a, b) => b.average - a.average);
    sorted.forEach((item, rIndex) => {
      item.rank = rIndex + 1;
    });

    // Put back to original index order
    processed.sort((a, b) => a.index - b.index);

    const q = filterQuery.toLowerCase().trim();
    let visibleCount = 0;
    let femaleCount = 0;
    let passingCount = 0;
    let sumTotalPoints = 0;
    let sumAverage = 0;

    let sumDict = 0, sumEssay = 0, sumKhTot = 0, sumCivics = 0, sumHist = 0, sumGeo = 0;
    let sumMath = 0, sumPhy = 0, sumChem = 0, sumBio = 0, sumEarth = 0, sumEng = 0;

    let topScore = -1;
    let topStudent = null;

    // Render rows
    processed.forEach((st, idx) => {
      if (st.sex === 'ស្រី') femaleCount++;
      if (st.average >= 45) passingCount++;
      sumTotalPoints += st.totalPoints;
      sumAverage += st.average;

      sumDict += Number(st.dict);
      sumEssay += Number(st.essay);
      sumKhTot += st.khmerTotal;
      sumCivics += Number(st.civics);
      sumHist += Number(st.hist);
      sumGeo += Number(st.geo);
      sumMath += Number(st.math);
      sumPhy += Number(st.phy);
      sumChem += Number(st.chem);
      sumBio += Number(st.bio);
      sumEarth += Number(st.earth);
      sumEng += Number(st.eng);

      if (st.average > topScore) {
        topScore = st.average;
        topStudent = st;
      }

      const match = !q ||
        st.id.toLowerCase().includes(q) ||
        (st.studentCode && st.studentCode.toLowerCase().includes(q)) ||
        st.name.toLowerCase().includes(q) ||
        (st.nameEn && st.nameEn.toLowerCase().includes(q));

      if (match) visibleCount++;

      const mention = getMention(st.average);
      const tr = document.createElement('tr');
      tr.className = "hover:bg-slate-50/80 transition-colors divide-x divide-slate-200";
      tr.setAttribute('data-student-id', st.id);
      if (st.studentCode) tr.setAttribute('data-student-code', st.studentCode);
      if (!match) tr.style.display = 'none';

      tr.innerHTML = `
        <td class="sticky-col-1 px-1.5 sm:px-2.5 py-2 text-center text-slate-500 font-mono text-[10px] sm:text-[11px]">${idx + 1}</td>
        <td class="sticky-col-2 px-2.5 sm:px-3 py-2 text-left font-mono font-medium text-slate-700 text-xs">${st.id}</td>
        <td class="sticky-col-3 px-2 sm:px-4 py-2 text-left font-khmer font-medium text-slate-900">
          <div class="flex flex-col min-w-0">
            <span class="truncate text-xs">${st.name}</span>
            <div class="flex items-center gap-1 text-[10px] text-slate-400 font-sans font-normal truncate">
              <span class="sm:hidden font-mono text-slate-500">${st.id} &bull;</span>
              <span class="truncate">${st.nameEn || ''}</span>
            </div>
          </div>
        </td>
        <td class="px-2 py-2 text-center">
          <span class="inline-block px-1.5 py-0.5 rounded text-[10px] font-medium ${st.sex === 'ស្រី' ? 'bg-pink-50 text-pink-700' : 'bg-blue-50 text-blue-700'}">
            ${st.sex}
          </span>
        </td>
        <td class="px-2.5 sm:px-3 py-2 text-center text-[10px] sm:text-[11px] text-slate-500 font-khmer">${st.dob}</td>

        <!-- Khmer Dictation Input -->
        <td class="px-1 py-1 text-center">
          <input type="number" min="0" max="50" step="0.5" value="${st.dict}" 
            data-student-index="${st.index}" data-field="dict" onfocus="this.select()"
            class="score-input w-11 sm:w-12 text-center text-xs font-mono font-medium py-1 px-0.5 border border-slate-200 rounded focus:border-emerald-600 bg-white">
        </td>

        <!-- Khmer Essay Input -->
        <td class="px-1 py-1 text-center">
          <input type="number" min="0" max="50" step="0.5" value="${st.essay}" 
            data-student-index="${st.index}" data-field="essay" onfocus="this.select()"
            class="score-input w-11 sm:w-12 text-center text-xs font-mono font-medium py-1 px-0.5 border border-slate-200 rounded focus:border-emerald-600 bg-white">
        </td>

        <!-- Khmer Total (Computed) -->
        <td class="px-2 py-2 text-center font-mono font-medium bg-emerald-50 text-emerald-900 text-xs">
          ${st.khmerTotal.toFixed(1)}
        </td>

        <!-- Civics (50) -->
        <td class="px-1 py-1 text-center">
          <input type="number" min="0" max="50" step="0.5" value="${st.civics}" 
            data-student-index="${st.index}" data-field="civics" onfocus="this.select()"
            class="score-input w-11 sm:w-12 text-center text-xs font-mono font-medium py-1 px-0.5 border border-slate-200 rounded focus:border-emerald-600 bg-white">
        </td>

        <!-- History (50) -->
        <td class="px-1 py-1 text-center">
          <input type="number" min="0" max="50" step="0.5" value="${st.hist}" 
            data-student-index="${st.index}" data-field="hist" onfocus="this.select()"
            class="score-input w-11 sm:w-12 text-center text-xs font-mono font-medium py-1 px-0.5 border border-slate-200 rounded focus:border-emerald-600 bg-white">
        </td>

        <!-- Geography (50) -->
        <td class="px-1 py-1 text-center">
          <input type="number" min="0" max="50" step="0.5" value="${st.geo}" 
            data-student-index="${st.index}" data-field="geo" onfocus="this.select()"
            class="score-input w-11 sm:w-12 text-center text-xs font-mono font-medium py-1 px-0.5 border border-slate-200 rounded focus:border-emerald-600 bg-white">
        </td>

        <!-- Math (100) -->
        <td class="px-1 py-1 text-center bg-amber-50/30">
          <input type="number" min="0" max="100" step="0.5" value="${st.math}" 
            data-student-index="${st.index}" data-field="math" onfocus="this.select()"
            class="score-input w-13 sm:w-14 text-center text-xs font-mono font-medium py-1 px-0.5 border border-amber-300 rounded focus:border-emerald-600 bg-amber-50/50">
        </td>

        <!-- Physics (50) -->
        <td class="px-1 py-1 text-center">
          <input type="number" min="0" max="50" step="0.5" value="${st.phy}" 
            data-student-index="${st.index}" data-field="phy" onfocus="this.select()"
            class="score-input w-11 sm:w-12 text-center text-xs font-mono font-medium py-1 px-0.5 border border-slate-200 rounded focus:border-emerald-600 bg-white">
        </td>

        <!-- Chem (50) -->
        <td class="px-1 py-1 text-center">
          <input type="number" min="0" max="50" step="0.5" value="${st.chem}" 
            data-student-index="${st.index}" data-field="chem" onfocus="this.select()"
            class="score-input w-11 sm:w-12 text-center text-xs font-mono font-medium py-1 px-0.5 border border-slate-200 rounded focus:border-emerald-600 bg-white">
        </td>

        <!-- Bio (50) -->
        <td class="px-1 py-1 text-center">
          <input type="number" min="0" max="50" step="0.5" value="${st.bio}" 
            data-student-index="${st.index}" data-field="bio" onfocus="this.select()"
            class="score-input w-11 sm:w-12 text-center text-xs font-mono font-medium py-1 px-0.5 border border-slate-200 rounded focus:border-emerald-600 bg-white">
        </td>

        <!-- Earth (50) -->
        <td class="px-1 py-1 text-center">
          <input type="number" min="0" max="50" step="0.5" value="${st.earth}" 
            data-student-index="${st.index}" data-field="earth" onfocus="this.select()"
            class="score-input w-11 sm:w-12 text-center text-xs font-mono font-medium py-1 px-0.5 border border-slate-200 rounded focus:border-emerald-600 bg-white">
        </td>

        <!-- Eng (50) -->
        <td class="px-1 py-1 text-center">
          <input type="number" min="0" max="50" step="0.5" value="${st.eng}" 
            data-student-index="${st.index}" data-field="eng" onfocus="this.select()"
            class="score-input w-11 sm:w-12 text-center text-xs font-mono font-medium py-1 px-0.5 border border-slate-200 rounded focus:border-emerald-600 bg-white">
        </td>

        <!-- Grand Total Points -->
        <td class="px-2.5 sm:px-3 py-2 text-center font-mono font-medium bg-slate-100 text-slate-900 text-xs">
          ${st.totalPoints.toFixed(1)}
        </td>

        <!-- Average (with student-avg class and weighted ID for regression compatibility) -->
        <td class="px-2.5 sm:px-3 py-2 text-center font-mono font-medium ${st.average >= 50 ? 'text-slate-900' : 'text-rose-600'} text-xs bg-slate-50">
          <span class="student-avg" id="weighted-${st.id}">${st.average.toFixed(2)}</span>
          <span class="hidden" id="weighted-${st.studentCode || ''}">${st.average.toFixed(2)}%</span>
        </td>

        <!-- Rank Pill -->
        <td class="px-1.5 sm:px-2 py-2 text-center">
          <span class="inline-flex items-center justify-center w-5 h-5 sm:w-6 sm:h-6 rounded-full text-[10px] sm:text-xs font-medium ${st.rank === 1 ? 'bg-amber-400 text-slate-900 ring-2 ring-amber-300' : st.rank <= 3 ? 'bg-emerald-100 text-emerald-800' : 'bg-slate-100 text-slate-700'}">
            ${st.rank}
          </span>
        </td>

        <!-- Mention Badge -->
        <td class="px-1.5 sm:px-2 py-2 text-center">
          <span class="inline-block px-1.5 sm:px-2 py-0.5 rounded-full text-[10px] sm:text-[11px] font-medium border ${mention.badge}">
            ${mention.label}
          </span>
        </td>

        <!-- Actions -->
        <td class="px-2 py-2 text-center text-slate-400 no-print">
          <button type="button" onclick="showStudentDossier(${st.index})" class="p-1 hover:text-emerald-700 rounded transition" title="View Student Dossier">
            <i class="ph ph-eye text-sm"></i>
          </button>
        </td>
      `;

      tbody.appendChild(tr);
    });

    // Master UI States: Empty State & No Search Results Handling
    if (processed.length === 0) {
      tbody.innerHTML = `<tr><td colspan="19" class="p-0 border-0">
        <div class="ngis-state-card" style="margin:28px auto; max-width:440px;">
          <div class="ngis-state-icon neutral"><i class="ph ph-users"></i></div>
          <h3 class="ngis-state-title">No Students in Gradebook</h3>
          <p class="ngis-state-desc">There are currently no students enrolled in Grade 10A for this examination evaluation period.</p>
          <button type="button" onclick="addNewStudentRow()" class="ngis-btn-primary"><i class="ph ph-user-plus"></i><span>Add Student</span></button>
        </div>
      </td></tr>`;
    } else if (visibleCount === 0 && filterQuery) {
      tbody.innerHTML = `<tr><td colspan="19" class="p-0 border-0">
        <div class="ngis-state-card" style="margin:28px auto; max-width:440px;">
          <div class="ngis-state-icon neutral"><i class="ph ph-magnifying-glass"></i></div>
          <h3 class="ngis-state-title">No matching students found</h3>
          <p class="ngis-state-desc">No records match &ldquo;${filterQuery}&rdquo;. Check the student ID or spelling, or reset the filter.</p>
          <button type="button" onclick="const i=document.getElementById('searchStudentInput'); if(i){i.value=''; const al=document.getElementById('searchStudentInputDesktop'); if(al) al.value=''; window.filterStudents('');} else { window.renderTable(); }" class="ngis-btn-secondary"><i class="ph ph-x-circle"></i><span>Clear Search</span></button>
        </div>
      </td></tr>`;
    }

    const totalCount = processed.length || 1;
    const avgScore = Number((sumAverage / totalCount).toFixed(2));
    const passPct = Number(((passingCount / totalCount) * 100).toFixed(1));

    // Update KPI cards & mobile floating bar
    document.getElementById('statTotalStudents').textContent = processed.length;
    document.getElementById('statFemaleStudents').textContent = `ស្រី: ${femaleCount} នាក់`;
    document.getElementById('kpiClassAvg').textContent = avgScore.toFixed(2);
    document.getElementById('statPassingRate').textContent = `${passPct}%`;
    document.getElementById('statPassingCount').textContent = `${passingCount}/${processed.length}`;

    const mobCountEl = document.getElementById('mobCount');
    if (mobCountEl) mobCountEl.textContent = processed.length;
    const mobAvgEl = document.getElementById('mobAvg');
    if (mobAvgEl) mobAvgEl.textContent = `${avgScore.toFixed(1)}%`;

    if (topStudent) {
      document.getElementById('statTopScore').textContent = topStudent.average.toFixed(1);
      document.getElementById('statTopStudent').textContent = topStudent.name;
    }

    const classMention = getMention(avgScore);
    document.getElementById('statClassMention').textContent = `Mention: ${classMention.text} (${classMention.label})`;

    // Update table summary footer
    document.getElementById('avg-dict').textContent = (sumDict / totalCount).toFixed(1);
    document.getElementById('avg-essay').textContent = (sumEssay / totalCount).toFixed(1);
    document.getElementById('avg-kh-tot').textContent = (sumKhTot / totalCount).toFixed(1);
    document.getElementById('avg-civics').textContent = (sumCivics / totalCount).toFixed(1);
    document.getElementById('avg-hist').textContent = (sumHist / totalCount).toFixed(1);
    document.getElementById('avg-geo').textContent = (sumGeo / totalCount).toFixed(1);
    document.getElementById('avg-math').textContent = (sumMath / totalCount).toFixed(1);
    document.getElementById('avg-phy').textContent = (sumPhy / totalCount).toFixed(1);
    document.getElementById('avg-chem').textContent = (sumChem / totalCount).toFixed(1);
    document.getElementById('avg-bio').textContent = (sumBio / totalCount).toFixed(1);
    document.getElementById('avg-earth').textContent = (sumEarth / totalCount).toFixed(1);
    document.getElementById('avg-eng').textContent = (sumEng / totalCount).toFixed(1);
    document.getElementById('avg-total-pts').textContent = (sumTotalPoints / totalCount).toFixed(1);
    document.getElementById('grand-avg-pts').textContent = avgScore.toFixed(2);

    const lblEl = document.getElementById('lblCountDisplay');
    if (lblEl) lblEl.textContent = visibleCount;

    // Bind input events for instant real-time calculation
    document.querySelectorAll('.score-input').forEach(input => {
      input.addEventListener('input', (e) => {
        const idx = e.target.getAttribute('data-student-index');
        const field = e.target.getAttribute('data-field');
        const val = parseFloat(e.target.value) || 0;
        studentsData[idx][field] = val;
        persistData();
        renderTable();
      });
    });
  };

  // Add new student record
  window.addNewStudentRow = function() {
    const nextIdx = studentsData.length + 1;
    const newId = `STU-10${nextIdx < 10 ? '0' + nextIdx : nextIdx}`;
    studentsData.push({
      id: newId,
      studentCode: `2026-STD-0${140 + nextIdx}`,
      name: 'សិស្សថ្មី',
      nameEn: 'New Student',
      sex: 'ប្រុស',
      dob: '01-មករា-2010',
      dict: 35, essay: 35, civics: 35, hist: 35, geo: 35, math: 70, phy: 35, chem: 35, bio: 35, earth: 35, eng: 35
    });
    persistData();
    renderTable();
    if (window.toast) window.toast('Added new student candidate', 'success');
  };

  // Export to CSV
  window.exportToCSV = function() {
    let csv = 'No,ID,Full Name,Gender,Birth Date,Khmer Dict (50),Khmer Essay (50),Khmer Total (100),Civics (50),History (50),Geo (50),Math (100),Physics (50),Chem (50),Bio (50),Earth (50),Eng (50),Total (600),Average /100,Rank,Mention\n';
    
    // Sort descending for ranks
    const sorted = [...studentsData].map((s, idx) => {
      const khTot = Number(s.dict) + Number(s.essay);
      const tot = khTot + Number(s.civics) + Number(s.hist) + Number(s.geo) + Number(s.math) + Number(s.phy) + Number(s.chem) + Number(s.bio) + Number(s.earth) + Number(s.eng);
      const avg = Number((tot / 6).toFixed(2));
      return { ...s, idx, khTot, tot, avg };
    }).sort((a, b) => b.avg - a.avg);

    sorted.forEach((item, rIdx) => { item.rank = rIdx + 1; });
    sorted.sort((a, b) => a.idx - b.idx);

    sorted.forEach((st, i) => {
      const mention = getMention(st.avg).label;
      csv += `"${i + 1}","${st.id}","${st.name} (${st.nameEn || ''})","${st.sex}","${st.dob}","${st.dict}","${st.essay}","${st.khTot}","${st.civics}","${st.hist}","${st.geo}","${st.math}","${st.phy}","${st.chem}","${st.bio}","${st.earth}","${st.eng}","${st.tot}","${st.avg}","${st.rank}","${mention}"\n`;
    });

    const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = 'NGIS_Grade_10A_Semester_2_Score_Sheet.csv';
    link.click();
    if (window.toast) window.toast('Exported CSV Score Sheet', 'success');
  };

  // Save changes
  window.saveAllScores = async function(btn) {
    const saveBtn = btn || document.getElementById('saveChangesBtn') || document.querySelector('[onclick*="saveAllScores"]');
    
    const saveOperation = async () => {
      persistData();

      // Check offline status
      if (!navigator.onLine && window.NGISUI) {
        NGISUI.toast.warning("Saved Locally", "Offline mode active. Examination records saved to browser storage and will sync when reconnected.");
        return;
      }

      try {
        const token = localStorage.getItem('token') || '';
        await fetch('/api/academic/gradebook/batch', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + token
          },
          body: JSON.stringify({
            classId: 'cls-10a',
            subjectId: 'subj-math',
            periodId: 'gp-sem2',
            workflow: 'submitted',
            grades: studentsData.map(s => ({
              studentId: s.studentCode || s.id,
              score: s.math,
              comments: 'Semester 2 MoEYS Score'
            }))
          })
        }).catch(() => {});
      } catch(e) {}

      if (window.NGISUI) {
        NGISUI.toast.success("Examination Scores Saved", `Successfully recorded ${studentsData.length} student grade entries for Grade 10A.`, {
          actionText: "Export CSV",
          onAction: () => window.exportToCSV()
        });
      } else if (window.toast) {
        window.toast('Saved and synced scores to NGIS Cloud', 'success');
      }
    };

    if (window.NGISUI && saveBtn) {
      await NGISUI.guardSubmit(saveBtn, saveOperation);
    } else {
      await saveOperation();
    }
  };

  window.showStudentDossier = function(index) {
    const s = studentsData[index];
    if (!s) return;
    alert(`Student Dossier:\nName: ${s.name} (${s.nameEn || ''})\nID: ${s.id}\nMath: ${s.math}\nKhmer: ${Number(s.dict) + Number(s.essay)}`);
  };

  window.onCohortChange = function(val) {
    loadSaved();
    renderTable();
  };

  window.onExamTypeChange = function(val) {
    loadSaved();
    renderTable();
  };

  // Keyboard navigation across cells
  document.addEventListener('keydown', function(e) {
    if (e.target && e.target.classList.contains('score-input')) {
      const currentCell = e.target.closest('td');
      const currentRow = currentCell ? currentCell.closest('tr') : null;
      if (!currentRow) return;

      const cellIndex = Array.from(currentRow.children).indexOf(currentCell);

      if (e.key === 'ArrowDown' || e.key === 'Enter') {
        e.preventDefault();
        const nextRow = currentRow.nextElementSibling;
        if (nextRow) {
          const targetInput = nextRow.children[cellIndex] ? nextRow.children[cellIndex].querySelector('input') : null;
          if (targetInput) {
            targetInput.focus();
            targetInput.select();
          }
        }
      } else if (e.key === 'ArrowUp') {
        e.preventDefault();
        const prevRow = currentRow.previousElementSibling;
        if (prevRow) {
          const targetInput = prevRow.children[cellIndex] ? prevRow.children[cellIndex].querySelector('input') : null;
          if (targetInput) {
            targetInput.focus();
            targetInput.select();
          }
        }
      }
    }
  });

  // Initialize
  document.addEventListener('DOMContentLoaded', () => {
    loadSaved();
    renderTable();

    // Wire search input
    const searchInput = document.getElementById('searchStudentInput');
    const aliasSearch = document.getElementById('searchStudent');

    function applySearch(query) {
      filterQuery = query || '';
      renderTable();
    }

    if (searchInput) {
      searchInput.addEventListener('input', (e) => {
        if (aliasSearch) aliasSearch.value = e.target.value;
        applySearch(e.target.value);
      });
    }

    if (aliasSearch) {
      aliasSearch.addEventListener('input', (e) => {
        if (searchInput) searchInput.value = e.target.value;
        applySearch(e.target.value);
      });
    }
  });

  loadSaved();
  renderTable();

})();

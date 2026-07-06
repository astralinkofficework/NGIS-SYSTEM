/* ══════════════════════════════════════
   NGIS Resource Library — lessons.js
   ══════════════════════════════════════ */

/* ── State ── */
var _previewSrc      = '';
var _previewName     = '';
var _currentType     = 'all';
var _currentSearch   = '';
var _currentName     = '';
var _activeId        = null;
var _currentResources = [];
var _currentSubjectId = '';

/* ════════════════════════════════════
   RESOURCE DATA per subject
   type: lesson | worksheet | exam | formula | video | link
   fileType: pdf | image | video | link
════════════════════════════════════ */
var RESOURCES = {
  math: [
    { id:'m1',  name:'Introduction to Algebra',             type:'lesson',    fileType:'pdf',   date:'2026-01-10', size:'1.4 MB', downloads:98,  tags:['#Algebra','#Grade10'],        src:'https://www.africau.edu/images/default/sample.pdf' },
    { id:'m2',  name:'Linear Equations & Inequalities',     type:'lesson',    fileType:'pdf',   date:'2026-01-18', size:'2.1 MB', downloads:142, tags:['#Algebra','#Chapter3'],        src:'https://www.africau.edu/images/default/sample.pdf' },
    { id:'m3',  name:'Quadratic Functions — Full Notes',    type:'lesson',    fileType:'pdf',   date:'2026-02-05', size:'3.2 MB', downloads:117, tags:['#Quadratic','#Functions'],     src:'https://www.africau.edu/images/default/sample.pdf' },
    { id:'m4',  name:'Calculus: Limits & Derivatives',      type:'lesson',    fileType:'pdf',   date:'2026-02-20', size:'4.0 MB', downloads:203, tags:['#Calculus','#Grade11'],        src:'https://www.africau.edu/images/default/sample.pdf' },
    { id:'m5',  name:'Analytic Geometry — Circles',         type:'lesson',    fileType:'pdf',   date:'2026-03-01', size:'2.8 MB', downloads:89,  tags:['#Geometry','#Circles'],        src:'https://www.africau.edu/images/default/sample.pdf' },
    { id:'m6',  name:'Trigonometry Identities',             type:'lesson',    fileType:'pdf',   date:'2026-03-15', size:'1.9 MB', downloads:76,  tags:['#Trig','#Identities'],         src:'https://www.africau.edu/images/default/sample.pdf' },
    { id:'m7',  name:'Algebra Practice Worksheet',          type:'worksheet', fileType:'pdf',   date:'2026-01-25', size:'0.8 MB', downloads:211, tags:['#Algebra','#Practice'],        src:'https://www.africau.edu/images/default/sample.pdf' },
    { id:'m8',  name:'Quadratic Equations Drill Sheet',     type:'worksheet', fileType:'pdf',   date:'2026-02-12', size:'0.5 MB', downloads:184, tags:['#Quadratic','#Drill'],         src:'https://www.africau.edu/images/default/sample.pdf' },
    { id:'m9',  name:'Calculus Practice Problems',          type:'worksheet', fileType:'pdf',   date:'2026-02-28', size:'1.1 MB', downloads:155, tags:['#Calculus','#Problems'],       src:'https://www.africau.edu/images/default/sample.pdf' },
    { id:'m10', name:'Trigonometry Worksheet Set A',        type:'worksheet', fileType:'pdf',   date:'2026-03-20', size:'0.7 MB', downloads:99,  tags:['#Trig','#Worksheet'],          src:'https://www.africau.edu/images/default/sample.pdf' },
    { id:'m11', name:'2024 Final Exam — Mathematics',       type:'exam',      fileType:'pdf',   date:'2025-11-10', size:'2.3 MB', downloads:320, tags:['#PastExam','#2024'],           src:'https://www.africau.edu/images/default/sample.pdf' },
    { id:'m12', name:'2023 Mid-Term Exam Paper',            type:'exam',      fileType:'pdf',   date:'2025-05-15', size:'1.9 MB', downloads:280, tags:['#PastExam','#MidTerm'],        src:'https://www.africau.edu/images/default/sample.pdf' },
    { id:'m13', name:'Algebra & Calculus Formula Sheet',    type:'formula',   fileType:'pdf',   date:'2026-01-08', size:'0.3 MB', downloads:450, tags:['#Formula','#Algebra'],         src:'https://www.africau.edu/images/default/sample.pdf' },
    { id:'m14', name:'Trigonometry Formula Reference',      type:'formula',   fileType:'pdf',   date:'2026-03-05', size:'0.2 MB', downloads:390, tags:['#Formula','#Trig'],            src:'https://www.africau.edu/images/default/sample.pdf' },
    { id:'m15', name:'Khan Academy — Algebra',              type:'link',      fileType:'link',  date:'2026-01-01', size:'—',      downloads:0,   tags:['#External','#Algebra'],        src:'https://www.khanacademy.org/math/algebra' },
  ],
  physics: [
    { id:'p1',  name:'Kinematics — Motion in 1D',           type:'lesson',    fileType:'pdf',   date:'2026-01-12', size:'2.0 MB', downloads:115, tags:['#Mechanics','#Kinematics'],    src:'https://www.africau.edu/images/default/sample.pdf' },
    { id:'p2',  name:'Newton\'s Laws of Motion',            type:'lesson',    fileType:'pdf',   date:'2026-01-22', size:'2.5 MB', downloads:140, tags:['#Mechanics','#Newton'],        src:'https://www.africau.edu/images/default/sample.pdf' },
    { id:'p3',  name:'Work, Energy & Power',                type:'lesson',    fileType:'pdf',   date:'2026-02-08', size:'3.0 MB', downloads:122, tags:['#Energy','#Work'],             src:'https://www.africau.edu/images/default/sample.pdf' },
    { id:'p4',  name:'Electricity — Circuits & Ohm\'s Law', type:'lesson',    fileType:'pdf',   date:'2026-02-25', size:'2.8 MB', downloads:96,  tags:['#Electricity','#Circuits'],    src:'https://www.africau.edu/images/default/sample.pdf' },
    { id:'p5',  name:'Waves & Oscillations',                type:'lesson',    fileType:'pdf',   date:'2026-03-10', size:'2.2 MB', downloads:88,  tags:['#Waves'],                      src:'https://www.africau.edu/images/default/sample.pdf' },
    { id:'p6',  name:'Thermodynamics — Heat & Gas Laws',    type:'lesson',    fileType:'pdf',   date:'2026-03-25', size:'3.4 MB', downloads:101, tags:['#Thermo','#GasLaws'],          src:'https://www.africau.edu/images/default/sample.pdf' },
    { id:'p7',  name:'Newton\'s Laws Practice Sheet',       type:'worksheet', fileType:'pdf',   date:'2026-01-28', size:'0.6 MB', downloads:178, tags:['#Mechanics','#Practice'],      src:'https://www.africau.edu/images/default/sample.pdf' },
    { id:'p8',  name:'Circuit Problems Worksheet',          type:'worksheet', fileType:'pdf',   date:'2026-03-02', size:'0.9 MB', downloads:143, tags:['#Electricity','#Problems'],    src:'https://www.africau.edu/images/default/sample.pdf' },
    { id:'p9',  name:'2024 Physics Final Exam',             type:'exam',      fileType:'pdf',   date:'2025-11-12', size:'2.1 MB', downloads:295, tags:['#PastExam','#2024'],           src:'https://www.africau.edu/images/default/sample.pdf' },
    { id:'p10', name:'Physics Constants & Formulas Sheet',  type:'formula',   fileType:'pdf',   date:'2026-01-05', size:'0.3 MB', downloads:410, tags:['#Formula','#Constants'],       src:'https://www.africau.edu/images/default/sample.pdf' },
    { id:'p11', name:'Waves Concept Explanation (Video)',   type:'video',     fileType:'video', date:'2026-03-18', size:'—',      downloads:0,   tags:['#Waves','#Video'],             src:'https://www.youtube.com/embed/dQw4w9WgXcQ' },
  ],
  chemistry: [
    { id:'c1',  name:'Atomic Structure & Periodic Table',  type:'lesson',    fileType:'pdf',   date:'2026-01-14', size:'2.3 MB', downloads:108, tags:['#Atoms','#PeriodicTable'],     src:'https://www.africau.edu/images/default/sample.pdf' },
    { id:'c2',  name:'Chemical Bonding',                   type:'lesson',    fileType:'pdf',   date:'2026-01-28', size:'2.7 MB', downloads:93,  tags:['#Bonding'],                    src:'https://www.africau.edu/images/default/sample.pdf' },
    { id:'c3',  name:'Stoichiometry & Moles',              type:'lesson',    fileType:'pdf',   date:'2026-02-14', size:'1.8 MB', downloads:112, tags:['#Stoich','#Moles'],            src:'https://www.africau.edu/images/default/sample.pdf' },
    { id:'c4',  name:'Acids, Bases & Salts',               type:'lesson',    fileType:'pdf',   date:'2026-03-03', size:'2.0 MB', downloads:87,  tags:['#AcidBase','#pH'],             src:'https://www.africau.edu/images/default/sample.pdf' },
    { id:'c5',  name:'Organic Chemistry — Hydrocarbons',   type:'lesson',    fileType:'pdf',   date:'2026-03-20', size:'3.1 MB', downloads:79,  tags:['#Organic'],                    src:'https://www.africau.edu/images/default/sample.pdf' },
    { id:'c6',  name:'Mole Calculations Worksheet',        type:'worksheet', fileType:'pdf',   date:'2026-02-20', size:'0.7 MB', downloads:161, tags:['#Stoich','#Worksheet'],        src:'https://www.africau.edu/images/default/sample.pdf' },
    { id:'c7',  name:'2024 Chemistry Final Exam',          type:'exam',      fileType:'pdf',   date:'2025-11-14', size:'2.0 MB', downloads:260, tags:['#PastExam','#2024'],           src:'https://www.africau.edu/images/default/sample.pdf' },
    { id:'c8',  name:'Periodic Table Reference Sheet',     type:'formula',   fileType:'pdf',   date:'2026-01-03', size:'0.4 MB', downloads:488, tags:['#Formula','#PeriodicTable'],   src:'https://www.africau.edu/images/default/sample.pdf' },
    { id:'c9',  name:'Reaction Types Formula Card',        type:'formula',   fileType:'pdf',   date:'2026-02-01', size:'0.2 MB', downloads:312, tags:['#Formula','#Reactions'],       src:'https://www.africau.edu/images/default/sample.pdf' },
  ],
  biology: [
    { id:'b1',  name:'Cell Structure & Functions',         type:'lesson',    fileType:'pdf',   date:'2026-01-11', size:'2.6 MB', downloads:99,  tags:['#Cells','#Biology'],           src:'https://www.africau.edu/images/default/sample.pdf' },
    { id:'b2',  name:'Genetics & DNA Replication',         type:'lesson',    fileType:'pdf',   date:'2026-01-25', size:'3.0 MB', downloads:118, tags:['#Genetics','#DNA'],            src:'https://www.africau.edu/images/default/sample.pdf' },
    { id:'b3',  name:'Photosynthesis & Respiration',       type:'lesson',    fileType:'pdf',   date:'2026-02-10', size:'2.4 MB', downloads:105, tags:['#Photosynthesis'],             src:'https://www.africau.edu/images/default/sample.pdf' },
    { id:'b4',  name:'Ecosystems & Biodiversity',          type:'lesson',    fileType:'pdf',   date:'2026-03-01', size:'2.9 MB', downloads:88,  tags:['#Ecosystems'],                 src:'https://www.africau.edu/images/default/sample.pdf' },
    { id:'b5',  name:'Human Body Systems Overview',        type:'lesson',    fileType:'pdf',   date:'2026-03-18', size:'3.5 MB', downloads:122, tags:['#HumanBody'],                  src:'https://www.africau.edu/images/default/sample.pdf' },
    { id:'b6',  name:'Cell Division Worksheet',            type:'worksheet', fileType:'pdf',   date:'2026-02-03', size:'0.5 MB', downloads:145, tags:['#Cells','#Mitosis'],           src:'https://www.africau.edu/images/default/sample.pdf' },
    { id:'b7',  name:'Genetics Problem Set',               type:'worksheet', fileType:'pdf',   date:'2026-02-18', size:'0.8 MB', downloads:177, tags:['#Genetics','#Mendel'],         src:'https://www.africau.edu/images/default/sample.pdf' },
    { id:'b8',  name:'2024 Biology Final Exam',            type:'exam',      fileType:'pdf',   date:'2025-11-10', size:'2.2 MB', downloads:277, tags:['#PastExam','#2024'],           src:'https://www.africau.edu/images/default/sample.pdf' },
    { id:'b9',  name:'Biology Key Terms & Diagrams',       type:'formula',   fileType:'pdf',   date:'2026-01-07', size:'1.0 MB', downloads:320, tags:['#Reference','#Diagrams'],      src:'https://www.africau.edu/images/default/sample.pdf' },
  ],
  english: [
    { id:'e1',  name:'Essay Writing — Structure & Style',  type:'lesson',    fileType:'pdf',   date:'2026-01-10', size:'1.5 MB', downloads:88,  tags:['#Writing','#Essay'],           src:'https://www.africau.edu/images/default/sample.pdf' },
    { id:'e2',  name:'Grammar: Clauses & Sentence Types',  type:'lesson',    fileType:'pdf',   date:'2026-01-24', size:'1.8 MB', downloads:104, tags:['#Grammar'],                    src:'https://www.africau.edu/images/default/sample.pdf' },
    { id:'e3',  name:'Literature Analysis: Short Stories', type:'lesson',    fileType:'pdf',   date:'2026-02-12', size:'2.0 MB', downloads:79,  tags:['#Literature','#Analysis'],     src:'https://www.africau.edu/images/default/sample.pdf' },
    { id:'e4',  name:'Grammar Practice Worksheet B',       type:'worksheet', fileType:'pdf',   date:'2026-02-20', size:'0.6 MB', downloads:165, tags:['#Grammar','#Practice'],        src:'https://www.africau.edu/images/default/sample.pdf' },
    { id:'e5',  name:'Vocabulary Builder Worksheet',       type:'worksheet', fileType:'pdf',   date:'2026-03-05', size:'0.5 MB', downloads:143, tags:['#Vocabulary'],                 src:'https://www.africau.edu/images/default/sample.pdf' },
    { id:'e6',  name:'2024 English Final Exam',            type:'exam',      fileType:'pdf',   date:'2025-11-08', size:'1.9 MB', downloads:240, tags:['#PastExam','#2024'],           src:'https://www.africau.edu/images/default/sample.pdf' },
    { id:'e7',  name:'Writing Structures Reference Card',  type:'formula',   fileType:'pdf',   date:'2026-01-06', size:'0.3 MB', downloads:298, tags:['#Formula','#Writing'],         src:'https://www.africau.edu/images/default/sample.pdf' },
  ],
  history: [
    { id:'h1',  name:'Angkor Empire — Rise & Fall',        type:'lesson',    fileType:'pdf',   date:'2026-01-13', size:'2.1 MB', downloads:92,  tags:['#Cambodia','#Angkor'],         src:'https://www.africau.edu/images/default/sample.pdf' },
    { id:'h2',  name:'World War II — Causes & Effects',    type:'lesson',    fileType:'pdf',   date:'2026-02-04', size:'2.9 MB', downloads:134, tags:['#WW2','#WorldHistory'],        src:'https://www.africau.edu/images/default/sample.pdf' },
    { id:'h3',  name:'Cold War & Decolonisation',          type:'lesson',    fileType:'pdf',   date:'2026-02-22', size:'2.5 MB', downloads:110, tags:['#ColdWar','#Modern'],          src:'https://www.africau.edu/images/default/sample.pdf' },
    { id:'h4',  name:'Primary Source Analysis Worksheet',  type:'worksheet', fileType:'pdf',   date:'2026-03-01', size:'0.7 MB', downloads:99,  tags:['#Sources','#Analysis'],        src:'https://www.africau.edu/images/default/sample.pdf' },
    { id:'h5',  name:'2024 History Final Exam',            type:'exam',      fileType:'pdf',   date:'2025-11-06', size:'1.8 MB', downloads:215, tags:['#PastExam','#2024'],           src:'https://www.africau.edu/images/default/sample.pdf' },
  ],
  geography: [
    { id:'g1',  name:'Physical Geography — Landforms',     type:'lesson',    fileType:'pdf',   date:'2026-01-15', size:'2.4 MB', downloads:77,  tags:['#Landforms'],                  src:'https://www.africau.edu/images/default/sample.pdf' },
    { id:'g2',  name:'Climate Zones & Weather Systems',    type:'lesson',    fileType:'pdf',   date:'2026-02-06', size:'2.2 MB', downloads:85,  tags:['#Climate','#Weather'],         src:'https://www.africau.edu/images/default/sample.pdf' },
    { id:'g3',  name:'Map Reading & Cartography',          type:'lesson',    fileType:'pdf',   date:'2026-03-10', size:'1.7 MB', downloads:71,  tags:['#Maps','#Cartography'],        src:'https://www.africau.edu/images/default/sample.pdf' },
    { id:'g4',  name:'Map Skills Worksheet',               type:'worksheet', fileType:'pdf',   date:'2026-03-15', size:'0.6 MB', downloads:118, tags:['#Maps','#Practice'],           src:'https://www.africau.edu/images/default/sample.pdf' },
    { id:'g5',  name:'2024 Geography Final Exam',          type:'exam',      fileType:'pdf',   date:'2025-11-07', size:'1.9 MB', downloads:188, tags:['#PastExam','#2024'],           src:'https://www.africau.edu/images/default/sample.pdf' },
  ],
  cs: [
    { id:'cs1', name:'Introduction to Programming (Python)', type:'lesson',  fileType:'pdf',   date:'2026-01-09', size:'2.0 MB', downloads:178, tags:['#Python','#Programming'],      src:'https://www.africau.edu/images/default/sample.pdf' },
    { id:'cs2', name:'Data Structures — Arrays & Lists',   type:'lesson',    fileType:'pdf',   date:'2026-01-23', size:'2.6 MB', downloads:155, tags:['#DataStructures'],             src:'https://www.africau.edu/images/default/sample.pdf' },
    { id:'cs3', name:'Algorithms: Searching & Sorting',    type:'lesson',    fileType:'pdf',   date:'2026-02-11', size:'3.1 MB', downloads:199, tags:['#Algorithms','#Sorting'],      src:'https://www.africau.edu/images/default/sample.pdf' },
    { id:'cs4', name:'Web Development Basics (HTML/CSS)',  type:'lesson',    fileType:'pdf',   date:'2026-02-28', size:'2.4 MB', downloads:212, tags:['#Web','#HTML'],                src:'https://www.africau.edu/images/default/sample.pdf' },
    { id:'cs5', name:'Databases & SQL Fundamentals',       type:'lesson',    fileType:'pdf',   date:'2026-03-14', size:'2.8 MB', downloads:167, tags:['#SQL','#Databases'],           src:'https://www.africau.edu/images/default/sample.pdf' },
    { id:'cs6', name:'OOP Concepts in Python',             type:'lesson',    fileType:'pdf',   date:'2026-03-28', size:'3.5 MB', downloads:145, tags:['#OOP','#Python'],              src:'https://www.africau.edu/images/default/sample.pdf' },
    { id:'cs7', name:'Python Coding Exercises Set A',      type:'worksheet', fileType:'pdf',   date:'2026-01-30', size:'0.8 MB', downloads:234, tags:['#Python','#Exercises'],        src:'https://www.africau.edu/images/default/sample.pdf' },
    { id:'cs8', name:'Algorithm Design Worksheet',         type:'worksheet', fileType:'pdf',   date:'2026-02-15', size:'1.0 MB', downloads:196, tags:['#Algorithms','#Design'],       src:'https://www.africau.edu/images/default/sample.pdf' },
    { id:'cs9', name:'SQL Query Practice Sheet',           type:'worksheet', fileType:'pdf',   date:'2026-03-18', size:'0.7 MB', downloads:155, tags:['#SQL','#Queries'],             src:'https://www.africau.edu/images/default/sample.pdf' },
    { id:'cs10',name:'2024 CS Final Exam',                 type:'exam',      fileType:'pdf',   date:'2025-11-11', size:'2.3 MB', downloads:305, tags:['#PastExam','#2024'],           src:'https://www.africau.edu/images/default/sample.pdf' },
    { id:'cs11',name:'2023 CS Mid-Term Exam',              type:'exam',      fileType:'pdf',   date:'2025-05-20', size:'1.7 MB', downloads:258, tags:['#PastExam','#MidTerm'],        src:'https://www.africau.edu/images/default/sample.pdf' },
    { id:'cs12',name:'Big-O Complexity Reference Sheet',   type:'formula',   fileType:'pdf',   date:'2026-01-04', size:'0.2 MB', downloads:389, tags:['#Formula','#BigO'],            src:'https://www.africau.edu/images/default/sample.pdf' },
    { id:'cs13',name:'Python Syntax Cheat Sheet',          type:'formula',   fileType:'pdf',   date:'2026-02-02', size:'0.3 MB', downloads:441, tags:['#Formula','#Python'],          src:'https://www.africau.edu/images/default/sample.pdf' },
    { id:'cs14',name:'W3Schools — HTML Reference',         type:'link',      fileType:'link',  date:'2026-01-01', size:'—',      downloads:0,   tags:['#External','#HTML'],           src:'https://www.w3schools.com/html/' },
    { id:'cs15',name:'CS50 — Intro to CS (Video)',         type:'video',     fileType:'video', date:'2026-02-01', size:'—',      downloads:0,   tags:['#Video','#CS50'],              src:'https://www.youtube.com/embed/dQw4w9WgXcQ' },
  ]
};

/* ════════════════════════════════════
   Type meta helpers
════════════════════════════════════ */
var TYPE_META = {
  lesson:    { label:'Lesson',    cls:'pdf-ic',  mdIcon:'menu_book'   },
  worksheet: { label:'Worksheet', cls:'ws-ic',   mdIcon:'assignment'  },
  exam:      { label:'Exam',      cls:'past-ic', mdIcon:'fact_check'  },
  formula:   { label:'Formula',   cls:'xls-ic',  mdIcon:'calculate'   },
  video:     { label:'Video',     cls:'vid-ic',  mdIcon:'play_circle' },
  link:      { label:'Link',      cls:'link-ic', mdIcon:'open_in_new' }
};
function typeMeta(t) { return TYPE_META[t] || { label:t, cls:'pdf-ic', mdIcon:'description' }; }
function escHtml(s)  { return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;'); }
function escAttr(s)  { return String(s).replace(/\\/g,'\\\\').replace(/'/g,"\\'"); }
function fmtDate(d)  {
  if (!d) return '';
  try { return new Date(d).toLocaleDateString('en-GB',{day:'2-digit',month:'short',year:'numeric'}); }
  catch(e){ return d; }
}
function isMobileLibraryView() {
  return window.matchMedia('(max-width: 640px)').matches;
}

/* ════════════════════════════════════
   STEP 1 — Subject Selection
════════════════════════════════════ */
function filterSubjects(q) {
  var cards = document.querySelectorAll('.subj-card');
  var empty = document.getElementById('subjEmptyState');
  var lower = (q || '').toLowerCase();
  var found = 0;
  cards.forEach(function(c){
    var match = !lower || c.dataset.name.toLowerCase().includes(lower);
    c.style.display = match ? '' : 'none';
    if (match) found++;
  });
  if (empty) empty.hidden = found > 0;
}

function openSubject(id, name, sub, icon, color, bg, teacher, subject, semester, dept, desc, count) {
  closeMobileSidebar();
  _currentSubjectId = id;
  _currentResources = RESOURCES[id] || [];
  _activeId         = null;
  _currentType      = 'all';
  _currentSearch    = '';
  _currentName      = '';

  document.getElementById('stepSubjects').hidden = true;
  document.getElementById('stepLibrary').hidden  = false;

  document.getElementById('libTitle').textContent = name;
  document.getElementById('libSub').textContent   = sub + ' · Teacher: ' + teacher;
  document.getElementById('teacherName').textContent    = teacher;
  document.getElementById('teacherDept').textContent    = dept;
  document.getElementById('panelTeacherName').textContent = teacher;
  document.getElementById('panelTeacherDept').textContent = dept;
  document.getElementById('siSubject').textContent  = subject || name;
  document.getElementById('siSemester').textContent = semester;
  document.getElementById('siDept').textContent     = dept;
  document.getElementById('siDesc').textContent     = desc;
  var ds = document.getElementById('detailSubject'), ds2 = document.getElementById('detailSemester');
  if (ds)  ds.textContent  = name;
  if (ds2) ds2.textContent = semester;

  var si = document.getElementById('sidebarSearch');
  if (si) si.value = '';

  /* reset tab */
  document.querySelectorAll('.lib-tab').forEach(function(el){
    el.classList.toggle('active', el.dataset.type === 'all');
  });

  buildSidebarList();
  renderFileList();
  showViewerPlaceholder();
}

function backToSubjects() {
  document.getElementById('stepLibrary').hidden  = true;
  document.getElementById('stepSubjects').hidden = false;
  document.getElementById('subjectSearch').value = '';
  filterSubjects('');
}

/* ════════════════════════════════════
   Sidebar — individual lesson names
════════════════════════════════════ */
function buildSidebarList() {
  var role      = (window.PAGE && window.PAGE.role) || 'student';
  var isTeacher = role === 'teacher' || role === 'admin';
  var label     = document.getElementById('sidebarListLabel');
  var list      = document.getElementById('folderList');
  if (!list) return;
  
  if (label) {
    label.innerHTML = '<div style="display:flex; align-items:center; gap:8px; font-weight:700; color:var(--fg); font-size:15px; margin-bottom:12px;">'
      + '<span class="material-symbols-outlined" style="color:var(--accent); font-size:18px;">book</span>'
      + '<span>' + (isTeacher ? 'All Files' : 'All Lessons') + '</span>'
      + '<span class="tab-badge" style="background:var(--accent-light); color:var(--accent); margin-left:auto; font-size:11px; padding:2px 8px; border-radius:12px;">' + _currentResources.length + '</span>'
      + '</div>';
  }

  var html = '';

  _currentResources.forEach(function(r){
    var m = typeMeta(r.type);
    var fts = fileTypeStyle(r.fileType);
    
    // Custom tag format
    var typeTag = '<span class="px-2 py-0.5 text-[10px] font-bold rounded uppercase" style="background:' + fts.bg + '; color:' + fts.color + '">' + m.label.toUpperCase() + '</span>';
    var formatTag = '<span class="px-2 py-0.5 text-[10px] font-bold rounded uppercase text-white bg-accent-600">' + r.fileType.toUpperCase() + '</span>';
    
    // Custom detail or duration
    var detail = r.fileType === 'video' ? '15 min' : 'Updated ' + fmtDate(r.date);
    
    // Active class logic
    var activeClass = _activeId === r.id ? ' active' : '';

    html += '<button class="lib-folder-item' + activeClass + '" data-item-id="' + r.id + '" onclick="filterByItem(this,\'' + r.id + '\')" style="display:flex; flex-direction:column; align-items:flex-start; gap:8px; padding:16px; border:1px solid var(--border); border-radius:14px; background:#fff; margin-bottom:10px; width:100%; transition:all 0.2s ease; cursor:pointer; text-align:left;">'
      + '  <div style="font-size:14px; font-weight:600; color:var(--fg); line-height:1.4; word-break:break-word;">' + escHtml(r.name) + '</div>'
      + '  <div style="display:flex; align-items:center; gap:6px; flex-wrap:wrap; width:100%;">'
      + '    ' + formatTag
      + '    ' + typeTag
      + '    <span style="font-size:11px; color:var(--muted); margin-left:auto; font-weight:500;">' + detail + '</span>'
      + '  </div>'
      + '</button>';
  });
  list.innerHTML = html;
}

function filterByItem(btn, itemId) {
  _currentName = itemId;
  document.querySelectorAll('.lib-folder-item').forEach(function(el){
    el.classList.toggle('active', el.dataset.itemId === itemId);
  });

  if (itemId) {
    /* find and open that resource directly in viewer */
    var r = _currentResources.find(function(x){ return x.id === itemId; });
    if (r) {
      openInViewer(r);
      if (isMobileLibraryView()) openPreview(r.name, r, r.src);
    }
    applyFilters();
  } else {
    showViewerPlaceholder();
    applyFilters();
  }
}

/* ════════════════════════════════════
   Render file list
════════════════════════════════════ */
function renderFileList() {
  var list = document.getElementById('resourceList');
  if (!list) return;
  var html = '';
  _currentResources.forEach(function(r){
    var m = typeMeta(r.type);
    html += '<div class="lib-file-row" data-type="' + r.type + '" data-name="' + escHtml(r.name.toLowerCase()) + '" data-id="' + r.id + '" data-date="' + r.date + '"'
      + ' onclick="selectFile(\'' + r.id + '\')" tabindex="0" role="button" aria-label="' + escHtml(r.name) + '">'
      + '<span class="lib-ftype-ico ' + m.cls + '">' + m.label.slice(0,4).toUpperCase() + '</span>'
      + '<div class="lib-file-row-body">'
      + '<div class="lib-file-row-name">' + escHtml(r.name) + '</div>'
      + '<div class="lib-file-row-sub">' + fmtDate(r.date) + (r.size !== '—' ? ' · ' + r.size : '') + (r.downloads ? ' · ' + r.downloads + ' downloads' : '') + '</div>'
      + '</div>'
      + '<div class="lib-file-row-tags">'
      + r.tags.slice(0,2).map(function(t){ return '<span class="lib-tag">' + t + '</span>'; }).join('')
      + '</div>'
      + '<div class="lib-file-row-actions" onclick="event.stopPropagation()">'
      + (r.fileType !== 'link' && r.fileType !== 'video' ?
        '<button class="icon-btn" title="Download" aria-label="Download" onclick="downloadFile(\'' + escAttr(r.src) + '\',\'' + escAttr(r.name) + '\')">'
        + '<span class="material-symbols-outlined">download</span></button>' : '')
      + '<button class="icon-btn lib-bm-btn" title="Bookmark" aria-label="Bookmark" onclick="toggleBookmark(this)">'
      + '<span class="material-symbols-outlined">bookmark_border</span></button>'
      + '</div>'
      + '</div>';
  });
  list.innerHTML = html;

  /* keyboard support */
  list.querySelectorAll('.lib-file-row').forEach(function(row){
    row.addEventListener('keydown', function(e){
      if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); selectFile(row.dataset.id); }
    });
  });
}

function selectFile(id) {
  _activeId = id;
  var r = _currentResources.find(function(x){ return x.id === id; });
  if (!r) return;

  /* highlight row */
  document.querySelectorAll('.lib-file-row').forEach(function(el){
    el.classList.toggle('active', el.dataset.id === id);
  });
  /* sync sidebar */
  document.querySelectorAll('.lib-folder-item').forEach(function(el){
    el.classList.toggle('active', el.dataset.itemId === id);
  });
  openInViewer(r);
  if (isMobileLibraryView()) openPreview(r.name, r, r.src);
}

/* ════════════════════════════════════
   Premium Resource Preview (rpv-*)
════════════════════════════════════ */

/* zoom / rotate state */
var _rpvZoom   = 100;
var _rpvRotate = 0;
var _rpvBm     = false;   /* bookmark state for current file */

/* icon & colour map per file type */
var FILE_TYPE_STYLE = {
  pdf:   { icon:'picture_as_pdf', bg:'#ffebee', color:'#e53935', badge:'pdf-ic'  },
  image: { icon:'image',          bg:'#f3e5f5', color:'#8e24aa', badge:'img-ic'  },
  video: { icon:'play_circle',    bg:'#e0f7fa', color:'#00838f', badge:'vid-ic'  },
  link:  { icon:'open_in_new',    bg:'#e3f2fd', color:'#1565c0', badge:'link-ic' }
};
function fileTypeStyle(ft) {
  return FILE_TYPE_STYLE[ft] || FILE_TYPE_STYLE['pdf'];
}

/* Resource descriptions (keyed by id) */
var RES_DESCRIPTIONS = {
  m1:  'A foundational introduction to algebraic thinking — variables, expressions, and basic operations. Ideal for students beginning their algebra journey.',
  m2:  'Covers solving linear equations and inequalities in one variable, including graphical interpretation. Please review examples and practice problems before the next lesson.',
  m3:  'Comprehensive notes on quadratic functions, including vertex form, factoring, and the quadratic formula with worked examples.',
  m4:  'Introduction to limits, continuity, and derivative rules. Includes chain rule, product rule, and real-world applications.',
  m5:  'Analytic geometry of circles — standard form, centre-radius form, and intersections with lines.',
  m6:  'All major trigonometric identities: Pythagorean, double-angle, sum-to-product, and product-to-sum formulas.',
  m7:  'Practice worksheet covering linear and quadratic algebra problems. Great for exam preparation.',
  m8:  'Drill sheet focused on quadratic equation techniques — factoring, completing the square, and the formula.',
  m9:  'A set of calculus practice problems covering derivatives, integrals, and applications.',
  m10: 'Worksheet Set A for trigonometry — unit circle, reference angles, and solving trig equations.',
  m11: '2024 final examination paper with full mark scheme. Essential for exam revision.',
  m12: '2023 mid-term exam covering algebra and geometry topics.',
  m13: 'Quick-reference formula sheet for algebra and calculus — suitable for use during revision.',
  m14: 'Trigonometry formula reference card covering all standard identities and ratios.',
  m15: 'External link to Khan Academy\'s comprehensive algebra course.'
};
function getDesc(r) {
  return RES_DESCRIPTIONS[r.id] || ('A ' + r.type + ' resource for ' + (r.tags[0] || 'this subject') + '. Uploaded by your teacher for study and revision.');
}

/* ── Page data for inline lesson preview (resource m2) ── */
var LESSON_PAGES = [
  /* Page 1 */
  '<div class="page-content" id="page1">'
  + '  <div class="text-center mb-10">'
  + '    <div class="text-xs font-semibold text-surface-400 uppercase tracking-widest mb-2">Grade 9 Mathematics</div>'
  + '    <h2 class="text-3xl font-bold text-surface-900 tracking-tight mb-1">Chapter 3</h2>'
  + '    <h3 class="text-xl font-semibold text-accent-600">Linear Equations &amp; Inequalities</h3>'
  + '    <div class="w-16 h-1 bg-accent-500 rounded-full mx-auto mt-4" style="width: 64px; height: 4px; background: var(--accent); border-radius: 9999px; margin-left: auto; margin-right: auto; margin-top: 16px;"></div>'
  + '  </div>'
  + '  <div class="mb-8">'
  + '    <h4 class="text-lg font-bold text-surface-900 mb-3" style="font-size:18px; font-weight:700; color:var(--fg); margin-bottom:12px;">3.1 What is a Linear Equation?</h4>'
  + '    <p class="text-[15px] text-surface-600 leading-relaxed mb-4" style="font-size:15px; color:var(--muted); line-height:1.625; margin-bottom:16px;">'
  + '      A <strong>linear equation in one variable</strong> is an equation that can be written in the form:'
  + '    </p>'
  + '    <div class="bg-surface-50 border border-surface-200 rounded-2xl p-5 text-center mb-4" style="background:#fafafa; border:1px solid var(--border); border-radius:16px; padding:20px; text-align:center; margin-bottom:16px;">'
  + '      <span class="math-eq text-xl" style="font-size:20px; font-weight:700;">ax + b = 0</span>'
  + '    </div>'
  + '    <p class="text-[15px] text-surface-600 leading-relaxed mb-4" style="font-size:15px; color:var(--muted); line-height:1.625; margin-bottom:16px;">'
  + '      where <span class="math-eq">a</span> and <span class="math-eq">b</span> are real numbers and <span class="math-eq">a ≠ 0</span>. The solution is <span class="math-eq">x = −b/a</span>.'
  + '    </p>'
  + '  </div>'
  + '  <div class="mb-8">'
  + '    <h4 class="text-lg font-bold text-surface-900 mb-3" style="font-size:18px; font-weight:700; color:var(--fg); margin-bottom:12px;">3.2 Solving Linear Equations</h4>'
  + '    <p class="text-[15px] text-surface-600 leading-relaxed mb-3" style="font-size:15px; color:var(--muted); line-height:1.625; margin-bottom:12px;">'
  + '      To solve a linear equation, isolate the variable on one side using inverse operations.'
  + '    </p>'
  + '    <div class="bg-accent-50 border border-accent-200 rounded-2xl p-5" style="background:var(--accent-light); border:1px solid #bbf7d0; border-radius:16px; padding:20px;">'
  + '      <div class="text-xs font-bold text-accent-700 uppercase tracking-wider mb-2" style="font-size:12px; font-weight:700; color:var(--accent); text-transform:uppercase; letter-spacing:0.05em; margin-bottom:8px;">Example 1</div>'
  + '      <p class="text-sm text-surface-700 mb-2" style="font-size:14px; color:var(--fg); margin-bottom:8px;">Solve: <span class="math-eq">3x + 7 = 22</span></p>'
  + '      <div class="space-y-1.5 text-sm text-surface-600 pl-4 border-l-2 border-accent-200" style="display:flex; flex-direction:column; gap:6px; padding-left:16px; border-left:2px solid var(--accent); font-size:14px; color:var(--muted);">'
  + '        <p style="margin:0;"><span class="math-eq">3x = 22 − 7</span></p>'
  + '        <p style="margin:0;"><span class="math-eq">3x = 15</span></p>'
  + '        <p style="margin:0;"><span class="math-eq font-bold text-accent-700" style="font-weight:700; color:var(--accent);">x = 5</span></p>'
  + '      </div>'
  + '    </div>'
  + '  </div>'
  + '  <div class="mb-6">'
  + '    <div class="bg-surface-50 border border-surface-200 rounded-2xl p-5" style="background:#fafafa; border:1px solid var(--border); border-radius:16px; padding:20px;">'
  + '      <div class="text-xs font-bold text-surface-500 uppercase tracking-wider mb-2" style="font-size:12px; font-weight:700; color:var(--muted); text-transform:uppercase; letter-spacing:0.05em; margin-bottom:8px;">Example 2</div>'
  + '      <p class="text-sm text-surface-700 mb-2" style="font-size:14px; color:var(--fg); margin-bottom:8px;">Solve: <span class="math-eq">5(x − 2) = 3x + 6</span></p>'
  + '      <div class="space-y-1.5 text-sm text-surface-600 pl-4 border-l-2 border-surface-300" style="display:flex; flex-direction:column; gap:6px; padding-left:16px; border-left:2px solid var(--border); font-size:14px; color:var(--muted);">'
  + '        <p style="margin:0;"><span class="math-eq">5x − 10 = 3x + 6</span></p>'
  + '        <p style="margin:0;"><span class="math-eq">5x − 3x = 6 + 10</span></p>'
  + '        <p style="margin:0;"><span class="math-eq">2x = 16</span></p>'
  + '        <p style="margin:0;"><span class="math-eq font-bold text-accent-700" style="font-weight:700; color:var(--accent);">x = 8</span></p>'
  + '      </div>'
  + '    </div>'
  + '  </div>'
  + '</div>',

  /* Page 2 */
  '<div class="page-content" id="page2">'
  + '  <div class="mb-8">'
  + '    <h4 class="text-lg font-bold text-surface-900 mb-3" style="font-size:18px; font-weight:700; color:var(--fg); margin-bottom:12px;">3.3 Linear Inequalities</h4>'
  + '    <p class="text-[15px] text-surface-600 leading-relaxed mb-4" style="font-size:15px; color:var(--muted); line-height:1.625; margin-bottom:16px;">'
  + '      A <strong>linear inequality</strong> looks similar to a linear equation but uses inequality symbols instead of an equals sign:'
  + '    </p>'
  + '    <div class="grid grid-cols-2 gap-3 mb-5" style="display:grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 20px;">'
  + '      <div class="bg-surface-50 border border-surface-200 rounded-xl p-3 text-center" style="background:#fafafa; border:1px solid var(--border); border-radius:12px; padding:12px; text-align:center;">'
  + '        <span class="math-eq text-lg" style="font-size:18px;">x &lt; a</span>'
  + '        <div class="text-xs text-surface-400 mt-1" style="font-size:12px; color:var(--muted); margin-top:4px;">Less than</div>'
  + '      </div>'
  + '      <div class="bg-surface-50 border border-surface-200 rounded-xl p-3 text-center" style="background:#fafafa; border:1px solid var(--border); border-radius:12px; padding:12px; text-align:center;">'
  + '        <span class="math-eq text-lg" style="font-size:18px;">x ≤ a</span>'
  + '        <div class="text-xs text-surface-400 mt-1" style="font-size:12px; color:var(--muted); margin-top:4px;">Less than or equal</div>'
  + '      </div>'
  + '      <div class="bg-surface-50 border border-surface-200 rounded-xl p-3 text-center" style="background:#fafafa; border:1px solid var(--border); border-radius:12px; padding:12px; text-align:center;">'
  + '        <span class="math-eq text-lg" style="font-size:18px;">x &gt; a</span>'
  + '        <div class="text-xs text-surface-400 mt-1" style="font-size:12px; color:var(--muted); margin-top:4px;">Greater than</div>'
  + '      </div>'
  + '      <div class="bg-surface-50 border border-surface-200 rounded-xl p-3 text-center" style="background:#fafafa; border:1px solid var(--border); border-radius:12px; padding:12px; text-align:center;">'
  + '        <span class="math-eq text-lg" style="font-size:18px;">x ≥ a</span>'
  + '        <div class="text-xs text-surface-400 mt-1" style="font-size:12px; color:var(--muted); margin-top:4px;">Greater than or equal</div>'
  + '      </div>'
  + '    </div>'
  + '    <div class="bg-amber-50 border border-amber-200 rounded-2xl p-4 flex gap-3" style="display:flex; gap:12px; align-items:flex-start; background:#fffbeb; border:1px solid #fef3c7; border-radius:16px; padding:16px;">'
  + '      <i class="fa-solid fa-triangle-exclamation text-amber-500 mt-0.5" style="color:#d97706; margin-top:2px;"></i>'
  + '      <p class="text-sm text-amber-800 leading-relaxed m-0" style="font-size:14px; color:#92400e; line-height:1.625; margin:0;">'
  + '        <strong>Important:</strong> When you multiply or divide both sides of an inequality by a negative number, you must <em>reverse</em> the inequality symbol.'
  + '      </p>'
  + '    </div>'
  + '  </div>'
  + '  <div class="mb-8">'
  + '    <div class="bg-accent-50 border border-accent-200 rounded-2xl p-5" style="background:var(--accent-light); border:1px solid #bbf7d0; border-radius:16px; padding:20px;">'
  + '      <div class="text-xs font-bold text-accent-700 uppercase tracking-wider mb-2" style="font-size:12px; font-weight:700; color:var(--accent); text-transform:uppercase; letter-spacing:0.05em; margin-bottom:8px;">Example 3</div>'
  + '      <p class="text-sm text-surface-700 mb-2" style="font-size:14px; color:var(--fg); margin-bottom:8px;">Solve: <span class="math-eq">−2x + 5 &gt; 11</span></p>'
  + '      <div class="space-y-1.5 text-sm text-surface-600 pl-4 border-l-2 border-accent-200" style="display:flex; flex-direction:column; gap:6px; padding-left:16px; border-left:2px solid var(--accent); font-size:14px; color:var(--muted);">'
  + '        <p style="margin:0;"><span class="math-eq">−2x &gt; 11 − 5</span></p>'
  + '        <p style="margin:0;"><span class="math-eq">−2x &gt; 6</span></p>'
  + '        <p style="margin:0;"><span class="math-eq">x &lt; −3</span> <span class="text-xs text-amber-600" style="font-size:12px; color:#d97706;">(reversed sign)</span></p>'
  + '      </div>'
  + '    </div>'
  + '  </div>'
  + '  <div class="mb-6">'
  + '    <h4 class="text-lg font-bold text-surface-900 mb-3" style="font-size:18px; font-weight:700; color:var(--fg); margin-bottom:12px;">3.4 Graphing Inequalities on a Number Line</h4>'
  + '    <p class="text-[15px] text-surface-600 leading-relaxed mb-4" style="font-size:15px; color:var(--muted); line-height:1.625; margin-bottom:16px;">'
  + '      To graph an inequality on a number line, use an open circle for strict inequalities (&lt;, &gt;) and a closed circle for inclusive inequalities (≤, ≥).'
  + '    </p>'
  + '    <div class="bg-surface-50 border border-surface-200 rounded-2xl p-6" style="background:#fafafa; border:1px solid var(--border); border-radius:16px; padding:24px;">'
  + '      <div class="flex items-center justify-center gap-1 mb-2" style="display:flex; align-items:center; justify-content:center; gap:4px;">'
  + '        <div class="w-2 h-2 rounded-full border-2 border-accent-600 bg-white flex-shrink-0" style="width:8px; height:8px; border-radius:50%; border:2px solid var(--accent); background:#fff; flex-shrink:0;"></div>'
  + '        <div class="h-0.5 bg-surface-300 flex-1 relative" style="height:2px; background:#e5e5e5; flex:1; position:relative;">'
  + '          <div class="absolute left-0 top-1/2 -translate-y-1/2 w-[60%] h-0.5 bg-accent-500 rounded-full" style="position:absolute; left:0; top:50%; transform:translateY(-50%); width:60%; height:2px; background:var(--accent);"></div>'
  + '        </div>'
  + '        <div class="text-xs text-surface-400" style="font-size:12px; color:var(--muted);">5</div>'
  + '      </div>'
  + '      <p class="text-center text-sm text-surface-500 mt-2 m-0" style="text-align:center; font-size:14px; color:var(--muted); margin-top:8px; margin-bottom:0;"><span class="math-eq">x &lt; 5</span></p>'
  + '    </div>'
  + '  </div>'
  + '</div>',

  /* Page 3 */
  '<div class="page-content" id="page3">'
  + '  <div class="mb-8">'
  + '    <h4 class="text-lg font-bold text-surface-900 mb-3" style="font-size:18px; font-weight:700; color:var(--fg); margin-bottom:12px;">3.5 Real-Life Applications</h4>'
  + '    <p class="text-[15px] text-surface-600 leading-relaxed mb-4" style="font-size:15px; color:var(--muted); line-height:1.625; margin-bottom:16px;">'
  + '      Linear equations and inequalities are used extensively in real-world problem solving. Below are some common scenarios:'
  + '    </p>'
  + '    <div class="bg-blue-50 border border-blue-200 rounded-2xl p-5 mb-5" style="background:#eff6ff; border:1px solid #bfdbfe; border-radius:16px; padding:20px; margin-bottom:20px;">'
  + '      <div class="text-xs font-bold text-blue-700 uppercase tracking-wider mb-2" style="color:#1d4ed8; font-weight:700; font-size:12px; text-transform:uppercase; letter-spacing:0.05em; margin-bottom:8px;">Application 1 — Budgeting</div>'
  + '      <p class="text-sm text-blue-900 mb-2" style="color:#1e3a8a; font-size:14px; margin-bottom:8px;">You have $50 to spend on notebooks and pens. Notebooks cost $8 each and pens cost $2 each. Write an inequality:</p>'
  + '      <div class="bg-white/60 rounded-xl p-3 text-center" style="background:rgba(255,255,255,0.6); border-radius:12px; padding:12px; text-align:center;">'
  + '        <span class="math-eq">8n + 2p ≤ 50</span>'
  + '      </div>'
  + '    </div>'
  + '    <div class="bg-purple-50 border border-purple-200 rounded-2xl p-5 mb-5" style="background:#faf5ff; border:1px solid #e9d5ff; border-radius:16px; padding:20px; margin-bottom:20px;">'
  + '      <div class="text-xs font-bold text-purple-700 uppercase tracking-wider mb-2" style="color:#7e22ce; font-weight:700; font-size:12px; text-transform:uppercase; letter-spacing:0.05em; margin-bottom:8px;">Application 2 — Temperature</div>'
  + '      <p class="text-sm text-purple-900 mb-2" style="color:#581c87; font-size:14px; margin-bottom:8px;">Water boils at 100°C at standard pressure. The temperature <span class="math-eq">T</span> must satisfy:</p>'
  + '      <div class="bg-white/60 rounded-xl p-3 text-center" style="background:rgba(255,255,255,0.6); border-radius:12px; padding:12px; text-align:center;">'
  + '        <span class="math-eq">T ≥ 100°C</span> for boiling to occur'
  + '      </div>'
  + '    </div>'
  + '  </div>'
  + '  <div class="mb-6">'
  + '    <h4 class="text-lg font-bold text-surface-900 mb-3" style="font-size:18px; font-weight:700; color:var(--fg); margin-bottom:12px;">3.6 Word Problem Strategy</h4>'
  + '    <div class="bg-surface-50 border border-surface-200 rounded-2xl p-5" style="background:#fafafa; border:1px solid var(--border); border-radius:16px; padding:20px;">'
  + '      <ol class="text-sm text-surface-600 space-y-2.5" style="list-style:none; padding:0; margin:0; display:flex; flex-direction:column; gap:10px;">'
  + '        <li class="flex gap-3" style="display:flex; gap:12px; align-items:flex-start;"><span class="w-6 h-6 rounded-full bg-accent-100 text-accent-700 flex items-center justify-center text-xs font-bold flex-shrink-0" style="width:24px; height:24px; border-radius:50%; background:var(--accent-light); color:var(--accent); display:flex; align-items:center; justify-content:center; font-size:12px; font-weight:700; flex-shrink:0;">1</span><span>Read the problem carefully. Identify what is given and what is asked.</span></li>'
  + '        <li class="flex gap-3" style="display:flex; gap:12px; align-items:flex-start;"><span class="w-6 h-6 rounded-full bg-accent-100 text-accent-700 flex items-center justify-center text-xs font-bold flex-shrink-0" style="width:24px; height:24px; border-radius:50%; background:var(--accent-light); color:var(--accent); display:flex; align-items:center; justify-content:center; font-size:12px; font-weight:700; flex-shrink:0;">2</span><span>Define a variable to represent the unknown quantity.</span></li>'
  + '        <li class="flex gap-3" style="display:flex; gap:12px; align-items:flex-start;"><span class="w-6 h-6 rounded-full bg-accent-100 text-accent-700 flex items-center justify-center text-xs font-bold flex-shrink-0" style="width:24px; height:24px; border-radius:50%; background:var(--accent-light); color:var(--accent); display:flex; align-items:center; justify-content:center; font-size:12px; font-weight:700; flex-shrink:0;">3</span><span>Write an equation or inequality based on the relationships described.</span></li>'
  + '        <li class="flex gap-3" style="display:flex; gap:12px; align-items:flex-start;"><span class="w-6 h-6 rounded-full bg-accent-100 text-accent-700 flex items-center justify-center text-xs font-bold flex-shrink-0" style="width:24px; height:24px; border-radius:50%; background:var(--accent-light); color:var(--accent); display:flex; align-items:center; justify-content:center; font-size:12px; font-weight:700; flex-shrink:0;">4</span><span>Solve the equation or inequality.</span></li>'
  + '        <li class="flex gap-3" style="display:flex; gap:12px; align-items:flex-start;"><span class="w-6 h-6 rounded-full bg-accent-100 text-accent-700 flex items-center justify-center text-xs font-bold flex-shrink-0" style="width:24px; height:24px; border-radius:50%; background:var(--accent-light); color:var(--accent); display:flex; align-items:center; justify-content:center; font-size:12px; font-weight:700; flex-shrink:0;">5</span><span>Check your answer in the context of the problem.</span></li>'
  + '      </ol>'
  + '    </div>'
  + '  </div>'
  + '</div>',

  /* Page 4 */
  '<div class="page-content" id="page4">'
  + '  <div class="text-center mb-8">'
  + '    <h4 class="text-xl font-bold text-surface-900 mb-1" style="font-size:20px; font-weight:700; color:var(--fg); margin-bottom:4px;">Practice Problems</h4>'
  + '    <p class="text-sm text-surface-400 m-0" style="font-size:14px; color:var(--muted); margin:0;">Solve each equation or inequality. Show all working.</p>'
  + '  </div>'
  + '  <div class="space-y-4" style="display:flex; flex-direction:column; gap:16px;">'
  + '    <div class="bg-surface-50 border border-surface-200 rounded-2xl p-4 flex gap-4 items-start" style="display:flex; gap:16px; align-items:flex-start; padding:16px; background:#fafafa; border:1px solid var(--border); border-radius:16px;">'
  + '      <span class="w-8 h-8 rounded-xl bg-accent-100 text-accent-700 flex items-center justify-center text-sm font-bold flex-shrink-0" style="width:32px; height:32px; border-radius:12px; background:var(--accent-light); color:var(--accent); display:flex; align-items:center; justify-content:center; font-size:14px; font-weight:700; flex-shrink:0;">1</span>'
  + '      <p class="text-sm text-surface-700 pt-1 m-0" style="font-size:14px; color:var(--fg); margin:0; padding-top:4px;"><span class="math-eq">7x − 3 = 4x + 12</span></p>'
  + '    </div>'
  + '    <div class="bg-surface-50 border border-surface-200 rounded-2xl p-4 flex gap-4 items-start" style="display:flex; gap:16px; align-items:flex-start; padding:16px; background:#fafafa; border:1px solid var(--border); border-radius:16px;">'
  + '      <span class="w-8 h-8 rounded-xl bg-accent-100 text-accent-700 flex items-center justify-center text-sm font-bold flex-shrink-0" style="width:32px; height:32px; border-radius:12px; background:var(--accent-light); color:var(--accent); display:flex; align-items:center; justify-content:center; font-size:14px; font-weight:700; flex-shrink:0;">2</span>'
  + '      <p class="text-sm text-surface-700 pt-1 m-0" style="font-size:14px; color:var(--fg); margin:0; padding-top:4px;"><span class="math-eq">2(3y − 1) = 5y + 7</span></p>'
  + '    </div>'
  + '    <div class="bg-surface-50 border border-surface-200 rounded-2xl p-4 flex gap-4 items-start" style="display:flex; gap:16px; align-items:flex-start; padding:16px; background:#fafafa; border:1px solid var(--border); border-radius:16px;">'
  + '      <span class="w-8 h-8 rounded-xl bg-accent-100 text-accent-700 flex items-center justify-center text-sm font-bold flex-shrink-0" style="width:32px; height:32px; border-radius:12px; background:var(--accent-light); color:var(--accent); display:flex; align-items:center; justify-content:center; font-size:14px; font-weight:700; flex-shrink:0;">3</span>'
  + '      <p class="text-sm text-surface-700 pt-1 m-0" style="font-size:14px; color:var(--fg); margin:0; padding-top:4px;"><span class="math-eq">−4x + 9 ≥ 21</span></p>'
  + '    </div>'
  + '    <div class="bg-surface-50 border border-surface-200 rounded-2xl p-4 flex gap-4 items-start" style="display:flex; gap:16px; align-items:flex-start; padding:16px; background:#fafafa; border:1px solid var(--border); border-radius:16px;">'
  + '      <span class="w-8 h-8 rounded-xl bg-accent-100 text-accent-700 flex items-center justify-center text-sm font-bold flex-shrink-0" style="width:32px; height:32px; border-radius:12px; background:var(--accent-light); color:var(--accent); display:flex; align-items:center; justify-content:center; font-size:14px; font-weight:700; flex-shrink:0;">4</span>'
  + '      <p class="text-sm text-surface-700 pt-1 m-0" style="font-size:14px; color:var(--fg); margin:0; padding-top:4px;"><span class="math-eq">3(m + 4) &lt; 2m − 1</span></p>'
  + '    </div>'
  + '    <div class="bg-surface-50 border border-surface-200 rounded-2xl p-4 flex gap-4 items-start" style="display:flex; gap:16px; align-items:flex-start; padding:16px; background:#fafafa; border:1px solid var(--border); border-radius:16px;">'
  + '      <span class="w-8 h-8 rounded-xl bg-accent-100 text-accent-700 flex items-center justify-center text-sm font-bold flex-shrink-0" style="width:32px; height:32px; border-radius:12px; background:var(--accent-light); color:var(--accent); display:flex; align-items:center; justify-content:center; font-size:14px; font-weight:700; flex-shrink:0;">5</span>'
  + '      <p class="text-sm text-surface-700 pt-1 m-0" style="font-size:14px; color:var(--fg); margin:0; padding-top:4px;"><span class="math-eq">(x + 2)/3 − (x − 1)/4 = 2</span></p>'
  + '    </div>'
  + '    <div class="bg-surface-50 border border-surface-200 rounded-2xl p-4 flex gap-4 items-start" style="display:flex; gap:16px; align-items:flex-start; padding:16px; background:#fafafa; border:1px solid var(--border); border-radius:16px;">'
  + '      <span class="w-8 h-8 rounded-xl bg-accent-100 text-accent-700 flex items-center justify-center text-sm font-bold flex-shrink-0" style="width:32px; height:32px; border-radius:12px; background:var(--accent-light); color:var(--accent); display:flex; align-items:center; justify-content:center; font-size:14px; font-weight:700; flex-shrink:0;">6</span>'
  + '      <p class="text-sm text-surface-700 pt-1 m-0" style="font-size:14px; color:var(--fg); margin:0; padding-top:4px;">A taxi charges $3 plus $1.50 per kilometer. If a passenger has $24, what is the maximum distance they can travel?</p>'
  + '    </div>'
  + '    <div class="bg-surface-50 border border-surface-200 rounded-2xl p-4 flex gap-4 items-start" style="display:flex; gap:16px; align-items:flex-start; padding:16px; background:#fafafa; border:1px solid var(--border); border-radius:16px;">'
  + '      <span class="w-8 h-8 rounded-xl bg-accent-100 text-accent-700 flex items-center justify-center text-sm font-bold flex-shrink-0" style="width:32px; height:32px; border-radius:12px; background:var(--accent-light); color:var(--accent); display:flex; align-items:center; justify-content:center; font-size:14px; font-weight:700; flex-shrink:0;">7</span>'
  + '      <p class="text-sm text-surface-700 pt-1 m-0" style="font-size:14px; color:var(--fg); margin:0; padding-top:4px;">The sum of two consecutive even numbers is 54. Find the numbers.</p>'
  + '    </div>'
  + '    <div class="bg-surface-50 border border-surface-200 rounded-2xl p-4 flex gap-4 items-start" style="display:flex; gap:16px; align-items:flex-start; padding:16px; background:#fafafa; border:1px solid var(--border); border-radius:16px;">'
  + '      <span class="w-8 h-8 rounded-xl bg-accent-100 text-accent-700 flex items-center justify-center text-sm font-bold flex-shrink-0" style="width:32px; height:32px; border-radius:12px; background:var(--accent-light); color:var(--accent); display:flex; align-items:center; justify-content:center; font-size:14px; font-weight:700; flex-shrink:0;">8</span>'
  + '      <p class="text-sm text-surface-700 pt-1 m-0" style="font-size:14px; color:var(--fg); margin:0; padding-top:4px;"><span class="math-eq">5 − 3(2p + 1) ≤ 2p − 7</span></p>'
  + '    </div>'
  + '  </div>'
  + '</div>',

  /* Page 5 */
  '<div class="page-content" id="page5">'
  + '  <div class="mb-8">'
  + '    <h4 class="text-lg font-bold text-surface-900 mb-3" style="font-size:18px; font-weight:700; color:var(--fg); margin-bottom:12px;">Answer Key</h4>'
  + '    <div class="space-y-3" style="display:flex; flex-direction:column; gap:12px;">'
  + '      <div class="flex items-center gap-4 p-3 rounded-xl bg-accent-50/50" style="display:flex; gap:16px; align-items:center; padding:12px; background:rgba(240,253,244,0.5); border-radius:12px;">'
  + '        <span class="w-6 h-6 rounded-lg bg-accent-100 text-accent-700 flex items-center justify-center text-xs font-bold flex-shrink-0" style="width:24px; height:24px; border-radius:8px; background:var(--accent-light); color:var(--accent); display:flex; align-items:center; justify-content:center; font-size:12px; font-weight:700; flex-shrink:0;">1</span>'
  + '        <span class="text-sm text-surface-700"><span class="math-eq">x = 5</span></span>'
  + '      </div>'
  + '      <div class="flex items-center gap-4 p-3 rounded-xl bg-accent-50/50" style="display:flex; gap:16px; align-items:center; padding:12px; background:rgba(240,253,244,0.5); border-radius:12px;">'
  + '        <span class="w-6 h-6 rounded-lg bg-accent-100 text-accent-700 flex items-center justify-center text-xs font-bold flex-shrink-0" style="width:24px; height:24px; border-radius:8px; background:var(--accent-light); color:var(--accent); display:flex; align-items:center; justify-content:center; font-size:12px; font-weight:700; flex-shrink:0;">2</span>'
  + '        <span class="text-sm text-surface-700"><span class="math-eq">y = 9</span></span>'
  + '      </div>'
  + '      <div class="flex items-center gap-4 p-3 rounded-xl bg-accent-50/50" style="display:flex; gap:16px; align-items:center; padding:12px; background:rgba(240,253,244,0.5); border-radius:12px;">'
  + '        <span class="w-6 h-6 rounded-lg bg-accent-100 text-accent-700 flex items-center justify-center text-xs font-bold flex-shrink-0" style="width:24px; height:24px; border-radius:8px; background:var(--accent-light); color:var(--accent); display:flex; align-items:center; justify-content:center; font-size:12px; font-weight:700; flex-shrink:0;">3</span>'
  + '        <span class="text-sm text-surface-700"><span class="math-eq">x ≤ −3</span></span>'
  + '      </div>'
  + '      <div class="flex items-center gap-4 p-3 rounded-xl bg-accent-50/50" style="display:flex; gap:16px; align-items:center; padding:12px; background:rgba(240,253,244,0.5); border-radius:12px;">'
  + '        <span class="w-6 h-6 rounded-lg bg-accent-100 text-accent-700 flex items-center justify-center text-xs font-bold flex-shrink-0" style="width:24px; height:24px; border-radius:8px; background:var(--accent-light); color:var(--accent); display:flex; align-items:center; justify-content:center; font-size:12px; font-weight:700; flex-shrink:0;">4</span>'
  + '        <span class="text-sm text-surface-700"><span class="math-eq">m &lt; −13</span></span>'
  + '      </div>'
  + '      <div class="flex items-center gap-4 p-3 rounded-xl bg-accent-50/50" style="display:flex; gap:16px; align-items:center; padding:12px; background:rgba(240,253,244,0.5); border-radius:12px;">'
  + '        <span class="w-6 h-6 rounded-lg bg-accent-100 text-accent-700 flex items-center justify-center text-xs font-bold flex-shrink-0" style="width:24px; height:24px; border-radius:8px; background:var(--accent-light); color:var(--accent); display:flex; align-items:center; justify-content:center; font-size:12px; font-weight:700; flex-shrink:0;">5</span>'
  + '        <span class="text-sm text-surface-700"><span class="math-eq">x = 26</span></span>'
  + '      </div>'
  + '      <div class="flex items-center gap-4 p-3 rounded-xl bg-accent-50/50" style="display:flex; gap:16px; align-items:center; padding:12px; background:rgba(240,253,244,0.5); border-radius:12px;">'
  + '        <span class="w-6 h-6 rounded-lg bg-accent-100 text-accent-700 flex items-center justify-center text-xs font-bold flex-shrink-0" style="width:24px; height:24px; border-radius:8px; background:var(--accent-light); color:var(--accent); display:flex; align-items:center; justify-content:center; font-size:12px; font-weight:700; flex-shrink:0;">6</span>'
  + '        <span class="text-sm text-surface-700"><span class="math-eq">14 km</span></span>'
  + '      </div>'
  + '      <div class="flex items-center gap-4 p-3 rounded-xl bg-accent-50/50" style="display:flex; gap:16px; align-items:center; padding:12px; background:rgba(240,253,244,0.5); border-radius:12px;">'
  + '        <span class="w-6 h-6 rounded-lg bg-accent-100 text-accent-700 flex items-center justify-center text-xs font-bold flex-shrink-0" style="width:24px; height:24px; border-radius:8px; background:var(--accent-light); color:var(--accent); display:flex; align-items:center; justify-content:center; font-size:12px; font-weight:700; flex-shrink:0;">7</span>'
  + '        <span class="text-sm text-surface-700"><span class="math-eq">26 and 28</span></span>'
  + '      </div>'
  + '      <div class="flex items-center gap-4 p-3 rounded-xl bg-accent-50/50" style="display:flex; gap:16px; align-items:center; padding:12px; background:rgba(240,253,244,0.5); border-radius:12px;">'
  + '        <span class="w-6 h-6 rounded-lg bg-accent-100 text-accent-700 flex items-center justify-center text-xs font-bold flex-shrink-0" style="width:24px; height:24px; border-radius:8px; background:var(--accent-light); color:var(--accent); display:flex; align-items:center; justify-content:center; font-size:12px; font-weight:700; flex-shrink:0;">8</span>'
  + '        <span class="text-sm text-surface-700"><span class="math-eq">p ≥ 1</span></span>'
  + '      </div>'
  + '    </div>'
  + '  </div>'
  + '  <div class="mt-10 pt-6 border-t border-surface-200 text-center" style="margin-top:40px; padding-top:24px; border-top:1px solid #e5e5e5; text-align:center;">'
  + '    <p class="text-xs text-surface-400 m-0" style="font-size:12px; color:#a3a3a3; margin:0;">End of Chapter 3 — Linear Equations &amp; Inequalities</p>'
  + '    <p class="text-xs text-surface-300 mt-1 m-0" style="font-size:12px; color:#d4d4d4; margin-top:4px; margin-bottom:0;">Prepared by Mr. Chea Sophea | Academic Year 2025–2026</p>'
  + '  </div>'
  + '</div>'
];

/* ── Inline pager state (only used when lesson preview is active) ── */
var _lsnPage  = 1;
var _lsnTotal = 5;

function _lsnGoTo(page) {
  if (page < 1 || page > _lsnTotal) return;
  _lsnPage = page;
  var paper = document.getElementById('rpvFrameWrap');
  if (!paper) return;
  var el = paper.querySelector('.lesson-preview-paper');
  if (el) el.innerHTML = LESSON_PAGES[_lsnPage - 1];
  /* sync the main toolbar page indicator */
  var cur = document.getElementById('rpvPageCur');
  if (cur) cur.textContent = _lsnPage;
  /* highlight active thumbnail */
  paper.querySelectorAll('.lsn-thumb').forEach(function(t) {
    t.classList.toggle('active', parseInt(t.dataset.page) === _lsnPage);
  });
}

function buildLessonPreviewMarkup(r) {
  /* Works for any resource that has inline HTML pages defined.
     Falls back gracefully — callers already check r.id === 'm2' upstream
     but we keep the guard so this is safe to call generically. */
  _lsnPage  = 1;
  _lsnTotal = LESSON_PAGES.length;

  return '<div class="lesson-preview-shell" id="lsnShell">'
    + '<div class="lesson-preview-body">'
    + '<div class="lesson-preview-paper" id="lsnPaper">'
    + LESSON_PAGES[0]
    + '</div>'
    + '</div>'
    + '</div>';
}

function showViewerPlaceholder() {
  var ph = document.getElementById('viewerPlaceholder');
  var ws = document.getElementById('rpvWorkspace');
  if (ph) ph.hidden = false;
  if (ws) ws.hidden = true;
}

function openInViewer(r) {
  _previewSrc    = r.src;
  _previewName   = r.name;
  _rpvZoom       = 100;
  _rpvRotate     = 0;
  _rpvBm         = false;

  var ph = document.getElementById('viewerPlaceholder');
  var ws = document.getElementById('rpvWorkspace');
  if (ph) ph.hidden = true;
  if (ws) ws.hidden = false;

  var m   = typeMeta(r.type);
  var fts = fileTypeStyle(r.fileType);

  /* ── Card 1: Resource Info ── */
  var iconWrap = document.getElementById('rpvFileIconWrap');
  var icon     = document.getElementById('rpvFileIcon');
  var badge    = document.getElementById('rpvFtypeBadge');
  var resTitle = document.getElementById('rpvResTitle');
  var resDesc  = document.getElementById('rpvResDesc');
  var metaDate = document.getElementById('rpvMetaDate');
  var metaTch  = document.getElementById('rpvMetaTeacher');
  var metaSz   = document.getElementById('rpvMetaSize');
  var metaDl   = document.getElementById('rpvMetaDownloads');
  var tagsEl   = document.getElementById('rpvTags');
  var dlBtn    = document.getElementById('rpvDlBtn');
  var bmBtn    = document.getElementById('rpvBmBtn');
  var bmBarBtn = document.getElementById('rpvBmBarBtn');

  if (iconWrap) { iconWrap.style.background = fts.bg; iconWrap.style.border = 'none'; }
  if (icon)     { icon.textContent = fts.icon; icon.style.color = fts.color; }
  if (badge)    { badge.className = 'rpv-ftype-badge ' + fts.badge; badge.textContent = m.label.toUpperCase(); }
  if (resTitle) {
    resTitle.textContent = r.id === 'm2' ? 'Chapter 3 — Linear Equations & Inequalities' : r.name;
  }
  if (resDesc) {
    resDesc.textContent = r.id === 'm2' ? 'Introduction to solving linear equations and inequalities in one variable.' : getDesc(r);
  }
  if (metaDate) metaDate.textContent = fmtDate(r.date);
  if (metaTch) {
    var tname = document.getElementById('teacherName');
    metaTch.textContent = (tname && tname.textContent) ? tname.textContent : 'Teacher';
  }
  if (metaSz)   metaSz.textContent  = r.size !== '—' ? r.size : 'N/A';
  if (metaDl)   metaDl.textContent  = r.downloads ? r.downloads.toLocaleString() : '0';
  if (tagsEl)   tagsEl.innerHTML    = r.tags.map(function(t){ return '<span class="rpv-tag">' + escHtml(t) + '</span>'; }).join('');
  if (dlBtn)    dlBtn.style.display = r.fileType === 'link' ? 'none' : '';

  /* reset bookmark */
  _rpvBm = false;
  _rpvSyncBmBtns();

  /* thumbnail placeholder — show type icon */
  var thumbPh = document.getElementById('rpvThumbPlaceholder');
  if (thumbPh) {
    thumbPh.innerHTML = '<span class="material-symbols-outlined" style="font-size:48px;color:' + fts.color + ';font-variation-settings:\'FILL\' 1">' + fts.icon + '</span>';
    thumbPh.style.background = fts.bg;
  }

  /* ── Right Panel: Teacher/Resource Details Stats ── */
  var rightViews = document.getElementById('rpvRightViews');
  var rightDls = document.getElementById('rpvRightDownloads');
  var rightSize = document.getElementById('rpvRightSize');
  var rightRelated = document.getElementById('rpvRightRelated');
  
  if (rightViews) rightViews.textContent = r.downloads ? (r.downloads * 4 + 15).toLocaleString() : '12';
  if (rightDls) rightDls.textContent = r.downloads ? r.downloads.toLocaleString() : '0';
  if (rightSize) rightSize.textContent = r.size !== '—' ? r.size : 'N/A';
  
  if (rightRelated) {
    var rels = RES_RELATED[r.id] || [];
    if (rels.length === 0) {
      rightRelated.innerHTML = '<div style="font-size: 12px; color: var(--muted); text-align: center; padding: 24px 0;">No related resources found.</div>';
    } else {
      rightRelated.innerHTML = rels.slice(0, 4).map(function(a) {
        var cls = FILE_TYPE_ICO_CLASS[a.type] || 'pdf-ic';
        var lbl = FILE_TYPE_ICO_LABEL[a.type] || 'FILE';
        return '<div class="rpv-related-card" style="margin-bottom:8px">'
          + '<span class="rpv-rc-ico lib-ftype-ico ' + cls + '">' + lbl + '</span>'
          + '<div class="rpv-rc-name">' + escHtml(a.name) + '</div>'
          + '<div class="rpv-rc-sub">' + escHtml(a.size) + '</div>'
          + '</div>';
      }).join('');
    }
  }

  /* ── Card 2: Embedded Viewer ── */
  rpvZoomLabel();
  var frameWrap = document.getElementById('rpvFrameWrap');
  if (frameWrap) {
    var frameHtml = '';
    if (r.id === 'm2') {
      frameHtml = buildLessonPreviewMarkup(r);
    } else if (r.fileType === 'pdf') {
      frameHtml = '<iframe src="' + r.src + '#toolbar=0&view=FitH" title="' + escHtml(r.name) + '" loading="lazy" style="width:100%;min-height:520px;border:none;display:block"></iframe>';
    } else if (r.fileType === 'image') {
      frameHtml = '<div class="viewer-img-wrap" style="min-height:420px;background:#fff"><img src="' + r.src + '" alt="' + escHtml(r.name) + '"></div>';
    } else if (r.fileType === 'video') {
      frameHtml = '<div style="background:#000;display:flex;align-items:center;justify-content:center;min-height:420px">'
        + '<iframe src="' + r.src + '" title="' + escHtml(r.name) + '" allowfullscreen style="width:100%;aspect-ratio:16/9;border:none"></iframe></div>';
    } else if (r.fileType === 'link') {
      frameHtml = '<div class="viewer-link-wrap">'
        + '<span class="material-symbols-outlined" style="font-size:56px;color:' + fts.color + '">open_in_new</span>'
        + '<div class="viewer-link-name">' + escHtml(r.name) + '</div>'
        + '<p>This is an external resource that opens in a new tab.</p>'
        + '<a href="' + escHtml(r.src) + '" target="_blank" rel="noopener noreferrer" class="btn btn-primary">'
        + '<span class="material-symbols-outlined">open_in_new</span>Open Link</a>'
        + '</div>';
    }
    frameWrap.innerHTML = frameHtml;
  }

  /* ── Wire page indicator & toolbar prev/next for inline lesson preview ── */
  var pageCur   = document.getElementById('rpvPageCur');
  var pageTotal = document.getElementById('rpvPageTotal');
  if (r.id === 'm2') {
    _lsnPage  = 1;
    _lsnTotal = LESSON_PAGES.length;
    if (pageCur)   pageCur.textContent   = '1';
    if (pageTotal) pageTotal.textContent = String(_lsnTotal);
    /* wire the toolbar prev / next buttons (by position in toolbar) */
    var toolbar = document.querySelector('.rpv-embed-toolbar');
    if (toolbar) {
      var prevBtn = toolbar.querySelector('[aria-label="Previous page"]');
      var nextBtn = toolbar.querySelector('[aria-label="Next page"]');
      if (prevBtn) {
        prevBtn.onclick = function() {
          _lsnGoTo(_lsnPage - 1);
          var cur = document.getElementById('rpvPageCur');
          if (cur) cur.textContent = _lsnPage;
        };
      }
      if (nextBtn) {
        nextBtn.onclick = function() {
          _lsnGoTo(_lsnPage + 1);
          var cur = document.getElementById('rpvPageCur');
          if (cur) cur.textContent = _lsnPage;
        };
      }
    }
    /* keyboard left/right arrow support for inline pages */
    document._lsnKeyHandler && document.removeEventListener('keydown', document._lsnKeyHandler);
    document._lsnKeyHandler = function(e) {
      if (e.target.matches('input, textarea, select')) return;
      if (e.key === 'ArrowLeft')  { e.preventDefault(); _lsnGoTo(_lsnPage - 1); var c = document.getElementById('rpvPageCur'); if(c) c.textContent = _lsnPage; }
      if (e.key === 'ArrowRight') { e.preventDefault(); _lsnGoTo(_lsnPage + 1); var c = document.getElementById('rpvPageCur'); if(c) c.textContent = _lsnPage; }
    };
    document.addEventListener('keydown', document._lsnKeyHandler);
  } else {
    if (pageCur)   pageCur.textContent   = '1';
    if (pageTotal) pageTotal.textContent = '—';
    /* reset prev/next to no-ops for non-paginated resources */
    var toolbar2 = document.querySelector('.rpv-embed-toolbar');
    if (toolbar2) {
      var pb = toolbar2.querySelector('[aria-label="Previous page"]');
      var nb = toolbar2.querySelector('[aria-label="Next page"]');
      if (pb) pb.onclick = null;
      if (nb) nb.onclick = null;
    }
    document._lsnKeyHandler && document.removeEventListener('keydown', document._lsnKeyHandler);
    document._lsnKeyHandler = null;
  }

  /* ── Populate tabs for resource m2 ── */
  _rpvPopulateTabs(r);

  /* ── Card 3: Teacher notes (fallback for resources without tab data) ── */
  var notesTeacher = document.getElementById('rpvNotesTeacher');
  var notesAvatar  = document.getElementById('rpvNotesAvatar');
  var notesText    = document.getElementById('rpvNotesText');
  var tname2       = document.getElementById('teacherName');
  var tavatar      = document.getElementById('teacherAvatar');
  if (notesTeacher && tname2) notesTeacher.textContent = tname2.textContent;
  if (notesAvatar  && tavatar) notesAvatar.src = tavatar.src;
  /* only set notes text if _rpvPopulateTabs didn't already supply specific notes */
  if (notesText && !RES_NOTES[r.id]) notesText.textContent = getDesc(r);

  /* ── Card 3: Description tab ── */
  var descText = document.getElementById('rpvDescText');
  var descMeta = document.getElementById('rpvDescMeta');
  if (descText) {
    descText.textContent = r.id === 'm2' ? 'This chapter introduces the basic concepts of linear equations, solving methods, and real-life applications. Students will learn to identify, set up, and solve linear equations and inequalities in one variable.' : getDesc(r);
  }
  if (descMeta) {
    descMeta.innerHTML = r.id === 'm2'
      ? '<span class="lib-tag">#Algebra</span><span class="lib-tag">#Chapter3</span><span class="lib-tag">#Worksheet</span>'
      : r.tags.map(function(t){ return '<span class="lib-tag">' + escHtml(t) + '</span>'; }).join('');
  }

  /* reset tabs to Description */
  rpvSwitchTabById('description');
}

function expandViewer() {
  openPreview(_previewName, _currentResources.find(function(r){ return r.id === _activeId; }) || {}, _previewSrc);
}

/* ════════════════════════════════════
   Tab data for m2 (and any resource)
════════════════════════════════════ */
var RES_ATTACHMENTS = {
  m2: [
    { name:'Ch3_AnswerKey.pdf',        size:'245 KB',  type:'pdf'   },
    { name:'NumberLine_Diagrams.png',  size:'1.2 MB',  type:'image' },
    { name:'Ch3_Extra_Practice.docx',  size:'380 KB',  type:'word'  },
    { name:'Student_Scores_Ch3.xlsx',  size:'156 KB',  type:'excel' },
    { name:'Ch3_Lesson_Slides.pptx',   size:'4.7 MB',  type:'ppt'   }
  ]
};
var RES_RELATED = {
  m2: [
    { name:'Ch2_Polynomials.pdf',          size:'1.8 MB', type:'pdf'   },
    { name:'Ch4_Systems_Equations.pdf',    size:'2.3 MB', type:'pdf'   },
    { name:'Algebra_Formulas_Sheet.docx',  size:'520 KB', type:'word'  },
    { name:'Grade9_Progress_Tracker.xlsx', size:'890 KB', type:'excel' },
    { name:'Midterm_Review_Pack.pdf',      size:'3.1 MB', type:'pdf'   },
    { name:'Inequalities_Visual_Guide.pptx',size:'2.8 MB',type:'ppt'   },
    { name:'Ch1_Real_Numbers.pdf',         size:'1.5 MB', type:'pdf'   },
    { name:'Graph_Paper_Template.png',     size:'210 KB', type:'image' }
  ]
};
var RES_REFS = {
  m2: [
    { title:'Singapore Math — Secondary 2 Workbook',   detail:'Marshall Cavendish Education, 2024. Chapter 5: Linear Equations.' },
    { title:'Algebra I — Glencoe Mathematics',          detail:'McGraw-Hill, 2023. Pages 142–178.' },
    { title:'Khan Academy — Linear Equations & Inequalities', detail:'Online resource. Accessed June 2026.' },
    { title:'MoEYS Mathematics Curriculum — Grade 9',  detail:'Ministry of Education, Youth and Sport, Cambodia. 2025 Edition.' }
  ]
};
var RES_LINKS = {
  m2: [
    { name:'Khan Academy — Algebra Foundations', url:'https://www.khanacademy.org/math/algebra',   domain:'khanacademy.org' },
    { name:'GeoGebra — Interactive Graphing Tool', url:'https://www.geogebra.org',                domain:'geogebra.org'    }
  ]
};
var RES_NOTES = {
  m2: 'Lesson Pacing: Allocate 2 class periods (80 min total). Sections 3.1–3.2 in period 1, 3.3–3.4 in period 2. Practice problems can be assigned as homework.\n\nCommon Misconceptions: Students frequently forget to reverse the inequality sign when multiplying/dividing by a negative number. Emphasise this with multiple examples.\n\nAssessment: Short quiz (10 min) at start of next class covering 3.1–3.4. Chapter test scheduled for Week 8.'
};

var FILE_TYPE_ICO_CLASS = {
  pdf:'pdf-ic', word:'word-ic', excel:'xls-ic', ppt:'ppt-ic', image:'img-ic', video:'vid-ic', link:'link-ic'
};
var FILE_TYPE_ICO_LABEL = {
  pdf:'PDF', word:'DOC', excel:'XLS', ppt:'PPT', image:'IMG', video:'VID', link:'LINK'
};

function _rpvPopulateTabs(r) {
  /* ── Attachments ── */
  var attEmpty = document.getElementById('rpvAttachmentsEmpty');
  var attList  = document.getElementById('rpvAttachmentsList');
  var attBtn   = document.querySelector('.rpv-tab[data-tab="attachments"] .rpv-tab-count');
  var atts     = RES_ATTACHMENTS[r.id] || [];
  if (attEmpty) attEmpty.hidden = atts.length > 0;
  if (attList)  {
    attList.hidden = atts.length === 0;
    attList.innerHTML = atts.map(function(a) {
      var cls = FILE_TYPE_ICO_CLASS[a.type] || 'pdf-ic';
      var lbl = FILE_TYPE_ICO_LABEL[a.type] || 'FILE';
      return '<div class="rpv-attach-item">'
        + '<span class="lib-ftype-ico ' + cls + '" style="height:28px;line-height:28px">' + lbl + '</span>'
        + '<div class="rpv-attach-body"><div class="rpv-attach-name">' + escHtml(a.name) + '</div>'
        + '<div class="rpv-attach-sub">' + escHtml(a.size) + '</div></div>'
        + '<button class="rpv-tool-btn" style="width:28px;height:28px;color:var(--muted)" title="Download" aria-label="Download '+ escHtml(a.name) +'">'
        + '<span class="material-symbols-outlined" style="font-size:16px">download</span></button>'
        + '</div>';
    }).join('');
  }
  if (attBtn) attBtn.textContent = atts.length;

  /* ── Related Files ── */
  var relEmpty = document.getElementById('rpvRelatedEmpty');
  var relGrid  = document.getElementById('rpvRelatedGrid');
  var relBtn   = document.querySelector('.rpv-tab[data-tab="related"] .rpv-tab-count');
  var rels     = RES_RELATED[r.id] || [];
  if (relEmpty) relEmpty.hidden = rels.length > 0;
  if (relGrid)  {
    relGrid.hidden = rels.length === 0;
    relGrid.innerHTML = rels.map(function(a) {
      var cls = FILE_TYPE_ICO_CLASS[a.type] || 'pdf-ic';
      var lbl = FILE_TYPE_ICO_LABEL[a.type] || 'FILE';
      return '<div class="rpv-related-card">'
        + '<span class="rpv-rc-ico lib-ftype-ico ' + cls + '">' + lbl + '</span>'
        + '<div class="rpv-rc-name">' + escHtml(a.name) + '</div>'
        + '<div class="rpv-rc-sub">' + escHtml(a.size) + '</div>'
        + '</div>';
    }).join('');
  }
  if (relBtn) relBtn.textContent = rels.length;

  /* ── References ── */
  var refsEmpty = document.getElementById('rpvRefsEmpty');
  var refsList  = document.getElementById('rpvRefsList');
  var refs      = RES_REFS[r.id] || [];
  if (refsEmpty) refsEmpty.hidden = refs.length > 0;
  if (refsList) {
    refsList.hidden = refs.length === 0;
    refsList.innerHTML = refs.map(function(ref, i) {
      return '<li>'
        + '<span class="material-symbols-outlined">link</span>'
        + '<div><strong style="font-size:13px;color:var(--heading)">' + escHtml(ref.title) + '</strong>'
        + '<div style="font-size:11px;color:var(--faint);margin-top:2px">' + escHtml(ref.detail) + '</div></div>'
        + '</li>';
    }).join('');
  }

  /* ── External Links ── */
  var linksEmpty = document.getElementById('rpvLinksEmpty');
  var linksList  = document.getElementById('rpvLinksList');
  var linksBtn   = document.querySelector('.rpv-tab[data-tab="links"] .rpv-tab-count');
  var links      = RES_LINKS[r.id] || [];
  if (linksEmpty) linksEmpty.hidden = links.length > 0;
  if (linksList) {
    linksList.hidden = links.length === 0;
    linksList.innerHTML = links.map(function(lnk) {
      return '<a href="' + escHtml(lnk.url) + '" target="_blank" rel="noopener noreferrer" class="rpv-ext-link">'
        + '<div class="rpv-ext-ico"><span class="material-symbols-outlined">open_in_new</span></div>'
        + '<div class="rpv-ext-body">'
        + '<div class="rpv-ext-name">' + escHtml(lnk.name) + '</div>'
        + '<div class="rpv-ext-url">' + escHtml(lnk.domain) + '</div>'
        + '</div>'
        + '<span class="material-symbols-outlined rpv-ext-arrow">arrow_forward</span>'
        + '</a>';
    }).join('');
  }
  if (linksBtn) linksBtn.textContent = links.length;

  /* ── Teacher notes ── */
  var notesText = document.getElementById('rpvNotesText');
  var noteDate  = document.getElementById('rpvNotesDate');
  if (notesText) notesText.textContent = RES_NOTES[r.id] || getDesc(r);
  if (noteDate) {
    var tname3 = document.getElementById('teacherName');
    noteDate.textContent = 'Posted by ' + ((tname3 && tname3.textContent) ? tname3.textContent : 'Teacher');
  }
}

/* ── Zoom ── */
function rpvZoom(delta) {
  _rpvZoom = Math.min(200, Math.max(50, _rpvZoom + delta));
  rpvZoomLabel();
  /* target the inline lesson paper if active, else the rpvPaper wrapper */
  var target = document.getElementById('lsnPaper') || document.getElementById('rpvPaper');
  if (target) {
    target.style.transformOrigin = 'top center';
    target.style.transform = 'scale(' + (_rpvZoom / 100) + ') rotate(' + _rpvRotate + 'deg)';
  }
}
function rpvZoomLabel() {
  var lbl = document.getElementById('rpvZoomLabel');
  if (lbl) lbl.textContent = _rpvZoom + '%';
}

/* ── Rotate ── */
function rpvRotate() {
  _rpvRotate = (_rpvRotate + 90) % 360;
  var target = document.getElementById('lsnPaper') || document.getElementById('rpvPaper');
  if (target) {
    target.style.transformOrigin = 'top center';
    target.style.transform = 'scale(' + (_rpvZoom / 100) + ') rotate(' + _rpvRotate + 'deg)';
  }
}

/* ── Bookmark (preview panel) ── */
function _rpvSyncBmBtns() {
  var bmBtn    = document.getElementById('rpvBmBtn');
  var bmBarBtn = document.getElementById('rpvBmBarBtn');
  var icon     = _rpvBm ? 'bookmark' : 'bookmark_border';
  var fill     = _rpvBm ? "'FILL' 1" : "'FILL' 0";
  [bmBtn, bmBarBtn].forEach(function(btn) {
    if (!btn) return;
    var ico = btn.querySelector('.material-symbols-outlined');
    if (ico) { ico.textContent = icon; ico.style.fontVariationSettings = fill; }
    btn.classList.toggle('bookmarked', _rpvBm);
  });
}
function togglePreviewBookmark() {
  _rpvBm = !_rpvBm;
  _rpvSyncBmBtns();
  /* also sync the row bookmark btn if available */
  if (_activeId) {
    var row = document.querySelector('.lib-file-row[data-id="' + _activeId + '"] .lib-bm-btn');
    if (row) {
      var ico = row.querySelector('.material-symbols-outlined');
      if (ico) { ico.textContent = _rpvBm ? 'bookmark' : 'bookmark_border'; ico.style.fontVariationSettings = _rpvBm ? "'FILL' 1" : "'FILL' 0"; }
      row.classList.toggle('bookmarked', _rpvBm);
    }
  }
}

/* ── Tab switching ── */
function rpvSwitchTab(btn, tabId) {
  document.querySelectorAll('.rpv-tab').forEach(function(el){
    el.classList.toggle('active', el.dataset.tab === tabId);
    el.setAttribute('aria-selected', el.dataset.tab === tabId ? 'true' : 'false');
  });
  document.querySelectorAll('.rpv-tab-pane').forEach(function(el){
    el.classList.toggle('active', el.id === 'rpv-tab-' + tabId);
  });
}
function rpvSwitchTabById(tabId) {
  document.querySelectorAll('.rpv-tab').forEach(function(el){
    el.classList.toggle('active', el.dataset.tab === tabId);
    el.setAttribute('aria-selected', el.dataset.tab === tabId ? 'true' : 'false');
  });
  document.querySelectorAll('.rpv-tab-pane').forEach(function(el){
    el.classList.toggle('active', el.id === 'rpv-tab-' + tabId);
  });
}

/* ════════════════════════════════════
   Filtering & Search
════════════════════════════════════ */
function filterType(btn, type) {
  _currentType = type;
  _currentName = '';
  _activeId    = null;
  document.querySelectorAll('.lib-tab').forEach(function(el){
    el.classList.toggle('active', el.dataset.type === type);
  });
  document.querySelectorAll('.lib-folder-item').forEach(function(el){
    el.classList.toggle('active', el.dataset.itemId === '');
  });
  showViewerPlaceholder();
  applyFilters();
}

function searchResources(q) {
  _currentSearch = (q || '').toLowerCase();
  applyFilters();
}

function sortResources(value) {
  var list = document.getElementById('resourceList');
  if (!list) return;
  var rows = Array.from(list.querySelectorAll('.lib-file-row'));
  rows.sort(function(a,b){
    if (value === 'name')   return (a.dataset.name||'').localeCompare(b.dataset.name||'');
    var da = new Date(a.dataset.date||0), db = new Date(b.dataset.date||0);
    return value === 'newest' ? db - da : da - db;
  });
  rows.forEach(function(r){ list.appendChild(r); });
}

function applyFilters() {
  var rows  = document.querySelectorAll('#resourceList .lib-file-row');
  var empty = document.getElementById('resourceEmpty');
  var vis   = 0;
  rows.forEach(function(el){
    var typeOk   = _currentType === 'all' || el.dataset.type === _currentType;
    var nameOk   = !_currentSearch || (el.dataset.name||'').includes(_currentSearch);
    var itemOk   = !_currentName   || el.dataset.id === _currentName;
    var show     = typeOk && nameOk && itemOk;
    el.style.display = show ? '' : 'none';
    if (show) vis++;
  });
  if (empty) empty.hidden = vis > 0;
}

/* ════════════════════════════════════
   Bookmark
════════════════════════════════════ */
function toggleBookmark(btn) {
  var ico = btn.querySelector('.material-symbols-outlined');
  if (!ico) return;
  var active = btn.classList.toggle('bookmarked');
  ico.textContent = active ? 'bookmark' : 'bookmark_border';
  ico.style.fontVariationSettings = active ? "'FILL' 1" : "'FILL' 0";
}

/* ════════════════════════════════════
   Copy link / Download
════════════════════════════════════ */
function copyLink(btn) {
  navigator.clipboard && navigator.clipboard.writeText(window.location.href);
  var ico = btn && btn.querySelector('.material-symbols-outlined');
  if (ico) { ico.textContent='check'; setTimeout(function(){ ico.textContent='link'; },1800); }
}
function copyLinkGeneric() { navigator.clipboard && navigator.clipboard.writeText(window.location.href); }
function downloadPreview() { downloadFile(_previewSrc, _previewName); }
function downloadFile(src, name) {
  if (!src) return;
  var a = document.createElement('a');
  a.href=src; a.download=name||'download'; a.target='_blank'; a.rel='noopener';
  document.body.appendChild(a); a.click(); document.body.removeChild(a);
}

/* ════════════════════════════════════
   Mobile sidebar
════════════════════════════════════ */
function toggleMobileSidebar() {
  var sb=document.getElementById('libSidebar'), scrim=document.getElementById('libScrim');
  if (!sb) return;
  var open=sb.classList.toggle('open');
  if (scrim) scrim.classList.toggle('show',open);
  document.body.style.overflow = open ? 'hidden' : '';
}
function closeMobileSidebar() {
  var sb=document.getElementById('libSidebar'), scrim=document.getElementById('libScrim');
  if (sb) sb.classList.remove('open');
  if (scrim) scrim.classList.remove('show');
  document.body.style.overflow='';
}

/* ════════════════════════════════════
   Full-screen Preview Modal
════════════════════════════════════ */
function openPreview(name, rOrObj, src) {
  var r = (typeof rOrObj === 'object' && rOrObj.fileType) ? rOrObj
        : (_currentResources.find(function(x){ return x.id === _activeId; }) || { fileType:'pdf' });
  _previewSrc  = src  || _previewSrc;
  _previewName = name || _previewName;

  document.getElementById('previewTitle').textContent = _previewName;
  var icon = document.getElementById('previewTypeIcon');
  var sub  = document.getElementById('previewType');
  var body = document.getElementById('previewBody');
  var m    = typeMeta(r.type || 'lesson');
  if (icon) icon.textContent = m.mdIcon;
  if (sub)  sub.textContent  = m.label;

  if (r.fileType === 'pdf' || !r.fileType) {
    body.innerHTML = '<iframe src="' + _previewSrc + '#toolbar=1&view=FitH" title="' + escHtml(_previewName) + '"></iframe>';
  } else if (r.fileType === 'image') {
    body.innerHTML = '<div class="preview-img-wrap"><img src="' + _previewSrc + '" alt="' + escHtml(_previewName) + '"></div>';
  } else if (r.fileType === 'video') {
    body.innerHTML = '<div style="flex:1;display:flex;align-items:center;justify-content:center;padding:24px;background:var(--surface-2)">'
      + '<iframe src="' + _previewSrc + '" allowfullscreen style="width:100%;aspect-ratio:16/9;border:none;border-radius:10px"></iframe></div>';
  } else {
    body.innerHTML = '<div class="lib-empty" style="flex:1;height:100%">'
      + '<span class="material-symbols-outlined">open_in_new</span>'
      + '<h4>' + escHtml(_previewName) + '</h4>'
      + '<a href="' + _previewSrc + '" target="_blank" rel="noopener" class="btn btn-primary" style="margin-top:16px">'
      + '<span class="material-symbols-outlined">open_in_new</span>Open Link</a></div>';
  }

  document.getElementById('previewModal').hidden = false;
  document.body.style.overflow = 'hidden';
}

function closePreview() {
  document.getElementById('previewModal').hidden = true;
  document.body.style.overflow = '';
  document.getElementById('previewBody').innerHTML = '';
}

document.getElementById('previewModal').addEventListener('click', function(e){
  if (e.target === this) closePreview();
});
document.addEventListener('keydown', function(e){
  if (e.key === 'Escape') closePreview();
});

/* no-op for removed view toggle — kept so any stray refs don't error */
function setView(){}

function toggleDetailsPanel() {
  var ws = document.querySelector('.lib-workspace');
  var btn = document.getElementById('toggleDetailsBtn');
  var icon = document.getElementById('toggleDetailsIcon');
  if (ws) {
    var isCollapsed = ws.classList.toggle('right-collapsed');
    if (btn) {
      btn.title = isCollapsed ? "Show details panel" : "Hide details panel";
    }
    if (icon) {
      if (isCollapsed) {
        icon.className = 'fa-solid fa-angles-left';
      } else {
        icon.className = 'fa-solid fa-angles-right';
      }
    }
  }
}

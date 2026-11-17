/* ══════════════════════════════════════════════════════════════
   NGIS Lesson Data — shared module
   Single source of truth for the Subject Library (lessons.html)
   and the dedicated Lesson Details viewer (lesson-details.html).
   Loaded BEFORE lessons.js / lesson-details.js.
   ══════════════════════════════════════════════════════════════ */

/* ── Resource data per subject ──
   type: lesson | worksheet | exam | formula | video | link
   fileType: pdf | image | video | link | quiz                */
var RESOURCES = {
  math: [
    {
      id: 'm1',
      name: 'Introduction to Algebra',
      fullName: 'Introduction to Algebra — Fundamentals',
      type: 'lesson',
      fileType: 'pdf',
      date: '2026-01-10',
      size: '1.4 MB',
      pages: 16,
      readTime: '15 min read',
      topic: 'Algebra',
      tone: 'tone-blue',
      formulas: ['f(x) = ax + b\nx = (-b ± √D)/2a\n∑ (x_i - μ)²'],
      desc: 'Fundamental theorems, variables, manipulation of polynomials, and foundational abstractions.',
      downloads: 98,
      tags: ['#Algebra', '#Grade10'],
      src: '../../assets/uploads/lessons/sample-lesson.pdf'
    },
    {
      id: 'm2',
      name: 'Linear Equations &...',
      fullName: 'Linear Equations & Inequalities',
      type: 'lesson',
      fileType: 'pdf',
      date: '2026-01-18',
      size: '2.1 MB',
      pages: 22,
      readTime: '20 min read',
      topic: 'Algebra',
      tone: 'tone-mint',
      formulas: ['y - y₀ = m(x - x₀)\n|ax + b| < c\nAx + By + C = 0'],
      desc: 'Comprehensive guide to single and multivariable systems, inequalities, and solution graphs.',
      downloads: 142,
      tags: ['#Algebra', '#Chapter3'],
      src: '../../assets/uploads/lessons/sample-lesson.pdf'
    },
    {
      id: 'm3',
      name: 'Quadratic Functions &...',
      fullName: 'Quadratic Functions & Curves',
      type: 'lesson',
      fileType: 'pdf',
      date: '2026-02-05',
      size: '3.2 MB',
      pages: 34,
      readTime: '25 min read',
      topic: 'Algebra',
      badge: 'Exam Focus',
      badgeClass: 'pill-green',
      tone: 'tone-peach',
      formulas: ['y = a(x - h)² + k\nΔ = b² - 4ac\nVertex: (-b/2a)'],
      desc: 'Parabolic behavior, discriminant analysis, optimization scenarios, and vertex calculations.',
      downloads: 117,
      tags: ['#Quadratic', '#Functions'],
      src: '../../assets/uploads/lessons/sample-lesson.pdf'
    },
    {
      id: 'm4',
      name: 'Calculus: Limits &...',
      fullName: 'Calculus: Limits & Derivatives',
      type: 'lesson',
      fileType: 'pdf',
      date: '2026-02-20',
      size: '4.0 MB',
      pages: 40,
      readTime: 'Advanced',
      topic: 'Calculus',
      tone: 'tone-cyan',
      formulas: ['lim (x→a) f(x) = L\ndy/dx = f\'(x)\nd/dx[uv] = u\'v + uv\''],
      desc: 'Differential calculus foundational rules, continuity criteria, rate of change, and limit theorems.',
      downloads: 203,
      tags: ['#Calculus', '#Grade11'],
      src: '../../assets/uploads/lessons/sample-lesson.pdf'
    },
    {
      id: 'm5',
      name: 'Analytic Geometry —...',
      fullName: 'Analytic Geometry — Circles',
      type: 'lesson',
      fileType: 'pdf',
      date: '2026-03-01',
      size: '2.8 MB',
      pages: 28,
      readTime: '18 min read',
      topic: 'Geometry',
      tone: 'tone-sand',
      formulas: ['(x - h)² + (y - k)² = r²\nx² + y² + 2gx = 0\nTangent: xx₁ + yy₁'],
      desc: 'Conic sections, radii calculations, secant equations, and locus problems in Cartesian space.',
      downloads: 89,
      tags: ['#Geometry', '#Circles'],
      src: '../../assets/uploads/lessons/sample-lesson.pdf'
    },
    {
      id: 'm7',
      name: 'Algebra Practice...',
      fullName: 'Algebra Practice Worksheet',
      type: 'worksheet',
      fileType: 'quiz',
      isQuiz: true,
      date: '2026-01-25',
      size: '0.8 MB',
      pages: 10,
      questions: 10,
      readTime: 'Interactive',
      topic: 'Interactive Exercise',
      badge: 'Interactive Exercise',
      badgeClass: 'pill-mint',
      tone: 'tone-green',
      formulas: ['[Q1] Find roots\n[Q2] Matrix det(A)\n[Q3] Solve system'],
      desc: 'Guided multi-tier problem set with automated hint checks and self-graded mastery validation.',
      downloads: 211,
      tags: ['#Algebra', '#Practice'],
      src: '../../assets/uploads/lessons/sample-lesson.pdf'
    }
  ],
  physics: [
    { id:'p1',  name:'Kinematics — Motion in 1D',           type:'lesson',    fileType:'pdf',   date:'2026-01-12', size:'2.0 MB', downloads:115, tags:['#Mechanics','#Kinematics'],    src:'../../assets/uploads/lessons/sample-lesson.pdf' },
    { id:'p2',  name:'Newton\'s Laws of Motion',            type:'lesson',    fileType:'pdf',   date:'2026-01-22', size:'2.5 MB', downloads:140, tags:['#Mechanics','#Newton'],        src:'../../assets/uploads/lessons/sample-lesson.pdf' },
    { id:'p3',  name:'Work, Energy & Power',                type:'lesson',    fileType:'pdf',   date:'2026-02-08', size:'3.0 MB', downloads:122, tags:['#Energy','#Work'],             src:'../../assets/uploads/lessons/sample-lesson.pdf' },
    { id:'p4',  name:'Electricity — Circuits & Ohm\'s Law', type:'lesson',    fileType:'pdf',   date:'2026-02-25', size:'2.8 MB', downloads:96,  tags:['#Electricity','#Circuits'],    src:'../../assets/uploads/lessons/sample-lesson.pdf' },
    { id:'p5',  name:'Waves & Oscillations',                type:'lesson',    fileType:'pdf',   date:'2026-03-10', size:'2.2 MB', downloads:88,  tags:['#Waves'],                      src:'../../assets/uploads/lessons/sample-lesson.pdf' },
    { id:'p6',  name:'Thermodynamics — Heat & Gas Laws',    type:'lesson',    fileType:'pdf',   date:'2026-03-25', size:'3.4 MB', downloads:101, tags:['#Thermo','#GasLaws'],          src:'../../assets/uploads/lessons/sample-lesson.pdf' },
    { id:'p7',  name:'Newton\'s Laws Practice Sheet',       type:'worksheet', fileType:'pdf',   date:'2026-01-28', size:'0.6 MB', downloads:178, tags:['#Mechanics','#Practice'],      src:'../../assets/uploads/lessons/sample-lesson.pdf' },
    { id:'p8',  name:'Circuit Problems Worksheet',          type:'worksheet', fileType:'pdf',   date:'2026-03-02', size:'0.9 MB', downloads:143, tags:['#Electricity','#Problems'],    src:'../../assets/uploads/lessons/sample-lesson.pdf' },
    { id:'p9',  name:'2024 Physics Final Exam',             type:'exam',      fileType:'pdf',   date:'2025-11-12', size:'2.1 MB', downloads:295, tags:['#PastExam','#2024'],           src:'../../assets/uploads/lessons/sample-lesson.pdf' },
    { id:'p10', name:'Physics Constants & Formulas Sheet',  type:'formula',   fileType:'pdf',   date:'2026-01-05', size:'0.3 MB', downloads:410, tags:['#Formula','#Constants'],       src:'../../assets/uploads/lessons/sample-lesson.pdf' },
    { id:'p11', name:'Waves Concept Explanation (Video)',   type:'video',     fileType:'video', date:'2026-03-18', size:'—',      downloads:0,   tags:['#Waves','#Video'],             src:'https://www.youtube.com/embed/dQw4w9WgXcQ' },
  ],
  chemistry: [
    { id:'c1',  name:'Atomic Structure & Periodic Table',  type:'lesson',    fileType:'pdf',   date:'2026-01-14', size:'2.3 MB', downloads:108, tags:['#Atoms','#PeriodicTable'],     src:'../../assets/uploads/lessons/sample-lesson.pdf' },
    { id:'c2',  name:'Chemical Bonding',                   type:'lesson',    fileType:'pdf',   date:'2026-01-28', size:'2.7 MB', downloads:93,  tags:['#Bonding'],                    src:'../../assets/uploads/lessons/sample-lesson.pdf' },
    { id:'c3',  name:'Stoichiometry & Moles',              type:'lesson',    fileType:'pdf',   date:'2026-02-14', size:'1.8 MB', downloads:112, tags:['#Stoich','#Moles'],            src:'../../assets/uploads/lessons/sample-lesson.pdf' },
    { id:'c4',  name:'Acids, Bases & Salts',               type:'lesson',    fileType:'pdf',   date:'2026-03-03', size:'2.0 MB', downloads:87,  tags:['#AcidBase','#pH'],             src:'../../assets/uploads/lessons/sample-lesson.pdf' },
    { id:'c5',  name:'Organic Chemistry — Hydrocarbons',   type:'lesson',    fileType:'pdf',   date:'2026-03-20', size:'3.1 MB', downloads:79,  tags:['#Organic'],                    src:'../../assets/uploads/lessons/sample-lesson.pdf' },
    { id:'c6',  name:'Mole Calculations Worksheet',        type:'worksheet', fileType:'pdf',   date:'2026-02-20', size:'0.7 MB', downloads:161, tags:['#Stoich','#Worksheet'],        src:'../../assets/uploads/lessons/sample-lesson.pdf' },
    { id:'c7',  name:'2024 Chemistry Final Exam',          type:'exam',      fileType:'pdf',   date:'2025-11-14', size:'2.0 MB', downloads:260, tags:['#PastExam','#2024'],           src:'../../assets/uploads/lessons/sample-lesson.pdf' },
    { id:'c8',  name:'Periodic Table Reference Sheet',     type:'formula',   fileType:'pdf',   date:'2026-01-03', size:'0.4 MB', downloads:488, tags:['#Formula','#PeriodicTable'],   src:'../../assets/uploads/lessons/sample-lesson.pdf' },
    { id:'c9',  name:'Reaction Types Formula Card',        type:'formula',   fileType:'pdf',   date:'2026-02-01', size:'0.2 MB', downloads:312, tags:['#Formula','#Reactions'],       src:'../../assets/uploads/lessons/sample-lesson.pdf' },
  ],
  biology: [
    { id:'b1',  name:'Cell Structure & Functions',         type:'lesson',    fileType:'pdf',   date:'2026-01-11', size:'2.6 MB', downloads:99,  tags:['#Cells','#Biology'],           src:'../../assets/uploads/lessons/sample-lesson.pdf' },
    { id:'b2',  name:'Genetics & DNA Replication',         type:'lesson',    fileType:'pdf',   date:'2026-01-25', size:'3.0 MB', downloads:118, tags:['#Genetics','#DNA'],            src:'../../assets/uploads/lessons/sample-lesson.pdf' },
    { id:'b3',  name:'Photosynthesis & Respiration',       type:'lesson',    fileType:'pdf',   date:'2026-02-10', size:'2.4 MB', downloads:105, tags:['#Photosynthesis'],             src:'../../assets/uploads/lessons/sample-lesson.pdf' },
    { id:'b4',  name:'Ecosystems & Biodiversity',          type:'lesson',    fileType:'pdf',   date:'2026-03-01', size:'2.9 MB', downloads:88,  tags:['#Ecosystems'],                 src:'../../assets/uploads/lessons/sample-lesson.pdf' },
    { id:'b5',  name:'Human Body Systems Overview',        type:'lesson',    fileType:'pdf',   date:'2026-03-18', size:'3.5 MB', downloads:122, tags:['#HumanBody'],                  src:'../../assets/uploads/lessons/sample-lesson.pdf' },
    { id:'b6',  name:'Cell Division Worksheet',            type:'worksheet', fileType:'pdf',   date:'2026-02-03', size:'0.5 MB', downloads:145, tags:['#Cells','#Mitosis'],           src:'../../assets/uploads/lessons/sample-lesson.pdf' },
    { id:'b7',  name:'Genetics Problem Set',               type:'worksheet', fileType:'pdf',   date:'2026-02-18', size:'0.8 MB', downloads:177, tags:['#Genetics','#Mendel'],         src:'../../assets/uploads/lessons/sample-lesson.pdf' },
    { id:'b8',  name:'2024 Biology Final Exam',            type:'exam',      fileType:'pdf',   date:'2025-11-10', size:'2.2 MB', downloads:277, tags:['#PastExam','#2024'],           src:'../../assets/uploads/lessons/sample-lesson.pdf' },
    { id:'b9',  name:'Biology Key Terms & Diagrams',       type:'formula',   fileType:'pdf',   date:'2026-01-07', size:'1.0 MB', downloads:320, tags:['#Reference','#Diagrams'],      src:'../../assets/uploads/lessons/sample-lesson.pdf' },
  ],
  english: [
    { id:'e1',  name:'Essay Writing — Structure & Style',  type:'lesson',    fileType:'pdf',   date:'2026-01-10', size:'1.5 MB', downloads:88,  tags:['#Writing','#Essay'],           src:'../../assets/uploads/lessons/sample-lesson.pdf' },
    { id:'e2',  name:'Grammar: Clauses & Sentence Types',  type:'lesson',    fileType:'pdf',   date:'2026-01-24', size:'1.8 MB', downloads:104, tags:['#Grammar'],                    src:'../../assets/uploads/lessons/sample-lesson.pdf' },
    { id:'e3',  name:'Literature Analysis: Short Stories', type:'lesson',    fileType:'pdf',   date:'2026-02-12', size:'2.0 MB', downloads:79,  tags:['#Literature','#Analysis'],     src:'../../assets/uploads/lessons/sample-lesson.pdf' },
    { id:'e4',  name:'Grammar Practice Worksheet B',       type:'worksheet', fileType:'pdf',   date:'2026-02-20', size:'0.6 MB', downloads:165, tags:['#Grammar','#Practice'],        src:'../../assets/uploads/lessons/sample-lesson.pdf' },
    { id:'e5',  name:'Vocabulary Builder Worksheet',       type:'worksheet', fileType:'pdf',   date:'2026-03-05', size:'0.5 MB', downloads:143, tags:['#Vocabulary'],                 src:'../../assets/uploads/lessons/sample-lesson.pdf' },
    { id:'e6',  name:'2024 English Final Exam',            type:'exam',      fileType:'pdf',   date:'2025-11-08', size:'1.9 MB', downloads:240, tags:['#PastExam','#2024'],           src:'../../assets/uploads/lessons/sample-lesson.pdf' },
    { id:'e7',  name:'Writing Structures Reference Card',  type:'formula',   fileType:'pdf',   date:'2026-01-06', size:'0.3 MB', downloads:298, tags:['#Formula','#Writing'],         src:'../../assets/uploads/lessons/sample-lesson.pdf' },
  ],
  history: [
    { id:'h1',  name:'Angkor Empire — Rise & Fall',        type:'lesson',    fileType:'pdf',   date:'2026-01-13', size:'2.1 MB', downloads:92,  tags:['#Cambodia','#Angkor'],         src:'../../assets/uploads/lessons/sample-lesson.pdf' },
    { id:'h2',  name:'World War II — Causes & Effects',    type:'lesson',    fileType:'pdf',   date:'2026-02-04', size:'2.9 MB', downloads:134, tags:['#WW2','#WorldHistory'],        src:'../../assets/uploads/lessons/sample-lesson.pdf' },
    { id:'h3',  name:'Cold War & Decolonisation',          type:'lesson',    fileType:'pdf',   date:'2026-02-22', size:'2.5 MB', downloads:110, tags:['#ColdWar','#Modern'],          src:'../../assets/uploads/lessons/sample-lesson.pdf' },
    { id:'h4',  name:'Primary Source Analysis Worksheet',  type:'worksheet', fileType:'pdf',   date:'2026-03-01', size:'0.7 MB', downloads:99,  tags:['#Sources','#Analysis'],        src:'../../assets/uploads/lessons/sample-lesson.pdf' },
    { id:'h5',  name:'2024 History Final Exam',            type:'exam',      fileType:'pdf',   date:'2025-11-06', size:'1.8 MB', downloads:215, tags:['#PastExam','#2024'],           src:'../../assets/uploads/lessons/sample-lesson.pdf' },
  ],
  geography: [
    { id:'g1',  name:'Physical Geography — Landforms',     type:'lesson',    fileType:'pdf',   date:'2026-01-15', size:'2.4 MB', downloads:77,  tags:['#Landforms'],                  src:'../../assets/uploads/lessons/sample-lesson.pdf' },
    { id:'g2',  name:'Climate Zones & Weather Systems',    type:'lesson',    fileType:'pdf',   date:'2026-02-06', size:'2.2 MB', downloads:85,  tags:['#Climate','#Weather'],         src:'../../assets/uploads/lessons/sample-lesson.pdf' },
    { id:'g3',  name:'Map Reading & Cartography',          type:'lesson',    fileType:'pdf',   date:'2026-03-10', size:'1.7 MB', downloads:71,  tags:['#Maps','#Cartography'],        src:'../../assets/uploads/lessons/sample-lesson.pdf' },
    { id:'g4',  name:'Map Skills Worksheet',               type:'worksheet', fileType:'pdf',   date:'2026-03-15', size:'0.6 MB', downloads:118, tags:['#Maps','#Practice'],           src:'../../assets/uploads/lessons/sample-lesson.pdf' },
    { id:'g5',  name:'2024 Geography Final Exam',          type:'exam',      fileType:'pdf',   date:'2025-11-07', size:'1.9 MB', downloads:188, tags:['#PastExam','#2024'],           src:'../../assets/uploads/lessons/sample-lesson.pdf' },
  ],
  cs: [
    { id:'cs1', name:'Introduction to Programming (Python)', type:'lesson',  fileType:'pdf',   date:'2026-01-09', size:'2.0 MB', downloads:178, tags:['#Python','#Programming'],      src:'../../assets/uploads/lessons/sample-lesson.pdf' },
    { id:'cs2', name:'Data Structures — Arrays & Lists',   type:'lesson',    fileType:'pdf',   date:'2026-01-23', size:'2.6 MB', downloads:155, tags:['#DataStructures'],             src:'../../assets/uploads/lessons/sample-lesson.pdf' },
    { id:'cs3', name:'Algorithms: Searching & Sorting',    type:'lesson',    fileType:'pdf',   date:'2026-02-11', size:'3.1 MB', downloads:199, tags:['#Algorithms','#Sorting'],      src:'../../assets/uploads/lessons/sample-lesson.pdf' },
    { id:'cs4', name:'Web Development Basics (HTML/CSS)',  type:'lesson',    fileType:'pdf',   date:'2026-02-28', size:'2.4 MB', downloads:212, tags:['#Web','#HTML'],                src:'../../assets/uploads/lessons/sample-lesson.pdf' },
    { id:'cs5', name:'Databases & SQL Fundamentals',       type:'lesson',    fileType:'pdf',   date:'2026-03-14', size:'2.8 MB', downloads:167, tags:['#SQL','#Databases'],           src:'../../assets/uploads/lessons/sample-lesson.pdf' },
    { id:'cs6', name:'OOP Concepts in Python',             type:'lesson',    fileType:'pdf',   date:'2026-03-28', size:'3.5 MB', downloads:145, tags:['#OOP','#Python'],              src:'../../assets/uploads/lessons/sample-lesson.pdf' },
    { id:'cs7', name:'Python Coding Exercises Set A',      type:'worksheet', fileType:'pdf',   date:'2026-01-30', size:'0.8 MB', downloads:234, tags:['#Python','#Exercises'],        src:'../../assets/uploads/lessons/sample-lesson.pdf' },
    { id:'cs8', name:'Algorithm Design Worksheet',         type:'worksheet', fileType:'pdf',   date:'2026-02-15', size:'1.0 MB', downloads:196, tags:['#Algorithms','#Design'],       src:'../../assets/uploads/lessons/sample-lesson.pdf' },
    { id:'cs9', name:'SQL Query Practice Sheet',           type:'worksheet', fileType:'pdf',   date:'2026-03-18', size:'0.7 MB', downloads:155, tags:['#SQL','#Queries'],             src:'../../assets/uploads/lessons/sample-lesson.pdf' },
    { id:'cs10',name:'2024 CS Final Exam',                 type:'exam',      fileType:'pdf',   date:'2025-11-11', size:'2.3 MB', downloads:305, tags:['#PastExam','#2024'],           src:'../../assets/uploads/lessons/sample-lesson.pdf' },
    { id:'cs11',name:'2023 CS Mid-Term Exam',              type:'exam',      fileType:'pdf',   date:'2025-05-20', size:'1.7 MB', downloads:258, tags:['#PastExam','#MidTerm'],        src:'../../assets/uploads/lessons/sample-lesson.pdf' },
    { id:'cs12',name:'Big-O Complexity Reference Sheet',   type:'formula',   fileType:'pdf',   date:'2026-01-04', size:'0.2 MB', downloads:389, tags:['#Formula','#BigO'],            src:'../../assets/uploads/lessons/sample-lesson.pdf' },
    { id:'cs13',name:'Python Syntax Cheat Sheet',          type:'formula',   fileType:'pdf',   date:'2026-02-02', size:'0.3 MB', downloads:441, tags:['#Formula','#Python'],          src:'../../assets/uploads/lessons/sample-lesson.pdf' },
    { id:'cs14',name:'W3Schools — HTML Reference',         type:'link',      fileType:'link',  date:'2026-01-01', size:'—',      downloads:0,   tags:['#External','#HTML'],           src:'https://www.w3schools.com/html/' },
    { id:'cs15',name:'CS50 — Intro to CS (Video)',         type:'video',     fileType:'video', date:'2026-02-01', size:'—',      downloads:0,   tags:['#Video','#CS50'],              src:'https://www.youtube.com/embed/dQw4w9WgXcQ' },
  ]
};

/* ── Subject titles & icons ── */
var OAK_SUBJECT_TITLES = {
  math: 'MATHEMATICS',
  physics: 'PHYSICS',
  chemistry: 'CHEMISTRY',
  biology: 'BIOLOGY',
  english: 'ENGLISH LANGUAGE',
  history: 'HISTORY',
  geography: 'GEOGRAPHY',
  cs: 'COMPUTER SCIENCE'
};

var OAK_SUBJECT_ICONS = {
  math: { icon: 'calculate', color: '#1565c0' },
  physics: { icon: 'bolt', color: '#6a1b9a' },
  chemistry: { icon: 'science', color: '#00695c' },
  biology: { icon: 'biotech', color: '#2e7d32' },
  english: { icon: 'menu_book', color: '#b71c1c' },
  history: { icon: 'history_edu', color: '#c62828' },
  geography: { icon: 'public', color: '#e65100' },
  cs: { icon: 'laptop_code', color: '#1565c0' }
};

/* ── Type meta helpers ── */
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

/* ── File-type icon & colour map ── */
var FILE_TYPE_STYLE = {
  pdf:   { icon:'picture_as_pdf', bg:'#ffebee', color:'#e53935', badge:'pdf-ic'  },
  image: { icon:'image',          bg:'#f3e5f5', color:'#8e24aa', badge:'img-ic'  },
  video: { icon:'play_circle',    bg:'#e0f7fa', color:'#00838f', badge:'vid-ic'  },
  link:  { icon:'open_in_new',    bg:'#e3f2fd', color:'#1565c0', badge:'link-ic' }
};
function fileTypeStyle(ft) {
  return FILE_TYPE_STYLE[ft] || FILE_TYPE_STYLE['pdf'];
}

/* ── Resource descriptions (keyed by id) ── */
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

/* ══════════════════════════════════════════════════════════════
   Shared Bookmark Store — persisted in localStorage so bookmark
   state stays consistent between the Subject Library cards and
   the Lesson Details page.
   ══════════════════════════════════════════════════════════════ */
var NGIS_BOOKMARK_KEY = 'ngis-bookmarked-ids';
var NGISBookmarks = {
  _ids: (function () {
    try { return JSON.parse(localStorage.getItem(NGIS_BOOKMARK_KEY)) || {}; }
    catch (e) { return {}; }
  })(),
  has: function (id) { return !!this._ids[id]; },
  toggle: function (id) {
    if (this._ids[id]) { delete this._ids[id]; } else { this._ids[id] = true; }
    try { localStorage.setItem(NGIS_BOOKMARK_KEY, JSON.stringify(this._ids)); } catch (e) {}
    return !!this._ids[id];
  },
  /* Sync a bookmark button's icon + class to the stored state */
  syncButton: function (btn, id) {
    if (!btn) return this.has(id);
    var active = this.has(id);
    var ico = btn.querySelector('[data-ngis-icon]');
    if (ico) ico.setAttribute('data-ngis-icon', active ? 'bookmarkAdded' : 'bookmark');
    btn.classList.toggle('active', active);
    btn.classList.toggle('bookmarked', active);
    if (window.NGIS && window.NGIS.hydrate) window.NGIS.hydrate(btn);
    return active;
  }
};

/* ── Shared URL builder for the dedicated lesson page ── */
function lessonDetailsUrl(resId, dept, role) {
  return 'lesson-details.html?id=' + encodeURIComponent(resId)
    + '&dept=' + encodeURIComponent(dept || 'math')
    + '&portal=' + encodeURIComponent(role || 'student');
}

/* ── Trigger a file download (reused by library & details pages) ── */
function ngisDownloadFile(src, name) {
  if (!src) return;
  var a = document.createElement('a');
  a.href = src; a.download = name || 'download'; a.target = '_blank'; a.rel = 'noopener';
  document.body.appendChild(a); a.click(); document.body.removeChild(a);
}

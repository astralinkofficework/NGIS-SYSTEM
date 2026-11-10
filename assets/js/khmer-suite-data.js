/* ============================================================================
   Khmer School Admin Suite — data layer
   Seed state, Khmer numerals, grid keys and a zero-dependency XLSX writer.
   Loaded as a plain script; publishes window.KSData.
   ========================================================================== */
(function (global) {
  'use strict';

  var DAYS = ['ច័ន្ទ', 'អង្គារ', 'ពុធ', 'ព្រហស្បតិ៍', 'សុក្រ', 'សៅរ៍'];
  var SHIFTS = ['ព្រឹក', 'រសៀល'];
  var MORNING_STARTS = ['07:00', '07:50', '08:40', '09:30', '10:20'];
  var AFTERNOON_STARTS = ['13:00', '13:50', '14:40', '15:30', '16:20'];

  // code, Khmer name, English, short name, colour, lessons/week
  var SUBJECT_DEFS = [
    ['K',  'ខ្មែរ',        'Khmer',              'ខ្មែរ',   '#FED766', 6],
    ['M',  'គណិតវិទ្យា',  'Mathematics',        'គណិត',   '#93C5FD', 6],
    ['EN', 'អង់គ្លេស',     'English',            'អង់',     '#99F6E4', 4],
    ['P',  'រូបវិទ្យា',    'Physics',            'រូប',     '#DDD6FE', 2],
    ['C',  'គីមីវិទ្យា',   'Chemistry',          'គីមី',   '#FBCFE8', 2],
    ['B',  'ជីវវិទ្យា',    'Biology',            'ជីវ',     '#A7F3D0', 2],
    ['ES', 'ភូមិវិទ្យា',   'Earth Science',      'ភូមិ',   '#FED7AA', 2],
    ['G',  'កុំព្យូទ័រ',   'Computer Studies',   'កុំព្យូ', '#BAE6FD', 2],
    ['H',  'ប្រវត្តិវិទ្យា', 'History',           'ប្រវត្តិ','#FDE68A', 2],
    ['I',  'ពលរដ្ឋ',       'Civics',             'ពល',     '#C7D2FE', 2],
    ['IT', 'កីឡា',         'Physical Education', 'កីឡា',   '#FECDD3', 2],
    ['ED', 'អប់រំសីលធម៌', 'Moral Education',    'សីលធម៌', '#FEF3C7', 2],
    ['SH', 'ភាសា',         'Social Language',    'ភាសា',   '#E9D5FF', 0]
  ];

  var TEACHER_NAMES = [
    'សុខ ដារ៉ា', 'តាន់ ធីតា', 'ហេង វីរៈ', 'ជើន ម៉ារី', 'ណុង សុធា',
    'យ៉ុក សុីន', 'ប៉ុក សុភី', 'អ៊ុក ចាន់ថា', 'លី សុភាព', 'ម៉ៅ ដារ៉ាវី',
    'គឹម ស្រីពេជ្រ', 'ចាន់ សុខលី', 'ប្រាក់ មុនី', 'អ៊ឹង រិទ្ធី', 'ស៊ុន ច័ន្ទណ៍',
    'ទូច សុភក្ត្រា', 'វ៉ាន់ សុភ័ក្ត្រ', 'រស់ សុគន្ធា', 'ខូវ ចាន់ដារ៉ា', 'ឈឹម ស្រីល័ក្ខ',
    'នូ សុខហេង', 'គង់ សុភាវី', 'ឡុង ចាន់ថុល', 'ប៉ែន សុភាវី', 'អន សុខរិទ្ធ',
    'សេង ដារ៉ាវុធ', 'ហ៊ុន មាលី', 'ជា សុភីរិទ្ធ', 'ផន ចាន់សុភា', 'ប៊ុន ស្រីមុំ',
    'វង្ស សុខាន់', 'តេង សុភ័ក្ត្រ'
  ];

  var CURRICULUM = {};
  SUBJECT_DEFS.forEach(function (d) { CURRICULUM[d[0]] = d[5]; });

  var RECORD_COLUMNS = [
    { key: 'no',            kh: 'ល.រ',                    en: 'No.' },
    { key: 'name',          kh: 'គោត្តនាម-នាម',           en: 'Full name' },
    { key: 'gender',        kh: 'ភេទ',                    en: 'Gender' },
    { key: 'dob',           kh: 'ថ្ងៃខែឆ្នាំកំណើត',       en: 'Date of birth' },
    { key: 'grade',         kh: 'ឆ្នាំ',                   en: 'Grade' },
    { key: 'code',          kh: 'កូដ',                    en: 'Code' },
    { key: 'birth_place',   kh: 'ទីកន្លែងកំណើត',         en: 'Place of birth' },
    { key: 'address',       kh: 'អាសយដ្ឋាន',              en: 'Address' },
    { key: 'language',      kh: 'ភាសា៖ ទូទាត់',          en: 'Language' },
    { key: 'id_number',     kh: 'អត្តលេខ',                en: 'ID number' },
    { key: 'registered_at', kh: 'កាលបរិច្ឆេទចុះឈ្មោះ', en: 'Registered' },
    { key: 'homeroom',      kh: 'គ្រូបង្រៀន',            en: 'Homeroom teacher' }
  ];

  var TEACHER_SPREADSHEET_COLUMNS = [
    { key: 'no', kh: 'ជួរ', en: 'Row', width: 48, readOnly: true },
    { key: 'name_kh', kh: 'ឈ្មោះ', en: 'Full Name', width: 140, required: true },
    { key: 'gender', kh: 'ភេទ', en: 'Gender', width: 65 },
    { key: 'phone', kh: 'ទូរស័ព្ទ', en: 'Phone', width: 110 },
    { key: 'position', kh: 'តួនាទី', en: 'Position', width: 110 },
    { key: 'category', kh: 'ក្របខ័ណ្ឌ', en: 'Category', width: 110 },
    { key: 'rank', kh: 'ឋានន្តរស័ក្ដិ', en: 'Rank', width: 110 },
    { key: 'specialization', kh: 'ឯកទេស', en: 'Specialization', width: 110 },
    { key: 'code', kh: 'កូដគ្រូ', en: 'Teacher Code', width: 80, required: true },
    { key: 'target', kh: 'ម៉ោងកំណត់', en: 'Target Hours', width: 85, type: 'number' },
    { key: 'max_daily', kh: 'អតិបរមា/ថ្ងៃ', en: 'Max/Day', width: 85, type: 'number' },
    { key: 'employee_id', kh: 'អត្តលេខមន្ត្រី', en: 'Employee ID', width: 110 },
    { key: 'start_year', kh: 'ឆ្នាំចូលបម្រើការងារ', en: 'Start Year', width: 95, type: 'number' },
    { key: 'notes', kh: 'កំណត់សម្គាល់', en: 'Notes', width: 140 }
  ];

  function parseClipboardTable(text) {
    if (!text || typeof text !== 'string') return [];
    var lines = text.trim().split(/\r?\n/);
    return lines.map(function (line) {
      if (line.indexOf('\t') !== -1) {
        return line.split('\t').map(function (c) { return c.trim(); });
      }
      return line.split(',').map(function (c) { return c.trim(); });
    });
  }

  function formatClipboardTable(matrix) {
    if (!Array.isArray(matrix)) return '';
    return matrix.map(function (row) {
      return (Array.isArray(row) ? row : [row]).join('\t');
    }).join('\n');
  }

  function kh(value) {
    return String(value == null ? '' : value);
  }

  var DAY_EN = {
    'ច័ន្ទ': 'Monday',
    'អង្គារ': 'Tuesday',
    'ពុធ': 'Wednesday',
    'ព្រហស្បតិ៍': 'Thursday',
    'សុក្រ': 'Friday',
    'សៅរ៍': 'Saturday'
  };
  var DAY_SHORT_EN = {
    'ច័ន្ទ': 'Mon',
    'អង្គារ': 'Tue',
    'ពុធ': 'Wed',
    'ព្រហស្បតិ៍': 'Thu',
    'សុក្រ': 'Fri',
    'សៅរ៍': 'Sat'
  };
  var SHIFT_EN = {
    'ព្រឹក': 'Morning',
    'រសៀល': 'Afternoon'
  };
  var TEACHER_EN_NAMES = {
    'សុខ ដារ៉ា': 'Sok Dara',
    'សុខ ដារ៉ា (Updated)': 'Sok Dara',
    'សុខ ដារ៉ា (Updated Name)': 'Sok Dara',
    'តាន់ ធីតា': 'Tan Thida',
    'ហេង វីរៈ': 'Heng Virak',
    'ជើន ម៉ារី': 'Cheun Mary',
    'ណុង សុធា': 'Nong Sothea',
    'យ៉ុក សុីន': 'Yok Sin',
    'ប៉ុក សុភី': 'Pok Sophy',
    'អ៊ុក ចាន់ថា': 'Ouk Chantha',
    'លី សុភាព': 'Ly Sopheap',
    'ម៉ៅ ដារ៉ាវី': 'Mao Daravy',
    'គឹម ស្រីពេជ្រ': 'Kim Sreypich',
    'ចាន់ សុខលី': 'Chan Sokhly',
    'ប្រាក់ មុនី': 'Prak Mony',
    'អ៊ឹង រិទ្ធី': 'Oeng Rithy',
    'ស៊ុន ច័ន្ទណ៍': 'Sun Chan',
    'ទូច សុភក្ត្រា': 'Touch Sopheaktra',
    'វ៉ាន់ សុភ័ក្ត្រ': 'Van Sopheak',
    'រស់ សុគន្ធា': 'Ros Sokunthea',
    'ខូវ ចាន់ដារ៉ា': 'Khov Chandara',
    'ឈឹម ស្រីល័ក្ខ': 'Chhim Sreyleak',
    'នូ សុខហេង': 'Nou Sokheng',
    'គង់ សុភាវី': 'Kong Sopheavy',
    'ឡុង ចាន់ថុល': 'Long Chanthol',
    'ប៉ែន សុភាវី': 'Pen Sopheavy',
    'អន សុខរិទ្ធ': 'Orn Sokrith',
    'សេង ដារ៉ាវុធ': 'Seng Daravuth',
    'ហ៊ុន មាលី': 'Hun Maly',
    'ជា សុភីរិទ្ធ': 'Chea Sophearith',
    'ផន ចាន់សុភា': 'Phorn Chansophea',
    'ប៊ុន ស្រីមុំ': 'Bun Sreymom',
    'វង្ស សុខាន់': 'Vong Sokhan',
    'តេង សុភ័ក្ត្រ': 'Teng Sopheaktra',
    'គ្រូថ្មី ពិសិដ្ឋ': 'Piseth New'
  };

  var SUBJECT_EN_NAMES = {
    'sub_K': 'Khmer Literature',
    'sub_M': 'Mathematics',
    'sub_EN': 'English',
    'sub_P': 'Physics',
    'sub_C': 'Chemistry',
    'sub_B': 'Biology',
    'sub_ES': 'Earth Science',
    'sub_G': 'Computer Studies',
    'sub_H': 'History',
    'sub_I': 'Moral & Civics',
    'sub_IT': 'Physical Education',
    'sub_ED': 'Economics',
    'sub_SH': 'Social Language',
    'K': 'Khmer Literature',
    'M': 'Mathematics',
    'EN': 'English',
    'P': 'Physics',
    'C': 'Chemistry',
    'B': 'Biology',
    'ES': 'Earth Science',
    'G': 'Computer Studies',
    'H': 'History',
    'I': 'Moral & Civics',
    'IT': 'Physical Education',
    'ED': 'Economics',
    'SH': 'Social Language',
    'ភាសាខ្មែរ': 'Khmer Literature',
    'គណិតវិទ្យា': 'Mathematics',
    'ភាសាអង់គ្លេស': 'English',
    'រូបវិទ្យា': 'Physics',
    'គីមីវិទ្យា': 'Chemistry',
    'ជីវវិទ្យា': 'Biology',
    'ផែនដីវិទ្យា': 'Earth Science',
    'វិទ្យាសាស្ត្រកុំព្យូទ័រ': 'Computer Studies',
    'កុំព្យូទ័រ': 'Computer Studies',
    'ប្រវត្តិវិទ្យា': 'History',
    'សីលធម៌-ពលរដ្ឋ': 'Moral & Civics',
    'អប់រំកាយ និងកីឡា': 'Physical Education',
    'សេដ្ឋកិច្ច': 'Economics',
    'ភាសាសង្គម': 'Social Language',
    'ភូមិវិទ្យា': 'Geography',
    'ខ្មែរ': 'Khmer',
    'គណិត': 'Math',
    'អង់គ្លេស': 'English',
    'រូប': 'Physics',
    'គីមី': 'Chemistry',
    'ជីវ': 'Biology',
    'ផែនដី': 'Earth Sci',
    'ប្រវត្តិ': 'History',
    'សីលធម៌': 'Civics',
    'កីឡា': 'PE',
    'សេដ្ឋ': 'Econ',
    'ពលរដ្ឋ': 'Moral & Civics',
    'ពល': 'Civics',
    'ទូទៅ': 'General Studies'
  };

  var POSITION_EN = {
    'គ្រូបង្រៀន': 'Teacher',
    'នាយក': 'Principal',
    'នាយករង': 'Vice Principal',
    'ប្រធានដេប៉ាតឺម៉ង់': 'Department Head',
    'គ្រូបន្ទុកថ្នាក់': 'Homeroom Teacher'
  };
  var CATEGORY_EN = {
    'ក្របខ័ណ្ឌរដ្ឋ': 'State Framework / Civil Servant',
    'កិច្ចសន្យា': 'Contract Teacher',
    'ពេញម៉ោង': 'Full-time',
    'ក្រៅម៉ោង': 'Part-time'
  };
  var RANK_EN = {
    'គ្រូកម្រិតឧត្តម': 'Senior Teacher',
    'គ្រូមូលដ្ឋាន': 'Junior Teacher',
    'គ្រូបឋម': 'Primary Teacher'
  };

  function toEnDay(d, short) {
    if (short) return DAY_SHORT_EN[d] || d;
    return DAY_EN[d] || d;
  }

  function toEnShift(s) {
    return SHIFT_EN[s] || s;
  }

  function toEnTeacher(t) {
    if (!t) return '';
    if (typeof t === 'string') return TEACHER_EN_NAMES[t] || t;
    return t.name_en || TEACHER_EN_NAMES[t.name_kh] || t.name_kh || t.id;
  }

  function toEnSubject(s) {
    if (!s) return '';
    if (typeof s === 'string') {
      var trimmed = s.trim();
      if (SUBJECT_EN_NAMES[trimmed]) return SUBJECT_EN_NAMES[trimmed];
      for (var k in SUBJECT_EN_NAMES) {
        if (k.length >= 2 && trimmed.indexOf(k) !== -1) return SUBJECT_EN_NAMES[k];
      }
      return trimmed;
    }
    return s.name_en || SUBJECT_EN_NAMES[s.name_kh] || SUBJECT_EN_NAMES[s.code] || SUBJECT_EN_NAMES[s.id] || s.name_kh || s.code;
  }

  function toEnRoom(r) {
    if (!r) return 'Room 101';
    var clean = String(r).replace(/បន្ទប់[់]*\s*[:ៈ]*/g, '').replace(/^Room\s*/i, '').trim();
    return clean ? ('Room ' + clean) : 'Room 101';
  }

  function toEnClass(c) {
    if (!c) return '';
    var raw = typeof c === 'string' ? c : (c.display || c.id || '');
    return String(raw).replace(/^class_/, '').replace(/^ថ្នាក់\s*/, '').trim();
  }

  function toEnPosition(p) {
    if (!p) return 'Teacher';
    return POSITION_EN[p] || p;
  }

  function toEnCategory(c) {
    if (!c) return 'State Framework';
    return CATEGORY_EN[c] || c;
  }

  function toEnRank(r) {
    if (!r) return 'Senior Teacher';
    return RANK_EN[r] || r;
  }

  function toEnGender(g) {
    if (g === 'ស្រី' || g === 'Female' || g === 'F') return 'Female';
    return 'Male';
  }

  var SUBJECT_COLOR_PALETTE = {
    'K':    '#FED766', // Khmer (Warm Amber Yellow)
    'M':    '#93C5FD', // Mathematics (Soft Sky Blue)
    'EN':   '#99F6E4', // English (Mint Teal)
    'P':    '#DDD6FE', // Physics (Lavender Violet)
    'C':    '#FBCFE8', // Chemistry (Soft Rose Pink)
    'B':    '#A7F3D0', // Biology (Light Emerald Green)
    'ES':   '#FED7AA', // Earth Science / Geography (Warm Peach)
    'GEO':  '#FED7AA',
    'G':    '#BAE6FD', // Computer Studies / ICT (Ice Blue)
    'H':    '#FDE68A', // History (Warm Apricot)
    'I':    '#C7D2FE', // Civics / Moral (Periwinkle Indigo)
    'IT':   '#FECDD3', // Physical Education / Sports (Coral Pink)
    'PE':   '#FECDD3',
    'ED':   '#FEF3C7', // Moral Education / Economics (Creamy Sage)
    'ECO':  '#FEF3C7',
    'SH':   '#E9D5FF'  // Social Language (Soft Lilac Purple)
  };

  function getSubjectColor(subjectId, subName, rawColor) {
    var sId = String(subjectId || '').trim();
    var code = sId.replace(/^sub_/, '').toUpperCase();
    if (SUBJECT_COLOR_PALETTE[code]) return SUBJECT_COLOR_PALETTE[code];
    if (SUBJECT_COLOR_PALETTE[sId]) return SUBJECT_COLOR_PALETTE[sId];

    var s = String(subName || '').toLowerCase();
    if (s.indexOf('ខ្មែរ') !== -1 || s.indexOf('khmer') !== -1) return '#FED766';
    if (s.indexOf('គណិត') !== -1 || s.indexOf('math') !== -1) return '#93C5FD';
    if (s.indexOf('អង់គ្លេស') !== -1 || s.indexOf('english') !== -1 || s.indexOf('eng') !== -1) return '#99F6E4';
    if (s.indexOf('រូប') !== -1 || s.indexOf('physic') !== -1) return '#DDD6FE';
    if (s.indexOf('គីមី') !== -1 || s.indexOf('chem') !== -1) return '#FBCFE8';
    if (s.indexOf('ជីវ') !== -1 || s.indexOf('bio') !== -1) return '#A7F3D0';
    if (s.indexOf('ភូមិ') !== -1 || s.indexOf('ផែនដី') !== -1 || s.indexOf('geo') !== -1 || s.indexOf('earth') !== -1) return '#FED7AA';
    if (s.indexOf('កុំព្យូទ័រ') !== -1 || s.indexOf('ព័ត៌មាន') !== -1 || s.indexOf('ict') !== -1 || s.indexOf('computer') !== -1) return '#BAE6FD';
    if (s.indexOf('ប្រវត្តិ') !== -1 || s.indexOf('histor') !== -1) return '#FDE68A';
    if (s.indexOf('ពលរដ្ឋ') !== -1 || s.indexOf('សីលធម៌') !== -1 || s.indexOf('civic') !== -1 || s.indexOf('moral') !== -1) return '#C7D2FE';
    if (s.indexOf('កីឡា') !== -1 || s.indexOf('sport') !== -1 || s.indexOf('pe') !== -1 || s.indexOf('physical') !== -1) return '#FECDD3';
    if (s.indexOf('សេដ្ឋកិច្ច') !== -1 || s.indexOf('econ') !== -1) return '#FEF3C7';
    if (s.indexOf('ភាសា') !== -1 || s.indexOf('social') !== -1) return '#E9D5FF';

    if (rawColor && rawColor !== '#E5E7EB' && rawColor !== '#e5e7eb' && rawColor !== '#ffffff' && rawColor !== '#fff' && rawColor !== 'transparent') {
      return rawColor;
    }
    return '#FED766';
  }

  var DAY_EN = {
    'ច័ន្ទ': 'Monday',
    'អង្គារ': 'Tuesday',
    'ពុធ': 'Wednesday',
    'ព្រហស្បតិ៍': 'Thursday',
    'សុក្រ': 'Friday',
    'សៅរ៍': 'Saturday'
  };
  var DAY_SHORT_EN = {
    'ច័ន្ទ': 'Mon',
    'អង្គារ': 'Tue',
    'ពុធ': 'Wed',
    'ព្រហស្បតិ៍': 'Thu',
    'សុក្រ': 'Fri',
    'សៅរ៍': 'Sat'
  };
  var SHIFT_EN = {
    'ព្រឹក': 'Morning',
    'រសៀល': 'Afternoon'
  };
  var TEACHER_EN_NAMES = {
    'សុខ ដារ៉ា': 'Sok Dara',
    'សុខ ដារ៉ា (Updated)': 'Sok Dara',
    'សុខ ដារ៉ា (Updated Name)': 'Sok Dara',
    'តាន់ ធីតា': 'Tan Thida',
    'ហេង វីរៈ': 'Heng Virak',
    'ជើន ម៉ារី': 'Cheun Mary',
    'ណុង សុធា': 'Nong Sothea',
    'យ៉ុក សុីន': 'Yok Sin',
    'ប៉ុក សុភី': 'Pok Sophy',
    'អ៊ុក ចាន់ថា': 'Ouk Chantha',
    'លី សុភាព': 'Ly Sopheap',
    'ម៉ៅ ដារ៉ាវី': 'Mao Daravy',
    'គឹម ស្រីពេជ្រ': 'Kim Sreypich',
    'ចាន់ សុខលី': 'Chan Sokhly',
    'ប្រាក់ មុនី': 'Prak Mony',
    'អ៊ឹង រិទ្ធី': 'Oeng Rithy',
    'ស៊ុន ច័ន្ទណ៍': 'Sun Chan',
    'ទូច សុភក្ត្រា': 'Touch Sopheaktra',
    'វ៉ាន់ សុភ័ក្ត្រ': 'Van Sopheak',
    'រស់ សុគន្ធា': 'Ros Sokunthea',
    'ខូវ ចាន់ដារ៉ា': 'Khov Chandara',
    'ឈឹម ស្រីល័ក្ខ': 'Chhim Sreyleak',
    'នូ សុខហេង': 'Nou Sokheng',
    'គង់ សុភាវី': 'Kong Sopheavy',
    'ឡុង ចាន់ថុល': 'Long Chanthol',
    'ប៉ែន សុភាវី': 'Pen Sopheavy',
    'អន សុខរិទ្ធ': 'Orn Sokrith',
    'សេង ដារ៉ាវុធ': 'Seng Daravuth',
    'ហ៊ុន មាលី': 'Hun Maly',
    'ជា សុភីរិទ្ធ': 'Chea Sophearith',
    'ផន ចាន់សុភា': 'Phorn Chansophea',
    'ប៊ុន ស្រីមុំ': 'Bun Sreymom',
    'វង្ស សុខាន់': 'Vong Sokhan',
    'តេង សុភ័ក្ត្រ': 'Teng Sopheaktra',
    'គ្រូថ្មី ពិសិដ្ឋ': 'Piseth New'
  };

  var SUBJECT_EN_NAMES = {
    'sub_K': 'Khmer Literature',
    'sub_M': 'Mathematics',
    'sub_EN': 'English',
    'sub_P': 'Physics',
    'sub_C': 'Chemistry',
    'sub_B': 'Biology',
    'sub_ES': 'Earth Science',
    'sub_G': 'Computer Studies',
    'sub_H': 'History',
    'sub_I': 'Moral & Civics',
    'sub_IT': 'Physical Education',
    'sub_ED': 'Economics',
    'sub_SH': 'Social Language',
    'K': 'Khmer Literature',
    'M': 'Mathematics',
    'EN': 'English',
    'P': 'Physics',
    'C': 'Chemistry',
    'B': 'Biology',
    'ES': 'Earth Science',
    'G': 'Computer Studies',
    'H': 'History',
    'I': 'Moral & Civics',
    'IT': 'Physical Education',
    'ED': 'Economics',
    'SH': 'Social Language',
    'ភាសាខ្មែរ': 'Khmer Literature',
    'គណិតវិទ្យា': 'Mathematics',
    'ភាសាអង់គ្លេស': 'English',
    'រូបវិទ្យា': 'Physics',
    'គីមីវិទ្យា': 'Chemistry',
    'ជីវវិទ្យា': 'Biology',
    'ផែនដីវិទ្យា': 'Earth Science',
    'វិទ្យាសាស្ត្រកុំព្យូទ័រ': 'Computer Studies',
    'កុំព្យូទ័រ': 'Computer Studies',
    'ប្រវត្តិវិទ្យា': 'History',
    'សីលធម៌-ពលរដ្ឋ': 'Moral & Civics',
    'អប់រំកាយ និងកីឡា': 'Physical Education',
    'សេដ្ឋកិច្ច': 'Economics',
    'ភាសាសង្គម': 'Social Language',
    'ភូមិវិទ្យា': 'Geography',
    'ខ្មែរ': 'Khmer',
    'គណិត': 'Math',
    'អង់គ្លេស': 'English',
    'រូប': 'Physics',
    'គីមី': 'Chemistry',
    'ជីវ': 'Biology',
    'ផែនដី': 'Earth Sci',
    'ប្រវត្តិ': 'History',
    'សីលធម៌': 'Civics',
    'កីឡា': 'PE',
    'សេដ្ឋ': 'Econ',
    'ពលរដ្ឋ': 'Moral & Civics',
    'ពល': 'Civics',
    'ទូទៅ': 'General Studies'
  };

  var POSITION_EN = {
    'គ្រូបង្រៀន': 'Teacher',
    'នាយក': 'Principal',
    'នាយករង': 'Vice Principal',
    'ប្រធានដេប៉ាតឺម៉ង់': 'Department Head',
    'គ្រូបន្ទុកថ្នាក់': 'Homeroom Teacher'
  };
  var CATEGORY_EN = {
    'ក្របខ័ណ្ឌរដ្ឋ': 'State Framework / Civil Servant',
    'កិច្ចសន្យា': 'Contract Teacher',
    'ពេញម៉ោង': 'Full-time',
    'ក្រៅម៉ោង': 'Part-time'
  };
  var RANK_EN = {
    'គ្រូកម្រិតឧត្តម': 'Senior Teacher',
    'គ្រូមូលដ្ឋាន': 'Junior Teacher',
    'គ្រូបឋម': 'Primary Teacher'
  };

  function toEnDay(d, short) {
    if (short) return DAY_SHORT_EN[d] || d;
    return DAY_EN[d] || d;
  }

  function toEnShift(s) {
    return SHIFT_EN[s] || s;
  }

  function toEnTeacher(t) {
    if (!t) return '';
    if (typeof t === 'string') return TEACHER_EN_NAMES[t] || t;
    return t.name_en || TEACHER_EN_NAMES[t.name_kh] || t.name_kh || t.id;
  }

  function toEnSubject(s) {
    if (!s) return '';
    if (typeof s === 'string') {
      var trimmed = s.trim();
      if (SUBJECT_EN_NAMES[trimmed]) return SUBJECT_EN_NAMES[trimmed];
      for (var k in SUBJECT_EN_NAMES) {
        if (k.length >= 2 && trimmed.indexOf(k) !== -1) return SUBJECT_EN_NAMES[k];
      }
      return trimmed;
    }
    return s.name_en || SUBJECT_EN_NAMES[s.name_kh] || SUBJECT_EN_NAMES[s.code] || SUBJECT_EN_NAMES[s.id] || s.name_kh || s.code;
  }

  function toEnRoom(r) {
    if (!r) return 'Room 101';
    var clean = String(r).replace(/បន្ទប់[់]*\s*[:ៈ]*/g, '').replace(/^Room\s*/i, '').trim();
    return clean ? ('Room ' + clean) : 'Room 101';
  }

  function toEnClass(c) {
    if (!c) return '';
    var raw = typeof c === 'string' ? c : (c.display || c.id || '');
    return String(raw).replace(/^class_/, '').replace(/^ថ្នាក់\s*/, '').trim();
  }

  function toEnPosition(p) {
    if (!p) return 'Teacher';
    return POSITION_EN[p] || p;
  }

  function toEnCategory(c) {
    if (!c) return 'State Framework';
    return CATEGORY_EN[c] || c;
  }

  function toEnRank(r) {
    if (!r) return 'Senior Teacher';
    return RANK_EN[r] || r;
  }

  function toEnGender(g) {
    if (g === 'ស្រី' || g === 'Female' || g === 'F') return 'Female';
    return 'Male';
  }

  var SUBJECT_COLOR_PALETTE = {
    'K':    '#FED766', // Khmer (Warm Amber Yellow)
    'M':    '#93C5FD', // Mathematics (Soft Sky Blue)
    'EN':   '#99F6E4', // English (Mint Teal)
    'P':    '#DDD6FE', // Physics (Lavender Violet)
    'C':    '#FBCFE8', // Chemistry (Soft Rose Pink)
    'B':    '#A7F3D0', // Biology (Light Emerald Green)
    'ES':   '#FED7AA', // Earth Science / Geography (Warm Peach)
    'GEO':  '#FED7AA',
    'G':    '#BAE6FD', // Computer Studies / ICT (Ice Blue)
    'H':    '#FDE68A', // History (Warm Apricot)
    'I':    '#C7D2FE', // Civics / Moral (Periwinkle Indigo)
    'IT':   '#FECDD3', // Physical Education / Sports (Coral Pink)
    'PE':   '#FECDD3',
    'ED':   '#FEF3C7', // Moral Education / Economics (Creamy Sage)
    'ECO':  '#FEF3C7',
    'SH':   '#E9D5FF'  // Social Language (Soft Lilac Purple)
  };

  function getSubjectColor(subjectId, subName, rawColor) {
    var sId = String(subjectId || '').trim();
    var code = sId.replace(/^sub_/, '').toUpperCase();
    if (SUBJECT_COLOR_PALETTE[code]) return SUBJECT_COLOR_PALETTE[code];
    if (SUBJECT_COLOR_PALETTE[sId]) return SUBJECT_COLOR_PALETTE[sId];

    var s = String(subName || '').toLowerCase();
    if (s.indexOf('ខ្មែរ') !== -1 || s.indexOf('khmer') !== -1) return '#FED766';
    if (s.indexOf('គណិត') !== -1 || s.indexOf('math') !== -1) return '#93C5FD';
    if (s.indexOf('អង់គ្លេស') !== -1 || s.indexOf('english') !== -1 || s.indexOf('eng') !== -1) return '#99F6E4';
    if (s.indexOf('រូប') !== -1 || s.indexOf('physic') !== -1) return '#DDD6FE';
    if (s.indexOf('គីមី') !== -1 || s.indexOf('chem') !== -1) return '#FBCFE8';
    if (s.indexOf('ជីវ') !== -1 || s.indexOf('bio') !== -1) return '#A7F3D0';
    if (s.indexOf('ភូមិ') !== -1 || s.indexOf('ផែនដី') !== -1 || s.indexOf('geo') !== -1 || s.indexOf('earth') !== -1) return '#FED7AA';
    if (s.indexOf('កុំព្យូទ័រ') !== -1 || s.indexOf('ព័ត៌មាន') !== -1 || s.indexOf('ict') !== -1 || s.indexOf('computer') !== -1) return '#BAE6FD';
    if (s.indexOf('ប្រវត្តិ') !== -1 || s.indexOf('histor') !== -1) return '#FDE68A';
    if (s.indexOf('ពលរដ្ឋ') !== -1 || s.indexOf('សីលធម៌') !== -1 || s.indexOf('civic') !== -1 || s.indexOf('moral') !== -1) return '#C7D2FE';
    if (s.indexOf('កីឡា') !== -1 || s.indexOf('sport') !== -1 || s.indexOf('pe') !== -1 || s.indexOf('physical') !== -1) return '#FECDD3';
    if (s.indexOf('សេដ្ឋកិច្ច') !== -1 || s.indexOf('econ') !== -1) return '#FEF3C7';
    if (s.indexOf('ភាសា') !== -1 || s.indexOf('social') !== -1) return '#E9D5FF';

    if (rawColor && rawColor !== '#E5E7EB' && rawColor !== '#e5e7eb' && rawColor !== '#ffffff' && rawColor !== '#fff' && rawColor !== 'transparent') {
      return rawColor;
    }
    return '#FED766';
  }

  function gridKey(day, shift, period, classId) {
    return day + '|' + shift + '|' + period + '|' + classId;
  }

  function parseGridKey(key) {
    var p = String(key).split('|');
    return { day: p[0], shift: p[1], period: parseInt(p[2], 10), class_id: p[3] };
  }

  function buildPeriods() {
    var out = [];
    [['ព្រឹក', MORNING_STARTS], ['រសៀល', AFTERNOON_STARTS]].forEach(function (pair) {
      pair[1].forEach(function (start, i) {
        var hm = start.split(':').map(Number);
        var total = hm[0] * 60 + hm[1] + 50;
        var end = ('0' + Math.floor(total / 60)).slice(-2) + ':' + ('0' + (total % 60)).slice(-2);
        out.push({ number: i + 1, shift: pair[0], start: start, end: end, label: pair[0] + ' ' + (i + 1) });
      });
    });
    return out;
  }

  function nowISO() { return new Date().toISOString().replace(/\.\d+Z$/, '+00:00'); }

  /** Mirror of timetable_models.build_seed_state() — used when the API is offline. */
  function buildSeedState() {
    var subjects = SUBJECT_DEFS.map(function (d) {
      return {
        id: 'sub_' + d[0], name_kh: d[1], name_en: d[2], short_name: d[3],
        code: d[0], color: d[4], lessons_per_week: d[5], is_locked: false
      };
    });
    var classes = [];
    for (var g = 7; g <= 12; g++) {
      ['A', 'B'].forEach(function (sec) {
        classes.push({
          id: 'class_' + g + sec, grade: g, section: sec, display: g + sec,
          shift: sec === 'A' ? 'ព្រឹក' : 'រសៀល', days: 6, capacity: 60
        });
      });
    }
    var teachers = [], nameIndex = 0;
    SUBJECT_DEFS.forEach(function (d) {
      var code = d[0], lessons = d[5];
      if (!lessons) return;
      var demand = lessons * 12;
      var target = (code === 'K' || code === 'M' || code === 'EN') ? 17 : 15;
      var perTeacher = Math.floor(target / lessons) * lessons || target;
      var count = Math.max(1, Math.ceil(demand / perTeacher));
      for (var i = 1; i <= count; i++) {
        var morningOnly = i === count && ['ES', 'G', 'H', 'IT', 'ED'].indexOf(code) !== -1;
        teachers.push({
          id: 't_' + code + i, code: code + i,
          name_kh: TEACHER_NAMES[nameIndex++ % TEACHER_NAMES.length], name_en: '',
          subject_id: 'sub_' + code, target: target,
          shifts: morningOnly ? ['ព្រឹក'] : SHIFTS.slice()
        });
      }
    });
    var bySubject = {}, load = {};
    teachers.forEach(function (t) {
      (bySubject[t.subject_id] = bySubject[t.subject_id] || []).push(t);
      load[t.id] = 0;
    });
    var assignments = [];
    classes.forEach(function (cls) {
      Object.keys(CURRICULUM).forEach(function (code) {
        var lessons = CURRICULUM[code];
        if (lessons <= 0) return;
        var subjectId = 'sub_' + code;
        var pool = bySubject[subjectId] || [];
        if (!pool.length) return;
        var feasible = pool.filter(function (t) { return load[t.id] + lessons <= t.target; });
        var chosen = (feasible.length ? feasible : pool).slice().sort(function (a, b) {
          return load[a.id] - load[b.id] || a.code.localeCompare(b.code);
        })[0];
        load[chosen.id] += lessons;
        assignments.push({
          id: 'asg_' + cls.id + '_' + code, class_id: cls.id, subject_id: subjectId,
          teacher_id: chosen.id, lessons: lessons, shift: cls.shift
        });
      });
    });
    var records = TEACHER_NAMES.slice(0, 12).map(function (name, idx) {
      var i = idx + 1;
      return {
        no: i, name: name, gender: i % 2 ? 'ស' : 'ប',
        dob: '១៩៨' + (5 + i % 4) + '·០' + (i % 9 + 1) + '·១២', grade: '១០',
        code: 'ST' + (2000 + i), birth_place: 'ភ្នំពេញ', address: 'រាជធានីភ្នំពេញ',
        language: 'ខ្មែរ', id_number: '០០' + ('000' + i).slice(-4),
        registered_at: '២០២៦·០៩·០១',
        homeroom: TEACHER_NAMES[(i + 3) % TEACHER_NAMES.length],
        type: i % 3 === 0 ? 'គ្រូបង្រៀង' : 'សិស្ស'
      };
    });
    var periods = buildPeriods();
    return {
      schema_version: 4,
      institution: {
        name_kh: 'វិទ្យាល័យ ហ្គេតវ៉េ អន្តរជាតិថ្មី', name_en: 'New Gateway International School',
        academic_year: 'ឆ្នាំសិក្សា ២០២៦–២០២៧', package: 'ស្តង់ដារ'
      },
      settings: { days: DAYS.slice(), shifts: SHIFTS.slice(), periods: periods, khmer_numerals: true, auto_save: true },
      subjects: subjects, teachers: teachers, classes: classes,
      assignments: assignments, grid: {}, records: records,
      history: [], revision: 1, updated_at: nowISO()
    };
  }

  /* ── Minimal OOXML writer (works offline, no libraries) ───────────────── */

  function esc(s) {
    return String(s == null ? '' : s)
      .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;').replace(/[\x00-\x08\x0B\x0C\x0E-\x1F]/g, '');
  }

  function colName(n) {
    var s = '';
    while (n > 0) { var r = (n - 1) % 26; s = String.fromCharCode(65 + r) + s; n = Math.floor((n - 1) / 26); }
    return s;
  }

  var CRC_TABLE = (function () {
    var t = new Uint32Array(256);
    for (var n = 0; n < 256; n++) {
      var c = n;
      for (var k = 0; k < 8; k++) c = (c & 1) ? (0xEDB88320 ^ (c >>> 1)) : (c >>> 1);
      t[n] = c >>> 0;
    }
    return t;
  })();

  function crc32(bytes) {
    var c = 0xFFFFFFFF;
    for (var i = 0; i < bytes.length; i++) c = CRC_TABLE[(c ^ bytes[i]) & 0xFF] ^ (c >>> 8);
    return (c ^ 0xFFFFFFFF) >>> 0;
  }

  function zipFiles(files) {
    var enc = new TextEncoder();
    var parts = [], central = [], offset = 0;
    files.forEach(function (f) {
      var name = enc.encode(f.name);
      var data = typeof f.data === 'string' ? enc.encode(f.data) : f.data;
      var crc = crc32(data);
      var local = new Uint8Array(30 + name.length);
      var dv = new DataView(local.buffer);
      dv.setUint32(0, 0x04034b50, true); dv.setUint16(4, 20, true);
      dv.setUint16(6, 0x0800, true);     dv.setUint16(8, 0, true);
      dv.setUint16(10, 0, true);         dv.setUint16(12, 0x21, true);
      dv.setUint32(14, crc, true);       dv.setUint32(18, data.length, true);
      dv.setUint32(22, data.length, true);
      dv.setUint16(26, name.length, true); dv.setUint16(28, 0, true);
      local.set(name, 30);
      parts.push(local, data);
      var cd = new Uint8Array(46 + name.length);
      var cv = new DataView(cd.buffer);
      cv.setUint32(0, 0x02014b50, true); cv.setUint16(4, 20, true);
      cv.setUint16(6, 20, true); cv.setUint16(8, 0x0800, true);
      cv.setUint16(10, 0, true); cv.setUint16(12, 0, true);
      cv.setUint16(14, 0x21, true); cv.setUint32(16, crc, true);
      cv.setUint32(20, data.length, true); cv.setUint32(24, data.length, true);
      cv.setUint16(28, name.length, true); cv.setUint16(30, 0, true);
      cv.setUint16(32, 0, true); cv.setUint16(34, 0, true);
      cv.setUint16(36, 0, true); cv.setUint32(38, 0, true);
      cv.setUint32(42, offset, true);
      cd.set(name, 46);
      central.push(cd);
      offset += local.length + data.length;
    });
    var cdSize = central.reduce(function (a, b) { return a + b.length; }, 0);
    var eocd = new Uint8Array(22);
    var ev = new DataView(eocd.buffer);
    ev.setUint32(0, 0x06054b50, true); ev.setUint16(4, 0, true);
    ev.setUint16(6, 0, true); ev.setUint16(8, files.length, true);
    ev.setUint16(10, files.length, true);
    ev.setUint32(12, cdSize, true); ev.setUint32(16, offset, true);
    ev.setUint16(20, 0, true);
    var all = parts.concat(central, [eocd]);
    var total = all.reduce(function (a, b) { return a + b.length; }, 0);
    var out = new Uint8Array(total), pos = 0;
    all.forEach(function (p) { out.set(p, pos); pos += p.length; });
    return out;
  }

  function rgb(color) {
    if (!color) return 'FFFFFFFF';
    var h = String(color).replace('#', '').toUpperCase();
    return /^[0-9A-F]{6}$/.test(h) ? 'FF' + h : (/^[0-9A-F]{8}$/.test(h) ? h : 'FFFFFFFF');
  }

  /**
   * sheets: [{ name, cols:[widths], freeze:n, merges:['A1:G1'],
   *            rows:[[ {v, fill, bold, color, align, span} ]] }]
   * Returns a Blob.  Colours accept #RRGGBB (subject palette).
   */
  function makeXlsx(sheets) {
    var fonts = [{ size: 11, bold: false, color: 'FF1F2937' }];
    var fills = [null];
    var styles = [], styleKeys = {};

    function style(o) {
      o = o || {};
      var key = [o.fill || '', !!o.bold, o.color || 'FF1F2937', o.align || 'center', o.size || 11].join('|');
      if (styleKeys[key] !== undefined) return styleKeys[key];
      var fontIdx = 0;
      if (o.bold || o.color || (o.size && o.size !== 11)) {
        fonts.push({ size: o.size || 11, bold: !!o.bold, color: o.color || 'FF1F2937' });
        fontIdx = fonts.length - 1;
      }
      var fillIdx = 0;
      if (o.fill) { fills.push(rgb(o.fill)); fillIdx = fills.length - 1; }
      var id = styles.length;
      styles.push({ font: fontIdx, fill: fillIdx, align: o.align || 'center' });
      styleKeys[key] = id;
      return id;
    }

    var sheetXml = sheets.map(function (sh) {
      var body = [], merges = [], heights = [];
      sh.rows.forEach(function (row, ri) {
        var cells = [], r = ri + 1;
        row.forEach(function (c, ci) {
          if (c == null) c = {};
          if (typeof c !== 'object') c = { v: c };
          var sid = style(c);
          var ref = colName(ci + 1) + r;
          var val = c.v == null ? '' : String(c.v);
          var isNum = typeof c.v === 'number';
          cells.push('<c r="' + ref + '" s="' + sid + '"' +
            (isNum ? '' : ' t="inlineStr"') + '>' +
            (val === '' ? '' : (isNum ? '<v>' + c.v + '</v>' : '<is><t xml:space="preserve">' + esc(val) + '</t></is>')) +
            '</c>');
          if (c.span > 1) merges.push(ref + ':' + colName(ci + c.span) + r);
        });
        body.push('<row r="' + r + '"' + (sh.rowHeights && sh.rowHeights[ri] ? ' ht="' + sh.rowHeights[ri] + '" customHeight="1"' : '') + '>' + cells.join('') + '</row>');
      });
      var cols = (sh.cols || []).map(function (w, i) {
        return '<col min="' + (i + 1) + '" max="' + (i + 1) + '" width="' + w + '" customWidth="1"/>';
      }).join('');
      var pane = sh.freeze ? '<pane ySplit="' + sh.freeze + '" topLeftCell="A' + (sh.freeze + 1) + '" activePane="bottomLeft" state="frozen"/>' : '';
      var mergeXml = merges.length ? '<mergeCells count="' + merges.length + '">' +
        merges.map(function (m) { return '<mergeCell ref="' + m + '"/>'; }).join('') + '</mergeCells>' : '';
      var maxCol = Math.max.apply(null, sh.rows.map(function (r) { return r.length; }).concat([1]));
      return '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>' +
        '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">' +
        '<dimension ref="A1:' + colName(maxCol) + Math.max(1, sh.rows.length) + '"/>' +
        '<sheetViews><sheetView workbookViewId="0" showGridLines="0">' + pane + '</sheetView></sheetViews>' +
        '<sheetFormatPr defaultRowHeight="18"/>' + (cols ? '<cols>' + cols + '</cols>' : '') +
        '<sheetData>' + body.join('') + '</sheetData>' + mergeXml +
        '<pageMargins left="0.3" right="0.3" top="0.5" bottom="0.5" header="0.2" footer="0.2"/>' +
        '<pageSetup paperSize="' + (sh.paper === 'A3' ? 8 : 9) + '" orientation="' + (sh.landscape ? 'landscape' : 'portrait') + '" fitToWidth="1" fitToHeight="0"/>' +
        '</worksheet>';
    });

    var fontXml = fonts.map(function (f) {
      return '<font><sz val="' + f.size + '"/><color rgb="' + f.color + '"/><name val="Noto Sans Khmer"/><family val="2"/>' + (f.bold ? '<b/>' : '') + '</font>';
    }).join('');
    var fillXml = fills.map(function (f) {
      return f ? '<fill><patternFill patternType="solid"><fgColor rgb="' + f + '"/><bgColor indexed="64"/></patternFill></fill>'
               : '<fill><patternFill patternType="none"/></fill>';
    }).join('');
    var borderXml = '<border><left style="thin"><color rgb="FFD8DEE9"/></left><right style="thin"><color rgb="FFD8DEE9"/></right><top style="thin"><color rgb="FFD8DEE9"/></top><bottom style="thin"><color rgb="FFD8DEE9"/></bottom><diagonal/></border>';
    var xfs = styles.map(function (s) {
      return '<xf numFmtId="0" fontId="' + s.font + '" fillId="' + s.fill + '" borderId="0" xfId="0" applyFont="1" applyFill="' + (s.fill ? 1 : 0) + '" applyAlignment="1"><alignment horizontal="' + s.align + '" vertical="center" wrapText="1"/></xf>';
    }).join('');
    var stylesXml = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>' +
      '<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">' +
      '<fonts count="' + fonts.length + '">' + fontXml + '</fonts>' +
      '<fills count="' + fills.length + '">' + fillXml + '</fills>' +
      '<borders count="1">' + borderXml + '</borders>' +
      '<cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs>' +
      '<cellXfs count="' + styles.length + '">' + xfs + '</cellXfs>' +
      '<cellStyles count="1"><cellStyle name="Normal" xfId="0" builtinId="0"/></cellStyles></styleSheet>';

    var sheetTags = sheets.map(function (s, i) {
      return '<sheet name="' + esc(s.name.slice(0, 31)) + '" sheetId="' + (i + 1) + '" r:id="rId' + (i + 1) + '"/>';
    }).join('');
    var relTags = sheets.map(function (s, i) {
      return '<Relationship Id="rId' + (i + 1) + '" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet' + (i + 1) + '.xml"/>';
    }).join('') + '<Relationship Id="rId' + (sheets.length + 1) + '" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>';
    var overrides = sheets.map(function (s, i) {
      return '<Override PartName="/xl/worksheets/sheet' + (i + 1) + '.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>';
    }).join('');

    var files = [
      { name: '[Content_Types].xml', data: '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/><Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>' + overrides + '</Types>' },
      { name: '_rels/.rels', data: '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/></Relationships>' },
      { name: 'xl/workbook.xml', data: '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><sheets>' + sheetTags + '</sheets></workbook>' },
      { name: 'xl/_rels/workbook.xml.rels', data: '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">' + relTags + '</Relationships>' },
      { name: 'xl/styles.xml', data: stylesXml }
    ];
    sheetXml.forEach(function (xml, i) {
      files.push({ name: 'xl/worksheets/sheet' + (i + 1) + '.xml', data: xml });
    });
    return new Blob([zipFiles(files)], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' });
  }

  function downloadXlsx(filename, sheets) {
    var blob = makeXlsx(sheets);
    var url = URL.createObjectURL(blob);
    var a = document.createElement('a');
    a.href = url; a.download = filename;
    document.body.appendChild(a); a.click();
    setTimeout(function () { URL.revokeObjectURL(url); a.remove(); }, 1500);
  }

  global.KSData = {
    DAYS: DAYS, SHIFTS: SHIFTS, SUBJECT_DEFS: SUBJECT_DEFS,
    TEACHER_NAMES: TEACHER_NAMES, CURRICULUM: CURRICULUM,
    RECORD_COLUMNS: RECORD_COLUMNS, TEACHER_SPREADSHEET_COLUMNS: TEACHER_SPREADSHEET_COLUMNS,
    CLASS_CAPACITY: 60,
    DAY_EN: DAY_EN, DAY_SHORT_EN: DAY_SHORT_EN, SHIFT_EN: SHIFT_EN,
    TEACHER_EN_NAMES: TEACHER_EN_NAMES, SUBJECT_EN_NAMES: SUBJECT_EN_NAMES,
    toEnDay: toEnDay, toEnShift: toEnShift, toEnTeacher: toEnTeacher,
    toEnSubject: toEnSubject, toEnRoom: toEnRoom, toEnClass: toEnClass,
    toEnPosition: toEnPosition, toEnCategory: toEnCategory, toEnRank: toEnRank, toEnGender: toEnGender,
    DAY_EN: DAY_EN, DAY_SHORT_EN: DAY_SHORT_EN, SHIFT_EN: SHIFT_EN,
    TEACHER_EN_NAMES: TEACHER_EN_NAMES, SUBJECT_EN_NAMES: SUBJECT_EN_NAMES,
    toEnDay: toEnDay, toEnShift: toEnShift, toEnTeacher: toEnTeacher,
    toEnSubject: toEnSubject, toEnRoom: toEnRoom, toEnClass: toEnClass,
    toEnPosition: toEnPosition, toEnCategory: toEnCategory, toEnRank: toEnRank, toEnGender: toEnGender,
    kh: kh, gridKey: gridKey, parseGridKey: parseGridKey,
    buildPeriods: buildPeriods, buildSeedState: buildSeedState,
    makeXlsx: makeXlsx, downloadXlsx: downloadXlsx, nowISO: nowISO,
    parseClipboardTable: parseClipboardTable, formatClipboardTable: formatClipboardTable,
    getSubjectColor: getSubjectColor, SUBJECT_COLOR_PALETTE: SUBJECT_COLOR_PALETTE
  };
})(window);

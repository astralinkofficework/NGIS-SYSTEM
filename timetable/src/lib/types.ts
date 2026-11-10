export type Shift = "AM" | "PM";
export type DayKey = "Mon" | "Tue" | "Wed" | "Thu" | "Fri" | "Sat";
export type ClassShift = "ព្រឹក" | "ពេញថ្ងៃ";

export interface Slot {
  day: DayKey;
  shift: Shift;
  period: number;
  time: string;
  key(): string;
}

export interface TimetableCell {
  subject?: string;
  teacher?: string;
  klass?: string;
  codes?: string[];
  locked?: boolean;
  raw?: string;
}

export interface TimetableRow {
  label: string;
  shift: Shift;
  period: number;
  time: string;
  day: DayKey;
  cells: Record<DayKey, TimetableCell>;
}

export interface TimetableGrid {
  class: string;
  term: number;
  rows: TimetableRow[];
}

export interface ClassInfo {
  id: string;
  name: string;
  grade: string;
  shift: ClassShift;
  placed: number;
  total: number;
  hoursPerWeek: number;
  homeroomTeacher: string;
}

export interface TeacherInfo {
  name: string;
  code: string;
  subject: string;
  hoursPerWeek: number;
  contracted: number;
  overtime: number;
  teachingDays: number;
  absencePerWeek: number;
  missingHours: number;
  classes: string[];
}

export interface ProblemItem {
  class: string;
  subject: string;
  missingHours: number;
  teacher?: string;
  code?: string;
}

export interface UnplacedItem extends ProblemItem {}

export interface Fix {
  n: number;
  text: string;
  action: string;
}

export interface WhyUnplaced {
  class: string;
  subject: string;
  totalHours: number;
  placed: number;
  missing: number;
  teacher?: string;
  code?: string;
  causes: string[];
  fixes: Fix[];
}

export interface WhereCanPlace {
  class: string;
  subject: string;
  freeSlots: Slot[];
  blocked: string[];
  note?: string;
}

export interface Proposal {
  id: string;
  status: "PENDING" | "APPROVED" | "REJECTED";
  reason: string;
  changes: any[];
  createdAt?: string;
}

export const DAYS: DayKey[] = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
export const DAY_LABELS_KM: Record<DayKey, string> = {
  Mon: "ចន្ទ", Tue: "អង្គារ", Wed: "ពុធ", Thu: "ព្រហស្បតិ៍", Fri: "សុក្រ", Sat: "សៅរ៍",
};
export const SHIFTS: Shift[] = ["AM", "PM"];
export const SHIFT_LABELS_KM: Record<Shift, string> = { AM: "ព្រឹឞ", PM: "រសៀល" };
export const SHIFT_LABELS_KM_LONG: Record<Shift, string> = { AM: "ព្រឹឞ (ក្រោយលើករហូតិ)", PM: "រសៀល" };
export const PERIODS = [1, 2, 3, 4, 5];
export const PERIOD_TIMES: Record<Shift, Record<number, string>> = {
  AM: { 1: "07:00–07:50", 2: "07:50–08:40", 3: "08:40–09:30", 4: "09:30–10:20", 5: "10:20–11:10" },
  PM: { 1: "13:00–13:50", 2: "13:50–14:40", 3: "14:40–15:30", 4: "15:30–16:20", 5: "16:20–17:10" },
};
export const PERIOD_LABELS_KM: Record<number, string> = { 1: "ម៉ោងទី1", 2: "ម៉ោងទី2", 3: "ម៉ោងទី3", 4: "ម៉ោងទី4", 5: "ម៉ោងទី5" };

export function slotKey(day: DayKey, shift: Shift, period: number): string {
  return `${day}|${shift}|${period}`;
}

export function subjectDiscipline(subject: string): "khmer" | "math" | "science" | "english" | "sports" | "social" | "default" {
  const s = (subject || "").toLowerCase();
  if (s.includes("ភាសាខ្មែរ") || s.includes("khmer")) return "khmer";
  if (s.includes("គណិតវិទ្យា") || s.includes("math")) return "math";
  if (s.includes("រូបវិទ្យា") || s.includes("គីមីវិទ្យា") || s.includes("ជីវវិទ្យា") || s.includes("ផែនដី") || s.includes("science") || s.includes("phys") || s.includes("chem") || s.includes("bio")) return "science";
  if (s.includes("អង់គ្លេស") || s.includes("english")) return "english";
  if (s.includes("កីឡា") || s.includes("sport")) return "sports";
  if (s.includes("ភូមិវិទ្យា") || s.includes("ប្រវត្តិវិទ្យា") || s.includes("ពលរដ្ឋ") || s.includes("social") || s.includes("geog") || s.includes("hist") || s.includes("civic")) return "social";
  if (s.includes("កសិកម្ម") || s.includes("បរិស្ថាន") || s.includes("សុខភាពសិក្សា") || s.includes("កុំព្យូទ័រ") || s.includes("it")) return "default";
  return "default";
}

export function honorific(name: string): string {
  return `គ្រូ ${name}`;
}

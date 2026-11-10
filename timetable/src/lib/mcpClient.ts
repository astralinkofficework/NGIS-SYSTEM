import { ClassInfo, TeacherInfo, TimetableGrid, TimetableCell, ProblemItem, WhyUnplaced, UnplacedItem, WhereCanPlace, Slot, Fix } from "@/lib/types";

const MCP_URL =
  process.env.NEXT_PUBLIC_MCP_URL ||
  "http://127.0.0.1:3480/mcp/VrW5q_4p8xqZNesWLPaymvH2iX-bL1NB";

export class MCPError extends Error {
  code?: number;
  data?: unknown;
  constructor(message: string, code?: number, data?: unknown) {
    super(message);
    this.name = "MCPError";
    this.code = code;
    this.data = data;
  }
}

async function mcpFetch(method: string, params: Record<string, unknown> = {}): Promise<any> {
  const res = await fetch("/api/mcp", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ jsonrpc: "2.0", id: String(Date.now()), method, params }),
  });
  if (!res.ok) {
    throw new MCPError(`MCP transport error: HTTP ${res.status}`, res.status);
  }
  const json = await res.json();
  if (json.error) {
    throw new MCPError(json.error.message || "MCP error", json.error.code, json.error.data);
  }
  return json.result;
}

function textOf(result: any): string {
  return Array.isArray(result?.content)
    ? result.content
        .map((c: any) => (c.type === "text" ? c.text : String(c)))
        .join("\n")
    : result == null
      ? ""
      : typeof result === "string"
        ? result
        : JSON.stringify(result);
}

/* ---------------- markdown table parsing ---------------- */

function splitTableCells(line: string): string[] {
  return line
    .split("|")
    .map((c) => c.trim())
    .filter((_, i) => i > 0 && i < line.split("|").length - 1);
}

function parseMarkdownTable(text: string): string[][] {
  const lines = text.split("\n").map((l) => l.trim()).filter(Boolean);
  const rows: string[][] = [];
  for (const line of lines) {
    if (!line.startsWith("|")) continue;
    if (/^|\s*-+\s*(\|-*\s*)+$/.test(line)) continue;
    rows.push(splitTableCells(line));
  }
  return rows;
}

function dayKey(day: string): string | null {
  const map: Record<string, string> = {
    ចន្ទ: "Mon", អង្គារ: "Tue", ពុធ: "Wed", ព្រហស្បតិ៍: "Thu",
    សុក្រ: "Fri", សៅរ៍: "Sat",
  };
  return map[day] ?? null;
}

function shiftKey(shift: string): "AM" | "PM" | null {
  if (shift === "ព្រឹក") return "AM";
  if (shift === "រសៀល") return "PM";
  return null;
}

function parseSlotLabel(label: string): { day: string; shift: "AM" | "PM"; period: number; time: string } | null {
  const m = label.match(/^(ព្រឹក|រសៀល)\s+ម៉ោងទី(\d+)\s*\((\d{2}:\d{2}\u2013\d{2}:\d{2})\)$/);
  if (!m) return null;
  return { shift: shiftKey(m[1])!, period: Number(m[2]), time: m[3], day: "" };
}

function parseCell(text: string, mode: "class" | "teacher" = "class"): TimetableCell {
  const t = text.trim();
  if (t === "—" || t === "-") return {};
  const codeM = t.match(/\(([^)]+)\)\s*$/);
  let codes: string[] = [];
  let body = t;
  if (codeM) {
    codes = codeM[1].split(",").map((c) => c.trim()).filter(Boolean);
    body = t.slice(0, codeM.index).trim();
  }
  const parts = body.split("·").map((p) => p.trim()).filter(Boolean);
  if (mode === "teacher") {
    return { klass: parts[0], subject: parts[1], codes, raw: t };
  }
  return { subject: parts[0], teacher: parts[1], codes, raw: t };
}

export async function schoolOverview(year?: string) {
  const result = await mcpFetch("school_overview", year ? { year } : {});
  return { raw: textOf(result) };
}

export async function listClasses(year?: string): Promise<{ classes: ClassInfo[]; raw: string }> {
  const result = await mcpFetch("list_classes", year ? { year } : {});
  const raw = textOf(result);
  const classes: ClassInfo[] = [];
  try {
    for (const row of parseMarkdownTable(raw)) {
      if (row.length < 4) continue;
      const [id, grade, shift, load, hours, homeroom] = row;
      const placedTotal = (load || "0/0").split("/").map(Number);
      classes.push({
        id: id.trim(),
        name: id.trim(),
        grade: grade.trim(),
        shift: (shift || "ពេញថ្ងៃ") as "ព្រឹក" | "ពេញថ្ងៃ",
        placed: placedTotal[0] || 0,
        total: placedTotal[1] || 0,
        hoursPerWeek: Number(hours?.trim()) || 0,
        homeroomTeacher: (homeroom || "").trim(),
      });
    }
  } catch {
    /* fall through, classes stays empty */
  }
  return { classes, raw };
}

export async function listTeachers(year?: string, subject?: string): Promise<{ teachers: TeacherInfo[]; raw: string }> {
  const result = await mcpFetch("list_teachers", { ...(year ? { year } : {}), ...(subject ? { subject } : {}) });
  const raw = textOf(result);
  const teachers: TeacherInfo[] = [];
  try {
    for (const row of parseMarkdownTable(raw)) {
      if (row.length < 6) continue;
      const [name, code, subjectName, hpw, contracted, overtime, days, absence, missing, classes] = row;
      teachers.push({
        name: name.trim(),
        code: code.trim(),
        subject: subjectName.trim(),
        hoursPerWeek: Number(hpw) || 0,
        contracted: Number(contracted) || 0,
        overtime: Number(overtime) || 0,
        teachingDays: Number(days) || 0,
        absencePerWeek: Number(absence) || 0,
        missingHours: Number(missing) || 0,
        classes: (classes || "").split(",").map((c) => c.trim()).filter(Boolean),
      });
    }
  } catch {
    /* fall through */
  }
  return { teachers, raw };
}

export async function curriculum(year?: string): Promise<{ raw: string }> {
  const result = await mcpFetch("curriculum", year ? { year } : {});
  return { raw: textOf(result) };
}

export async function classTimetable(classId: string, term = 1, year?: string): Promise<{ grid: TimetableGrid; raw: string }> {
  const result = await mcpFetch("class_timetable", { class: classId, term, ...(year ? { year } : {}) });
  const raw = textOf(result);
  const rows: TimetableGrid["rows"] = [];
  try {
    const table = parseMarkdownTable(raw);
    if (table.length < 2) throw new Error("no table");
    const header = table[0];
    const dayCols: string[] = header.slice(1);
    for (let r = 1; r < table.length; r++) {
      const row = table[r];
      const slot = parseSlotLabel(row[0]);
      if (!slot) continue;
      const day = dayKey(dayCols[0]) || "Mon";
      const cells: Record<string, TimetableCell> = {};
      dayCols.forEach((dc, i) => {
        const dk = dayKey(dc);
        if (dk) cells[dk] = parseCell(row[i + 1] || "", "class");
      });
      rows.push({
        label: row[0],
        shift: slot.shift,
        period: slot.period,
        time: slot.time,
        day,
        cells,
      });
    }
  } catch {
    /* keep rows empty */
  }
  return { grid: { class: classId, term, rows }, raw };
}

export async function teacherTimetable(teacher: string, term = 1, year?: string): Promise<{ grid: TimetableGrid; raw: string }> {
  const result = await mcpFetch("teacher_timetable", { teacher, term, ...(year ? { year } : {}) });
  const raw = textOf(result);
  const rows: TimetableGrid["rows"] = [];
  try {
    const table = parseMarkdownTable(raw);
    if (table.length < 2) throw new Error("no table");
    const header = table[0];
    const dayCols: string[] = header.slice(1);
    for (let r = 1; r < table.length; r++) {
      const row = table[r];
      const slot = parseSlotLabel(row[0]);
      if (!slot) continue;
      const cells: Record<string, TimetableCell> = {};
      dayCols.forEach((dc, i) => {
        const dk = dayKey(dc);
        if (dk) cells[dk] = parseCell(row[i + 1] || "", "teacher");
      });
      rows.push({
        label: row[0],
        shift: slot.shift,
        period: slot.period,
        time: slot.time,
        day: dayKey(dayCols[0]) || "Mon",
        cells,
      });
    }
  } catch {
    /* keep rows empty */
  }
  return { grid: { class: teacher, term, rows }, raw };
}

export async function findProblems(year?: string): Promise<{ problems: ProblemItem[]; raw: string }> {
  const result = await mcpFetch("find_problems", year ? { year } : {});
  const raw = textOf(result);
  const problems: ProblemItem[] = [];
  try {
    for (const line of raw.split("\n")) {
      const m = line.match(/^\s*[-•]\s*(.+?)\s*—\s*ខ្វះ\s*(\d+)\s*ម៉ោង\s*—\s*គ្រូ\s*(.+?)\s*\(([^)]+)\)\s*$/);
      if (m) {
        problems.push({ class: m[1].trim().split(/\s+/).slice(0, -1).join(" ").trim(), subject: m[1].trim().split(/\s+/).pop() || "", missingHours: Number(m[2]), teacher: m[3].trim(), code: m[4].trim() });
        continue;
      }
      const m2 = line.match(/^\s*[-•]\s*(.+?)\s*—\s*ខ្វះ\s*(\d+)\s*ម៉ោង$/);
      if (m2) {
        const parts = m2[1].trim().split(/\s+/);
        problems.push({ class: parts.slice(0, -1).join(" ").trim(), subject: parts.pop() || "", missingHours: Number(m2[2]) });
      }
    }
  } catch {
    /* fall through */
  }
  return { problems, raw };
}

export interface WhyUnplacedResult {
  class: string;
  subject: string;
  totalHours: number;
  placed: number;
  missing: number;
  teacher?: string;
  code?: string;
  causes: string[];
  fixes: Fix[];
  raw: string;
}

export async function whyUnplaced(classId: string, subject: string, term = 1, year?: string): Promise<WhyUnplacedResult> {
  const result = await mcpFetch("why_unplaced", { class: classId, subject, term, ...(year ? { year } : {}) });
  const raw = textOf(result);
  const out: WhyUnplacedResult = { class: classId, subject, totalHours: 0, placed: 0, missing: 0, causes: [], fixes: [], raw };
  try {
    const headM = raw.match(/^(.+?)\s*—\s*(\d+)\s*ម៉ោង\/សប្ដាហ៍\s*,?\s*ដាក់រួច\s*(\d+)\s*·?\s*គ្រូ\s*(.+?)\s*$/m);
    if (headM) {
      out.totalHours = Number(headM[2]);
      out.placed = Number(headM[3]);
      const teach = headM[4].match(/(.+?)\s*\(([^)]+)\)\s*$/);
      if (teach) { out.teacher = teach[1].trim(); out.code = teach[2].trim(); }
    }
    const missM = raw.match(/ខ្វះ\s*(\d+)\s*ម៉ោង/);
    if (missM) out.missing = Number(missM[1]);
    const fixesSection = raw.split(/ដំណោះស្រាយ/)[1] || "";
    const causeLines: string[] = [];
    const fixes: Fix[] = [];
    let inCauses = false;
    for (const line of fixesSection.split("\n")) {
      const trimmed = line.trim();
      if (/^\s*\d+\.\s/.test(trimmed)) {
        inCauses = false;
        const nm = trimmed.match(/^(\d+)\.\s+(.*)$/);
        if (nm) fixes.push({ n: Number(nm[1]), text: nm[2].trim(), action: nm[2].trim() });
      } else if (trimmed.startsWith("- ") && !inCauses) {
        inCauses = true;
        causeLines.push(trimmed.slice(2));
      }
    }
    out.causes = causeLines;
    out.fixes = fixes;
  } catch {
    /* fall through */
  }
  return out;
}

export interface WhereCanPlaceResult {
  class: string;
  subject: string;
  freeSlots: Slot[];
  blocked: string[];
  note?: string;
  raw: string;
}

export async function whereCanPlace(classId: string, subject: string, term = 1, year?: string): Promise<WhereCanPlaceResult> {
  const result = await mcpFetch("where_can_place", { class: classId, subject, term, ...(year ? { year } : {}) });
  const raw = textOf(result);
  const out: WhereCanPlaceResult = { class: classId, subject, freeSlots: [], blocked: [], raw };
  try {
    let inFree = false;
    let inBlocked = false;
    for (const line of raw.split("\n")) {
      const trimmed = line.trim();
      if (trimmed === "ក្រឡាផ្សេងទៀតដាក់មិនបាន ព្រោះៈ" || trimmed === "ក្រឡាផ្សេងទៀតដាក់មិឞមិនបាន ព្រោះៈ") {
        inFree = false; inBlocked = true; continue;
      }
      if (trimmed.includes("ក្រឡាទំនេរដែលដាក់បានភ្លាម")) { inFree = true; inBlocked = false; continue; }
      const sm = trimmed.match(/^- (ចន្ទ|អង្គារ|ពុធ|ព្រហស្បតិ៍|សុក្រ|សៅរ៍) (ព្រឹឞ|រសៀល) ម៉ោងទី(\d+) \((\d{2}:\d{2}\u2013\d{2}:\d{2})\)$/);
      if (sm) {
        out.freeSlots.push({ day: dayKey(sm[1])!, shift: shiftKey(sm[2])!, period: Number(sm[3]), time: sm[4] });
      } else if (inBlocked && trimmed.startsWith("- ")) {
        out.blocked.push(trimmed.slice(2));
      }
    }
    const noteM = raw.match(/ចំណាំ៖ (.+)/);
    if (noteM) out.note = noteM[1].trim();
  } catch {
    /* fall through */
  }
  return out;
}

export async function proposeChanges(reason: string, changes: any[], term = 1, year?: string): Promise<{ id?: string; raw: string }> {
  const result = await mcpFetch("propose_changes", { reason, changes, term, ...(year ? { year } : {}) });
  const raw = textOf(result);
  let id: string | undefined;
  try {
    const m = raw.match(/id[:=]\s*([A-Za-z0-9\-_]+)/i) || raw.match(/\b(PROP-\d+|[A-Z]{2,}\-\d+)\b/);
    if (m) id = m[1];
  } catch { /* */ }
  return { id, raw };
}

export async function proposeFix(classId: string, subject: string, fix: number, reason = "", term = 1, year?: string): Promise<{ id?: string; raw: string }> {
  const result = await mcpFetch("propose_fix", { class: classId, subject, fix, reason, term, ...(year ? { year } : {}) });
  const raw = textOf(result);
  let id: string | undefined;
  try {
    const m = raw.match(/id[:=]\s*([A-Za-z0-9\-_]+)/i);
    if (m) id = m[1];
  } catch { /* */ }
  return { id, raw };
}

export async function proposalStatus(id?: string): Promise<{ status: string; raw: string }> {
  const result = await mcpFetch("proposal_status", id ? { id } : {});
  const raw = textOf(result);
  const m = raw.match(/(PENDING|APPROVED|REJECTED|រង់ចាំ|អនុញ្ញាត|បដិសេធ)/);
  return { status: m ? m[1] : "unknown", raw };
}

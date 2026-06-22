import { el } from "../modules/dom.js";
import * as d from "../modules/mockData.js";
import { PageHead } from "../components/ui.js";
import { getState } from "../modules/store.js";

const subjectHue = {
  Mathematics: 1, Physics: 2, Chemistry: 3, Biology: 4,
  "English Literature": 5, "World History": 6, "Computer Science": 7, "Visual Art": 8,
};

export function timetablePage() {
  const { role } = getState();
  const root = el("div");
  const today = d.weekdays[Math.min(new Date().getDay() - 1, 4)] || "Monday";

  // collect all period start times for the grid rows
  const times = [...new Set(d.weekdays.flatMap((day) => d.timetable[day].map((c) => c.start)))].sort();

  const cell = (day, time) => {
    const c = d.timetable[day].find((x) => x.start === time);
    if (!c) return `<td class="tt-empty"></td>`;
    return `<td><div class="tt-block hue-${subjectHue[c.subject] || 1}">
      <strong>${c.subject}</strong>
      <span>${c.room}</span>
      <span class="muted">${c.start}–${c.end} · ${c.teacher}</span>
    </div></td>`;
  };

  root.innerHTML = `
    ${PageHead({ title: "Timetable", sub: `${d.school.year} · ${d.school.term}${role === "teacher" ? " · your teaching schedule" : " · Grade 10-B"}`,
      action: `<div class="segmented"><button class="active">Week</button><button>Day</button></div>` })}
    <div class="card" style="overflow:hidden">
      <div class="table-wrap">
        <table class="table tt-table">
          <thead><tr><th class="tt-time-col">Time</th>${d.weekdays.map((day) =>
            `<th class="${day === today ? "tt-today" : ""}">${day}${day === today ? ' <span class="badge badge-accent" style="margin-left:6px">Today</span>' : ""}</th>`).join("")}</tr></thead>
          <tbody>${times.map((t) => `<tr><td class="tt-time-col mono">${t}</td>${d.weekdays.map((day) => cell(day, t)).join("")}</tr>`).join("")}</tbody>
        </table>
      </div>
    </div>`;
  return root;
}

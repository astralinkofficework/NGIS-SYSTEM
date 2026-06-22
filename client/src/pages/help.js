import { el } from "../modules/dom.js";
import { icon } from "../modules/icons.js";
import { PageHead, Card, Btn } from "../components/ui.js";
import { toast } from "../components/toast.js";

const faqs = [
  ["How do I download my report card?", "Open Grades & exams and select “Download report card.” The PDF includes all subjects, your term average, and teacher comments."],
  ["I can't submit an assignment — what should I do?", "Check the deadline and accepted file types (PDF, images, documents up to 20 MB). If it's already past due, contact your teacher through Announcements."],
  ["How is attendance recorded?", "Teachers mark attendance each session as present, late, absent, or excused. Your monthly summary updates automatically on the Attendance page."],
  ["Who can see my grades?", "Only you, your teachers for assigned classes, your linked parent or guardian, and administrators. Access follows strict role-based rules."],
  ["How do I change my password?", "Go to Profile & settings → Security → Change. You'll be signed out of other devices after a successful change."],
];

export function helpPage() {
  const root = el("div");
  root.innerHTML = `
    ${PageHead({ title: "Help center", sub: "Answers, guides, and a direct line to the office" })}
    <div class="grid grid-3" style="margin-bottom:var(--s-5)">
      ${[["Report an issue","flag","Tell us what's not working"],["Contact administration","message","Reach the school office"],["IT support","settings","Account & access problems"]]
        .map(([t,ic,s])=>`<button class="card pad help-card">
          <span class="doc-ic">${icon(ic)}</span><strong style="display:block;margin-top:var(--s-3)">${t}</strong>
          <span class="muted" style="font-size:var(--fs-sm)">${s}</span></button>`).join("")}
    </div>
    ${Card({ title: "Frequently asked questions", flush: true, body: `<div class="faq">${faqs.map(([q,a],i)=>`
      <details ${i===0?"open":""}><summary>${q}${icon("chevronDown")}</summary><p class="muted">${a}</p></details>`).join("")}</div>` })}`;
  root.querySelectorAll(".help-card").forEach((b) => b.addEventListener("click", () =>
    toast("We're here to help", { msg: "A contact form opens here.", type: "info" })));
  return root;
}

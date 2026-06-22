import { el } from "../modules/dom.js";
import { icon } from "../modules/icons.js";
import { school, roleLabels, roles, accounts } from "../modules/mockData.js";
import { Avatar } from "../components/ui.js";

export function loginPage(onLogin) {
  const root = el("div", { class: "auth" });

  const quick = roles.map((r) => `
    <button class="quick-role" data-role="${r}">
      ${Avatar(accounts[r].name, "sm")}
      <span class="col" style="gap:1px;min-width:0;text-align:left">
        <strong>${roleLabels[r]}</strong>
        <span class="muted" style="font-size:var(--fs-xs)">${accounts[r].email}</span>
      </span>
      ${icon("chevronRight")}
    </button>`).join("");

  root.innerHTML = `
    <div class="auth-brand">
      <div class="auth-brand-inner">
        <div class="brand" style="padding:0">
          <div class="brand-mark">${icon("graduation")}</div>
          <div class="brand-text"><strong style="color:#fff">${school.short}</strong>
            <span style="color:rgba(255,255,255,.7)">${school.year}</span></div>
        </div>
        <div class="auth-hero">
          <p class="eyebrow" style="color:rgba(255,255,255,.65)">${school.name}</p>
          <h1 class="display auth-title">One calm place<br>to run the school day.</h1>
          <p class="auth-lede">Attendance, grades, assignments, and announcements — for students,
            teachers, parents, and administrators. Clear, fast, and built around the people who use it.</p>
        </div>
        <div class="auth-foot">
          <div class="auth-chip">${icon("shield")}<span>Role-based access</span></div>
          <div class="auth-chip">${icon("checkCircle")}<span>FERPA-minded privacy</span></div>
          <div class="auth-chip">${icon("trend")}<span>Built for a full term</span></div>
        </div>
      </div>
      <div class="auth-glow"></div>
    </div>

    <div class="auth-panel">
      <div class="auth-card">
        <h2 class="display" style="font-size:var(--fs-h1)">Welcome back</h2>
        <p class="muted" style="margin-top:6px">Sign in to your ${school.short} account.</p>

        <form class="auth-form col gap-4" novalidate>
          <div class="field">
            <label for="email">School email</label>
            <input class="input" id="email" type="email" placeholder="you@ngis.edu" autocomplete="username" value="student@ngis.edu">
          </div>
          <div class="field">
            <div class="row spread"><label for="pw">Password</label>
              <a href="#/login" class="link" style="font-size:var(--fs-xs)">Forgot password?</a></div>
            <input class="input" id="pw" type="password" placeholder="••••••••" autocomplete="current-password" value="demo-password">
          </div>
          <label class="row gap-2" style="font-size:var(--fs-sm);cursor:pointer">
            <input type="checkbox" checked style="width:16px;height:16px;accent-color:var(--accent)"> Keep me signed in
          </label>
          <button class="btn btn-primary" type="submit" style="height:44px">Sign in</button>
        </form>

        <div class="auth-or"><span>or jump straight in (demo)</span></div>
        <div class="quick-roles">${quick}</div>
      </div>
      <p class="auth-fineprint muted">Demo build · front-end only · no real credentials are checked.</p>
    </div>`;

  root.querySelector(".auth-form").addEventListener("submit", (e) => {
    e.preventDefault();
    const email = root.querySelector("#email").value.trim().toLowerCase();
    const match = roles.find((r) => accounts[r].email === email);
    onLogin(match || "student");
  });
  root.querySelectorAll(".quick-role").forEach((b) =>
    b.addEventListener("click", () => onLogin(b.dataset.role)));

  return root;
}

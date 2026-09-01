"use strict";

const fs = require("fs");
const path = require("path");

const root = path.resolve(__dirname, "..");
const roles = ["admin", "teacher", "student", "parent"];
const tags = [
  '<script src="../../assets/js/auth.js"></script>',
  '<script src="../../assets/js/protect.js"></script>',
  '<script src="_auth-bootstrap.js"></script>',
];
const escapedNewline = String.fromCharCode(92) + "n";
const escapedTagPattern = new RegExp(tags.map((tag) => tag.replace(/[.*+?^${}()|[\\]\\\\]/g, "\\\\$&")).join("|"), "g");
let changed = 0;

for (const role of roles) {
  const dir = path.join(root, "pages", role);
  for (const name of fs.readdirSync(dir)) {
    if (!name.endsWith(".html")) continue;
    const file = path.join(dir, name);
    const source = fs.readFileSync(file, "utf8");
    const withoutTags = source.split(escapedNewline).join("\n").replace(escapedTagPattern, "");
    if (!withoutTags.includes("</head>")) throw new Error(`Missing </head> in ${file}`);
    const normalized = withoutTags.replace("</head>", `${tags.join("\n")}\n</head>`);
    if (normalized === source) continue;
    fs.writeFileSync(file, normalized);
    changed += 1;
  }
}
console.log(`Protected pages updated: ${changed}`);

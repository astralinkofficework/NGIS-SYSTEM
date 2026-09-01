"use strict";

const fs = require("fs");
const path = require("path");

const root = path.resolve(__dirname, "..");
const htmlFiles = [];
function walk(dir) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    if (["node_modules", ".git"].includes(entry.name)) continue;
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) walk(full);
    else if (entry.isFile() && full.endsWith(".html")) htmlFiles.push(full);
  }
}
walk(root);

const missing = [];
const refPattern = /(?:src|href)=["']([^"'#?]+)["']/gi;
for (const html of htmlFiles) {
  if (path.relative(root, html).startsWith("_concepts" + path.sep)) continue;
  const source = fs.readFileSync(html, "utf8");
  let match;
  while ((match = refPattern.exec(source))) {
    const ref = match[1];
    if (!ref || ref.includes("${") || ref.startsWith("/") || ref.startsWith("http") || ref.startsWith("data:") || ref.startsWith("mailto:") || ref.startsWith("javascript:")) continue;
    const target = path.resolve(path.dirname(html), ref);
    if (!fs.existsSync(target)) missing.push({ file: path.relative(root, html), ref });
  }
}

console.log(`HTML pages scanned: ${htmlFiles.length}`);
console.log(`Missing local references: ${missing.length}`);
for (const item of missing) console.log(`${item.file} -> ${item.ref}`);
process.exitCode = missing.length ? 1 : 0;

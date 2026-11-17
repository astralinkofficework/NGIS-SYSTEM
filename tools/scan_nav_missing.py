import re

with open('assets/js/layout.js', 'r', encoding='utf-8') as f:
    text = f.read()

# Let's extract NAV = { ... } in layout.js
# Or let's evaluate it via node or inspect with python
import subprocess

node_script = """
const fs = require('fs');
const content = fs.readFileSync('assets/js/layout.js', 'utf8');

// Find NAV definition
const navMatch = content.match(/const NAV = ({[\\s\\S]*?\\n  };)/);
if (!navMatch) {
  console.log('Could not find const NAV = {');
  process.exit(1);
}

// Eval NAV
let NAV;
try {
  eval(navMatch[0]);
} catch(e) {
  console.error('Error evaluating NAV:', e);
  process.exit(1);
}

console.log('Roles in NAV:', Object.keys(NAV));

let missingCount = 0;
for (const [role, cfg] of Object.entries(NAV)) {
  console.log(`\\n--- ROLE: ${role} (${cfg.groups ? cfg.groups.length : 0} groups) ---`);
  if (!cfg.groups) continue;
  cfg.groups.forEach((g, gi) => {
    if (!g.icon) {
      console.log(`  [GROUP MISSING ICON] ${role} -> group '${g.label}' (id: ${g.id})`);
      missingCount++;
    }
    (g.links || []).forEach(l => {
      if (!l.icon) {
        console.log(`  [LINK MISSING ICON] ${role} -> group '${g.label}' -> link '${l.label}' (id: ${l.id}, href: ${l.href})`);
        missingCount++;
      }
      if (l.children) {
        l.children.forEach(sub => {
          if (!sub.icon) {
            console.log(`    [SUBLINK MISSING ICON] ${role} -> sub '${sub.label}' (id: ${sub.id}, href: ${sub.href})`);
            missingCount++;
          }
          if (sub.children) {
            sub.children.forEach(nested => {
              if (!nested.icon) {
                console.log(`      [NESTED LINK MISSING ICON] ${role} -> nested '${nested.label}' (id: ${nested.id}, href: ${nested.href})`);
                missingCount++;
              }
            });
          }
        });
      }
    });
  });
}
console.log(`\\nTotal missing icons in layout.js NAV: ${missingCount}`);
"""

with open('tools/scan_nav_missing.js', 'w', encoding='utf-8') as f:
    f.write(node_script)

const fs = require('fs');
const content = fs.readFileSync('assets/js/layout.js', 'utf8');

// Find NAV definition
const navStart = content.indexOf('const NAV = {');
if (navStart === -1) {
  console.log('Could not find const NAV = {');
  process.exit(1);
}

// Find matching closing brace
let braceCount = 0;
let navEnd = -1;
for (let i = navStart + 12; i < content.length; i++) {
  if (content[i] === '{') braceCount++;
  else if (content[i] === '}') {
    braceCount--;
    if (braceCount === 0) {
      navEnd = i + 1;
      break;
    }
  }
}

const navCode = 'global.NAV = ' + content.slice(navStart + 12, navEnd);
try {
  eval(navCode);
} catch(e) {
  console.error('Error evaluating NAV:', e);
  process.exit(1);
}

console.log('Roles in NAV:', Object.keys(global.NAV));

let missingCount = 0;
for (const [role, cfg] of Object.entries(global.NAV)) {
  console.log(`\n--- ROLE: ${role} (${cfg.groups ? cfg.groups.length : 0} groups) ---`);
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
console.log(`\nTotal missing icons in layout.js NAV: ${missingCount}`);

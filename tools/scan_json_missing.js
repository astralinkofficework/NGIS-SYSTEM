const fs = require('fs');
const data = JSON.parse(fs.readFileSync('data/sidebar_nav.json', 'utf8'));

let missingCount = 0;
for (const [portal, pdata] of Object.entries(data.portals)) {
  console.log(`\n=== Portal: ${portal} ===`);
  (pdata.groups || []).forEach(g => {
    if (!g.icon) {
      console.log(`  [GROUP MISSING ICON] ${portal} -> group '${g.label}' (id: ${g.id})`);
      missingCount++;
    }
    (g.links || []).forEach(l => {
      if (!l.icon) {
        console.log(`  [LINK MISSING ICON] ${portal} -> group '${g.label}' -> link '${l.label}' (id: ${l.id}, href: ${l.href})`);
        missingCount++;
      }
      if (l.children) {
        l.children.forEach(sub => {
          if (!sub.icon) {
            console.log(`    [SUBLINK MISSING ICON] ${portal} -> sub '${sub.label}' (id: ${sub.id}, href: ${sub.href})`);
            missingCount++;
          }
          if (sub.children) {
            sub.children.forEach(nested => {
              if (!nested.icon) {
                console.log(`      [NESTED LINK MISSING ICON] ${portal} -> nested '${nested.label}' (id: ${nested.id}, href: ${nested.href})`);
                missingCount++;
              }
            });
          }
        });
      }
    });
  });
}
console.log(`\nTotal missing icons in sidebar_nav.json: ${missingCount}`);

const fs = require('fs');
const { execSync } = require('child_process');

const jsFiles = fs.readdirSync('assets/js').filter(f => f.endsWith('.js'));
let hasError = false;
for (const f of jsFiles) {
  try {
    execSync(`node --check assets/js/${f}`);
    console.log(`OK: assets/js/${f}`);
  } catch (e) {
    console.error(`ERROR in assets/js/${f}:`, e.message);
    hasError = true;
  }
}
if (!hasError) {
  console.log('All JS files passed syntax check!');
}


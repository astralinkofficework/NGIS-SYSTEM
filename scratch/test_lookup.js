const fs = require('fs');

const state = JSON.parse(fs.readFileSync('data/timetable_state.json', 'utf8'));
const classes = state.classes;
console.log("Class 0 id:", classes[0].id, "shift:", classes[0].shift);

const demoPlacements = [
  { cid: 'class_7A', shift: 'ព្រឹក', p: 1, sub: 'Mathematics', code: 'M1', tname: 'Bun Sophy', tid: 't_M1', color: 'bg-blue-600', disc: 'Math' }
];

const classSlots = {};
demoPlacements.forEach(dp => {
  classSlots[dp.cid + '|' + dp.shift + '|' + dp.p] = dp;
});

const key = classes[0].id + '|' + classes[0].shift + '|1';
console.log("Looking up key:", key);
console.log("Found in classSlots:", classSlots[key]);
console.log("Keys in classSlots:", Object.keys(classSlots));


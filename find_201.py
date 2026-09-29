import subprocess

test_js = """
const fs = require('fs');
const html = fs.readFileSync('dump_encontrados_fixed.html', 'utf8');

const rawMatch = html.match(/<div id='raw-data' style='display:none;'>(.*?)<\\/div>/);
const rawData = rawMatch ? rawMatch[1] : '';
const items = rawData.split('~');

const regMap = { 'S': 'Regional Sul', 'SP': 'Regional SP', 'SD': 'Regional Sudeste', 'N': 'Regional NNCO', 'O': 'Outras' };

// Test by regional
for (let r of ['S', 'SP', 'SD', 'N']) {
    let count = 0;
    let sum = 0;
    for (let it of items) {
        let cols = it.split('|');
        if (cols[0] === r) {
            count++;
            sum += parseFloat(cols[7].replace(',', '.')) || 0;
        }
    }
    console.log(`Regional ${r} => Count: ${count}, Sum: ${sum}`);
}

// Test by month
let months = {};
for (let it of items) {
    let cols = it.split('|');
    let m = cols[6] ? cols[6].substring(0, 7) : '';
    if (!months[m]) months[m] = { count: 0, sum: 0 };
    months[m].count++;
    months[m].sum += parseFloat(cols[7].replace(',', '.')) || 0;
}
console.log('Months:', months);

// Test by area
let areas = {};
for (let it of items) {
    let cols = it.split('|');
    let a = cols[1];
    if (!areas[a]) areas[a] = { count: 0, sum: 0 };
    areas[a].count++;
    areas[a].sum += parseFloat(cols[7].replace(',', '.')) || 0;
}
console.log('Areas:', areas);
"""

with open('find_201.js', 'w', encoding='utf-8') as f:
    f.write(test_js)

res = subprocess.run(["node", "find_201.js"], capture_output=True, text=True)
print(res.stdout)

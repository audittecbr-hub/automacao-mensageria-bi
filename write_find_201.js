const fs = require('fs');
const html = fs.readFileSync('dump_encontrados_fixed.html', 'utf8');
const rawMatch = html.match(/<div id='raw-data' style='display:none;'>(.*?)<\/div>/);
const rawData = rawMatch ? rawMatch[1] : '';
const items = rawData.split('~');

let out = '';

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
    out += `Regional ${r} => Count: ${count}, Sum: ${sum}\n`;
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
out += 'Months:\n' + JSON.stringify(months, null, 2) + '\n';

fs.writeFileSync('find_201_utf8.txt', out, 'utf8');

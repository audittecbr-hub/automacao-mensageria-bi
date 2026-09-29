
const fs = require('fs');
const html = fs.readFileSync('dump_apresentados_fixed.html', 'utf8');

// Simple DOM emulation
const rawMatch = html.match(/<div id='raw-data' style='display:none;'>(.*?)<\/div>/);
const rawData = rawMatch ? rawMatch[1] : '';
const items = rawData.split('~');

console.log('Total items in raw-data:', items.length);

let totalSum = 0;
let validCount = 0;
for(let i=0; i<items.length; i++) {
    let cols = items[i].split('|');
    if(cols.length >= 8) {
        let valNum = parseFloat(cols[7].replace(',', '.')) || 0;
        totalSum += valNum;
        validCount++;
    }
}
console.log('Valid rows count:', validCount);
console.log('Calculated Total:', totalSum.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' }));


const fs = require('fs');
const html = fs.readFileSync('dump_encontrados_fixed.html', 'utf8');

const rawMatch = html.match(/<div id='raw-data' style='display:none;'>(.*?)<\/div>/);
const rawData = rawMatch ? rawMatch[1] : '';
const items = rawData.split('~');

console.log('Total items in raw:', items.length);

const regMap = { 'S': 'Regional Sul', 'SP': 'Regional SP', 'SD': 'Regional Sudeste', 'N': 'Regional NNCO', 'O': 'Outras' };

let visibleCount = 0;
let visibleSum = 0;

// Default filter values
let qG = '';
let qT = '';
let qR = '';
let qM = '';
let qA = '';
let qC = '';
let qJ = '';
let qP = '';
let qD = '';
let qDM = '';

for(let i=0; i<items.length; i++) {
    let item = items[i];
    if(!item) continue;
    let cols = item.split('|');
    if(cols.length < 8) continue;
    
    let rCode = cols[0];
    let rName = regMap[rCode] || rCode;
    let area = cols[1];
    let cli = cols[2];
    let job = cols[3];
    let prod = cols[4];
    let dtRt = cols[5];
    let dtMov = cols[6];
    let valStr = cols[7];
    let rowMes = dtMov ? dtMov.substring(0, 7) : (dtRt ? dtRt.substring(0, 7) : '');
    let valNum = parseFloat(valStr.replace(',', '.')) || 0;
    
    // Check match
    let tT = 'encontrado';
    let tR = rName.toLowerCase();
    let tA = area.toLowerCase();
    let tC = cli.toLowerCase();
    let tJ = job.toLowerCase();
    let tP = prod.toLowerCase();
    
    let matchG = (qG === '' || tA.indexOf(qG)>-1 || tC.indexOf(qG)>-1 || tJ.indexOf(qG)>-1 || tP.indexOf(qG)>-1 || tR.indexOf(qG)>-1 || tT.indexOf(qG)>-1);
    let matchT = (qT === '' || tT.indexOf(qT)>-1);
    let matchR = (qR === '' || tR.indexOf(qR)>-1);
    let matchM = (qM === '' || rowMes === qM);
    let matchA = (qA === '' || tA.indexOf(qA)>-1);
    let matchC = (qC === '' || tC.indexOf(qC)>-1);
    let matchJ = (qJ === '' || tJ.indexOf(qJ)>-1);
    let matchP = (qP === '' || tP.indexOf(qP)>-1);
    let matchD = (qD === '' || dtRt === qD);
    let matchDM = (qDM === '' || dtMov === qDM);
    
    if(matchG && matchT && matchR && matchM && matchA && matchC && matchJ && matchP && matchD && matchDM) {
        visibleCount++;
        visibleSum += valNum;
    }
}

console.log('Visible count:', visibleCount);
console.log('Visible sum:', visibleSum.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' }));

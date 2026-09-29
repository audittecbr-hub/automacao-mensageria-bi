const fs = require('fs');
const html = fs.readFileSync('dump_matriz_apneg_verified.html', 'utf8');

function getSpans(containerId) {
    const reg = new RegExp(`<div style='display:none;' id='${containerId}'>(.*?)<\\/div>`);
    const match = html.match(reg);
    if (!match) return [];
    const raw = match[1];
    const spanReg = /<span class='(.*?)' data-regional='(.*?)' data-valor='(.*?)' data-valor-sr='(.*?)' data-data='(.*?)' data-produto='(.*?)'><\/span>/g;
    let spans = [];
    let m;
    while ((m = spanReg.exec(raw)) !== null) {
        spans.push({
            regional: m[2],
            valor: parseFloat(m[3].replace(',', '.')) || 0,
            valor_sr: parseFloat(m[4].replace(',', '.')) || 0,
            data: m[5],
            produto: m[6]
        });
    }
    return spans;
}

const apnegSpans = getSpans('dados-apneg-total-container');
console.log('Total apneg spans:', apnegSpans.length);

let totalComRT = 0;
let regSums = {};
for (let s of apnegSpans) {
    totalComRT += s.valor;
    regSums[s.regional] = (regSums[s.regional] || 0) + s.valor;
}

console.log('Total Aprovados em Negociação (Com RT):', totalComRT.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' }));
for (let r of Object.keys(regSums)) {
    console.log(`  - ${r}:`, regSums[r].toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' }));
}

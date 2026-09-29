const fs = require('fs');

const htmlMatriz = fs.readFileSync('dump_matriz_perfect.html', 'utf8');
const htmlAprov = fs.readFileSync('dump_HTML_Detalhamento_Aprovados.html', 'utf8');

function getSpans(html, containerId) {
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

const matrizSpans = getSpans(htmlMatriz, 'dados-aprov-total-container');

// Group by Month and Product
let matrizMap = {};
for (let s of matrizSpans) {
    let key = `${s.data}|${s.produto}`;
    matrizMap[key] = (matrizMap[key] || 0) + s.valor;
}

// Read raw items from Detalhamento
const rawMatch = htmlAprov.match(/<div id='raw-data' style='display:none;'>(.*?)<\/div>/)[1];
const items = rawMatch.split('~').filter(Boolean);

let detalheMap = {};
for (let item of items) {
    const cols = item.split('|');
    const prod = cols[4];
    const dtRt = cols[5];
    const dtMov = cols[6];
    const val = parseFloat(cols[7].replace(',', '.')) || 0;
    if (dtRt >= '2026-06-12') {
        const rowMes = dtMov.substring(0, 7);
        // Find which product filter in matrix matches cols[4]
        let key = `${rowMes}|${prod}`;
        detalheMap[key] = (detalheMap[key] || 0) + val;
    }
}

console.log('--- COMPARING MONTH/PRODUCT SUMS ---');
let allKeys = new Set([...Object.keys(matrizMap), ...Object.keys(detalheMap)]);
let diffSum = 0;
for (let k of [...allKeys].sort()) {
    let mVal = matrizMap[k] || 0;
    let dVal = detalheMap[k] || 0;
    let diff = mVal - dVal;
    if (Math.abs(diff) > 0.01) {
        console.log(`Key ${k}: Matriz = ${mVal.toFixed(2)}, Detalhe = ${dVal.toFixed(2)}, Diff = ${diff.toFixed(2)}`);
        diffSum += diff;
    }
}
console.log('Total Diff Sum:', diffSum.toFixed(2));

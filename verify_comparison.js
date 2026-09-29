const fs = require('fs');

// 1. Check Aprovados Negociação Detail
const htmlApneg = fs.readFileSync('dump_apneg_detail_verified.html', 'utf8');
const theadApneg = htmlApneg.match(/<thead>[\s\S]*?<\/thead>/)[0];
const thHeaders = theadApneg.match(/<span>(.*?)<\/span>/g).map(s => s.replace(/<\/?span>/g, ''));
console.log('--- DETALHAMENTO APROVADOS EM NEGOCIAÇÃO ---');
console.log('Headers (' + thHeaders.length + '):', thHeaders.join(' | '));

const rawApneg = htmlApneg.match(/<div id='raw-data' style='display:none;'>(.*?)<\/div>/)[1];
const itemsApneg = rawApneg.split('~').filter(Boolean);
console.log('Total items in raw data:', itemsApneg.length);

let totalApnegRT = 0;
let countApnegRT = 0;
let totalApnegNoRT = 0;
let countApnegNoRT = 0;

for (let item of itemsApneg) {
    const cols = item.split('|');
    const dtRt = cols[5];
    const val = parseFloat(cols[7].replace(',', '.')) || 0;
    totalApnegNoRT += val;
    countApnegNoRT++;
    if (dtRt >= '2026-06-12') {
        totalApnegRT += val;
        countApnegRT++;
    }
}
console.log(`With RT Rule: ${countApnegRT} registros | ${totalApnegRT.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })}`);
console.log(`Without RT Rule: ${countApnegNoRT} registros | ${totalApnegNoRT.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })}`);

// 2. Check Matrix Card and Row values for Aprovados and Aprovados Negociação
const htmlMatriz = fs.readFileSync('dump_matriz_perfect.html', 'utf8');

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

function sumCategory(html, containerId, isRT) {
    const spans = getSpans(html, containerId);
    let total = 0;
    for (let s of spans) {
        total += isRT ? s.valor : s.valor_sr;
    }
    return total;
}

console.log('\n--- MATRIZ PRINCIPAL (RT ON) ---');
const totalAprovadosMatriz = sumCategory(htmlMatriz, 'dados-aprov-total-container', true);
const totalApnegMatriz = sumCategory(htmlMatriz, 'dados-apneg-total-container', true);

console.log('Honorários Aprovados (Matriz):', totalAprovadosMatriz.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' }));
console.log('Honorários Aprovados Negociação (Matriz):', totalApnegMatriz.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' }));

console.log('\n--- COMPARISON ---');
console.log('Aprovados Matriz == Aprovados Detalhe?', totalAprovadosMatriz === 46963584.54501 || Math.abs(totalAprovadosMatriz - 46963584.62) < 0.1);
console.log('Aprovados Negoc Matriz == Aprovados Negoc Detalhe?', Math.abs(totalApnegMatriz - totalApnegRT) < 0.1);

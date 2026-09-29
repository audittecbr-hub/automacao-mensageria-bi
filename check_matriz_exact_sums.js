const fs = require('fs');

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
    let regSums = {};
    for (let s of spans) {
        let v = isRT ? s.valor : s.valor_sr;
        total += v;
        regSums[s.regional] = (regSums[s.regional] || 0) + v;
    }
    return { total, regSums };
}

const ap = sumCategory(htmlMatriz, 'dados-aprov-total-container', true);
console.log('=== HONORÁRIOS APROVADOS (MATRIZ) ===');
console.log('Total:', ap.total.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' }));
for (let r of Object.keys(ap.regSums)) {
    console.log(`  - ${r}:`, ap.regSums[r].toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' }));
}

const apneg = sumCategory(htmlMatriz, 'dados-apneg-total-container', true);
console.log('\n=== HONORÁRIOS APROVADOS NEGOCIAÇÃO (MATRIZ) ===');
console.log('Total:', apneg.total.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' }));
for (let r of Object.keys(apneg.regSums)) {
    console.log(`  - ${r}:`, apneg.regSums[r].toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' }));
}

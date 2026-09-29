const fs = require('fs');

const html = fs.readFileSync('dump_fresh_direct_eval.html', 'utf8');

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

const ap = getSpans(html, 'dados-aprov-total-container');
for (let s of ap) {
    if (s.valor > 0) {
        console.log(`${s.data} | ${s.regional} | ${s.produto} | Val: ${s.valor}`);
    }
}

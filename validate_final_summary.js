const fs = require('fs');

function testDetail(filename, title) {
    const html = fs.readFileSync(filename, 'utf8');
    const rawMatch = html.match(/<div id='raw-data' style='display:none;'>(.*?)<\/div>/)[1];
    const items = rawMatch.split('~').filter(Boolean);
    let countRT = 0, sumRT = 0;
    let countNoRT = 0, sumNoRT = 0;
    for (let item of items) {
        const cols = item.split('|');
        const dtRt = cols[5];
        const val = parseFloat(cols[7].replace(',', '.')) || 0;
        countNoRT++;
        sumNoRT += val;
        if (dtRt >= '2026-06-12') {
            countRT++;
            sumRT += val;
        }
    }
    console.log(`=== ${title} ===`);
    console.log(`- Com Regra RT (Default): ${countRT} registros | ${sumRT.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })}`);
    console.log(`- Sem Regra RT: ${countNoRT} registros | ${sumNoRT.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })}`);
    return { countRT, sumRT, countNoRT, sumNoRT };
}

const aprov = testDetail('dump_HTML_Detalhamento_Aprovados.html', 'DETALHAMENTO HONORÁRIOS APROVADOS');
const apneg = testDetail('dump_HTML_Detalhamento_Aprovados_Negociacao.html', 'DETALHAMENTO HONORÁRIOS APROVADOS EM NEGOCIAÇÃO');

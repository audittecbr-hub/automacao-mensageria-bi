const fs = require('fs');
const html = fs.readFileSync('dump_detalhamento_aprovados_verified.html', 'utf8');

// 1. Script check
const scriptStart = html.indexOf('<script>') + '<script>'.length;
const scriptEnd = html.indexOf('</script>');
const jsCode = html.substring(scriptStart, scriptEnd);

fs.writeFileSync('temp_aprovados_script.js', jsCode, 'utf8');
console.log('Saved temp_aprovados_script.js');

// 2. Column alignment check
const theadMatch = html.match(/<thead>[\s\S]*?<\/thead>/)[0];
const thHeaders = theadMatch.match(/<span>(.*?)<\/span>/g).map(s => s.replace(/<\/?span>/g, ''));
console.log('THEAD Headers (' + thHeaders.length + '):', thHeaders.join(' | '));

// Check raw items
const rawMatch = html.match(/<div id='raw-data' style='display:none;'>(.*?)<\/div>/)[1];
const items = rawMatch.split('~').filter(Boolean);
console.log('Total raw items in data:', items.length);

const regMap = { 'S': 'Regional Sul', 'SP': 'Regional SP', 'SD': 'Regional Sudeste', 'N': 'Regional NNCO', 'O': 'Outras' };

let totalWithRT = 0;
let countWithRT = 0;
let totalWithoutRT = 0;
let countWithoutRT = 0;

let sampleRows = [];

for (let i = 0; i < items.length; i++) {
    const cols = items[i].split('|');
    const rCode = cols[0];
    const rName = regMap[rCode] || rCode;
    const area = cols[1];
    const cli = cols[2];
    const job = cols[3];
    const prod = cols[4];
    const dtRt = cols[5];
    const dtMov = cols[6];
    const val = parseFloat(cols[7].replace(',', '.')) || 0;

    totalWithoutRT += val;
    countWithoutRT++;

    if (dtRt >= '2026-06-12') {
        totalWithRT += val;
        countWithRT++;
    }

    if (i < 5) {
        sampleRows.push({
            Tipo: 'Aprovado',
            Regional: rName,
            AreaAtual: area,
            Cliente: cli,
            Job: job,
            Produto: prod,
            DataRT: dtRt,
            DataMov: dtMov,
            Valor: 'R$ ' + val.toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
        });
    }
}

console.log('\n--- SIMULATION RESULTS ---');
console.log(`With RT Rule (Default): ${countWithRT} registros | ${totalWithRT.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })}`);
console.log(`Without RT Rule: ${countWithoutRT} registros | ${totalWithoutRT.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })}`);

console.log('\n--- SAMPLE ALIGNED ROWS (First 5) ---');
console.table(sampleRows);

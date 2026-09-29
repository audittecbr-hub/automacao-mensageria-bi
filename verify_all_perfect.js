const fs = require('fs');
const html = fs.readFileSync('dump_matriz_perfect.html', 'utf8');

// 1. Verify script syntax
const scriptStart = html.indexOf('<script>') + '<script>'.length;
const scriptEnd = html.indexOf('</script>');
const jsCode = html.substring(scriptStart, scriptEnd);

fs.writeFileSync('temp_perfect_script.js', jsCode, 'utf8');
console.log('Saved temp_perfect_script.js');

// 2. Check HTML elements
const cardsMatch = html.match(/<div class='card'>/g);
console.log('Total summary cards in HTML:', cardsMatch ? cardsMatch.length : 0);

// Check card IDs in HTML
const cardIds = [
    'card-credito-sem-hon',
    'card-encontrados',
    'card-apresentados',
    'card-aprov-negoc',
    'card-aprov',
    'card-nao-aprovados',
    'card-perdidos',
    'card-nao-aprovados-real'
];

for (let id of cardIds) {
    if (html.includes(`id='${id}'`)) {
        console.log(`  ✓ Card found: ${id}`);
    } else {
        console.log(`  ✗ Card MISSING: ${id}`);
    }
}

// 3. Simulate calculation of all categories
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

function sumCategory(containerId, isRT) {
    const spans = getSpans(containerId);
    let total = 0;
    let regSums = {};
    for (let s of spans) {
        let v = isRT ? s.valor : s.valor_sr;
        total += v;
        regSums[s.regional] = (regSums[s.regional] || 0) + v;
    }
    return { total, regSums };
}

console.log('\n--- SIMULATED VALUES (RT ON) ---');
const cats = [
    { name: 'Crédito Sem Hon', id: 'dados-cred-sem-container' },
    { name: 'Encontrados', id: 'dados-enc-container' },
    { name: 'Apresentados', id: 'dados-apres-container' },
    { name: 'Aprovados em Negociação', id: 'dados-apneg-total-container' },
    { name: 'Aprovados Total', id: 'dados-aprov-total-container' },
    { name: 'Em Negociação', id: 'dados-nao-aprov-container' },
    { name: 'Perdidos', id: 'dados-perdidos-container' },
    { name: 'Não Aprovados Real', id: 'dados-nao-aprovados-real-container' }
];

for (let c of cats) {
    let res = sumCategory(c.id, true);
    console.log(`${c.name}: ${res.total.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })}`);
    for (let r of Object.keys(res.regSums)) {
        if (res.regSums[r] > 0) {
            console.log(`   - ${r}: ${res.regSums[r].toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })}`);
        }
    }
}

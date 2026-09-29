const fs = require('fs');
const html = fs.readFileSync('dump_enc_rt_verified.html', 'utf8');

// 1. Check syntax of the embedded script
const scriptStart = html.indexOf('<script>') + '<script>'.length;
const scriptEnd = html.indexOf('</script>');
const jsCode = html.substring(scriptStart, scriptEnd);

fs.writeFileSync('temp_rt_script.js', jsCode, 'utf8');

const rawMatch = html.match(/<div id='raw-data' style='display:none;'>(.*?)<\/div>/);
const rawData = rawMatch ? rawMatch[1] : '';
const items = rawData.split('~');

console.log('Total items in raw-data:', items.length);

function runSimulation(isRTActive, activeMonths) {
    let count = 0;
    let sum = 0;
    for (let it of items) {
        let cols = it.split('|');
        if (cols.length < 8) continue;
        let dtRtStr = cols[5];
        let dtMovStr = cols[6];
        let rowMes = dtMovStr ? dtMovStr.substring(0, 7) : (dtRtStr ? dtRtStr.substring(0, 7) : '');
        let valNum = parseFloat(cols[7].replace(',', '.')) || 0;

        let matchRT = (!isRTActive || (dtRtStr && dtRtStr >= '2026-06-12'));
        let matchMes = (activeMonths[rowMes] === true);

        if (matchRT && matchMes) {
            count++;
            sum += valNum;
        }
    }
    return { count, sum };
}

const allMonths = {
    '2026-06': true,
    '2026-07': true,
    '2026-08': true,
    '2026-09': true,
    '2026-10': true,
    '2026-11': true,
    '2026-12': true
};

const defaultState = runSimulation(true, allMonths);
console.log('1. Default State (RT ON, Todos os Meses):');
console.log('   Registros:', defaultState.count);
console.log('   Valor:', defaultState.sum.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' }));

const rtOffState = runSimulation(false, allMonths);
console.log('2. RT OFF State (RT OFF, Todos os Meses):');
console.log('   Registros:', rtOffState.count);
console.log('   Valor:', rtOffState.sum.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' }));

const augOnly = runSimulation(true, { '2026-08': true });
console.log('3. Agosto/2026 State (RT ON, Apenas 2026-08):');
console.log('   Registros:', augOnly.count);
console.log('   Valor:', augOnly.sum.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' }));

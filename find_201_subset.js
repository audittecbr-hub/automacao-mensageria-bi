const fs = require('fs');
const html = fs.readFileSync('dump_encontrados_fixed.html', 'utf8');
const rawMatch = html.match(/<div id='raw-data' style='display:none;'>(.*?)<\/div>/);
const rawData = rawMatch ? rawMatch[1] : '';
const items = rawData.split('~');

console.log('Total items in raw:', items.length);

const parsed = [];
for (let it of items) {
    let cols = it.split('|');
    if (cols.length < 8) continue;
    parsed.push({
        r: cols[0],
        area: cols[1],
        cli: cols[2],
        job: cols[3],
        prod: cols[4],
        rt: cols[5],
        mov: cols[6],
        mes: cols[6] ? cols[6].substring(0, 7) : '',
        val: parseFloat(cols[7].replace(',', '.')) || 0
    });
}

console.log('Parsed count:', parsed.length);

// Let's find any subset that has count === 201
// Test combinations of filters:
// 1. By Area
let areas = [...new Set(parsed.map(x => x.area))];
for (let a of areas) {
    let sub = parsed.filter(x => x.area === a);
    if (sub.length === 201) console.log('MATCH Area:', a);
}

// 2. By Month + Area
let months = [...new Set(parsed.map(x => x.mes))];
for (let m of months) {
    let subM = parsed.filter(x => x.mes === m);
    if (subM.length === 201) {
        let sum = subM.reduce((acc, x) => acc + x.val, 0);
        console.log(`MATCH Month ${m}: count=201, sum=${sum}`);
    }
    for (let a of areas) {
        let sub = parsed.filter(x => x.mes === m && x.area === a);
        if (sub.length === 201) {
            let sum = sub.reduce((acc, x) => acc + x.val, 0);
            console.log(`MATCH Month ${m} + Area ${a}: count=201, sum=${sum}`);
        }
    }
}

// 3. By Regional + Month
for (let r of ['S', 'SP', 'SD', 'N']) {
    let subR = parsed.filter(x => x.r === r);
    if (subR.length === 201) console.log('MATCH Regional:', r);
    for (let m of months) {
        let sub = parsed.filter(x => x.r === r && x.mes === m);
        if (sub.length === 201) {
            let sum = sub.reduce((acc, x) => acc + x.val, 0);
            console.log(`MATCH Regional ${r} + Month ${m}: count=201, sum=${sum}`);
        }
    }
}

// 4. By Product
let prods = [...new Set(parsed.map(x => x.prod))];
for (let p of prods) {
    let subP = parsed.filter(x => x.prod === p);
    if (subP.length === 201) console.log('MATCH Prod:', p);
    for (let m of months) {
        let sub = parsed.filter(x => x.prod === p && x.mes === m);
        if (sub.length === 201) {
            let sum = sub.reduce((acc, x) => acc + x.val, 0);
            console.log(`MATCH Prod ${p} + Month ${m}: count=201, sum=${sum}`);
        }
    }
}
console.log('Finished search in parsed items.');

const fs = require('fs');

const dbRows = fs.readFileSync('db_aprov_rows.txt', 'utf8').split('\n').map(s => s.trim()).filter(Boolean);
const html = fs.readFileSync('dump_detalhamento_aprovados_verified.html', 'utf8');

const rawMatch = html.match(/<div id='raw-data' style='display:none;'>(.*?)<\/div>/)[1];
const items = rawMatch.split('~').filter(Boolean);

let htmlJobs = new Set();
for (let item of items) {
    const cols = item.split('|');
    const dtRt = cols[5];
    if (dtRt >= '2026-06-12') {
        htmlJobs.add(cols[3]); // JOB
    }
}

for (let r of dbRows) {
    const [job, dtRt, dtMov, val] = r.split('|');
    if (!htmlJobs.has(job)) {
        console.log('Missing in HTML:', job, dtRt, dtMov, val);
    }
}

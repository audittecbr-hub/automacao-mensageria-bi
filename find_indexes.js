const fs = require('fs');
const html = fs.readFileSync('dump_encontrados_fixed.html', 'utf8');
const rawMatch = html.match(/<div id='raw-data' style='display:none;'>(.*?)<\/div>/);
const rawData = rawMatch ? rawMatch[1] : '';
const items = rawData.split('~');

const searchJobs = [
    "86730-FTX",
    "87233-RPQ",
    "86146-T",
    "87613-FTX",
    "87616-FTX",
    "87628-RPQ",
    "87724-FTX",
    "87724-PRT",
    "87259-FTX"
];

for (let i = 0; i < items.length; i++) {
    for (let j of searchJobs) {
        if (items[i].includes(j)) {
            console.log(`Index ${i}: ${items[i]}`);
            break;
        }
    }
}

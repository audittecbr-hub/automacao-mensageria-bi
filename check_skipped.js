const fs = require('fs');
const html = fs.readFileSync('dump_encontrados_fixed.html', 'utf8');
const rawMatch = html.match(/<div id='raw-data' style='display:none;'>(.*?)<\/div>/);
const rawData = rawMatch ? rawMatch[1] : '';
const items = rawData.split('~');

// In Image 1, we know the first 11 rows:
// 1. Index 5
// 2. Index 15
// 3. Index 17
// 4. Index 63
// 5. Index 67
// 6. Index 68
// 7. Index 69
// 8. Index 81
// 9. Index 82
// 10. Index 121
// 11. Index 122

// What about rows between 0 and 122?
// Why was Index 0 not included? (S|OPERAÇÃO)
// Why was Index 1 not included? (SD|REUNIÃO TÉCNICA)
// Why was Index 2 not included? (N|FIM)
// Why was Index 3 not included? (SP|FIM)
// Why was Index 4 not included? (SD|COMPENSAÇÃO|NUTRIMINAS|86210-T) -> wait, why not Nutriminas?
// Why was Index 6 not included? (SP|AJUÍZAMENTO|HOTEL FAZENDA ARAR) -> wait, why not Hotel Fazenda?

console.log("Index 4:", items[4]);
console.log("Index 6:", items[6]);
console.log("Index 7:", items[7]);
console.log("Index 8:", items[8]);
console.log("Index 9:", items[9]);
console.log("Index 10:", items[10]);
console.log("Index 11:", items[11]);
console.log("Index 12:", items[12]);
console.log("Index 13:", items[13]);
console.log("Index 14:", items[14]);
console.log("Index 16:", items[16]);

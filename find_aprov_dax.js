const fs = require('fs');
const dax = fs.readFileSync('matriz_perfect.dax', 'utf8');

const lines = dax.split('\n');
for (let i = 0; i < lines.length; i++) {
    if (lines[i].includes('Honorários aprovados') || lines[i].includes('dado-aprov')) {
        console.log(`Line ${i + 1}: ${lines[i]}`);
    }
}

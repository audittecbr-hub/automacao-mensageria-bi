const fs = require('fs');
const html = fs.readFileSync('dump_matriz_perfect.html', 'utf8');

const scriptStart = html.indexOf('<script>');
const scriptEnd = html.indexOf('</script>');
const js = html.substring(scriptStart, scriptEnd);

const lines = js.split('\n');
for (let i = 0; i < lines.length; i++) {
    if (lines[i].includes('aprov') || lines[i].includes('sAp')) {
        console.log(`JS Line ${i + 1}: ${lines[i]}`);
    }
}

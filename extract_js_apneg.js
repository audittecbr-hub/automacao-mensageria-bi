const fs = require('fs');
const html = fs.readFileSync('dump_matriz_apneg_verified.html', 'utf8');

const scriptStart = html.indexOf('<script>') + '<script>'.length;
const scriptEnd = html.indexOf('</script>');
const jsCode = html.substring(scriptStart, scriptEnd);

fs.writeFileSync('temp_matriz_apneg_script.js', jsCode, 'utf8');
console.log('Saved temp_matriz_apneg_script.js');

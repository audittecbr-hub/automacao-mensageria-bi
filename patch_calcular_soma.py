import re

file_path = r'C:\Users\cristhofer.maciel.GRUPOSTUDIO\Desktop\Mockup_Honorarios_Matriz_Corrigido.dax'
with open(file_path, 'r', encoding='utf8') as f:
    dax = f.read()

# 1. Fix Margin to 150px
dax = dax.replace('margin-bottom: 80px;', 'margin-bottom: 150px;')

# 2. Fix calcularSoma
# We need to replace the entire calcularSoma block. Let's find it.
start_idx = dax.find('"function calcularSoma(')
end_idx = dax.find('"function filtrarTudo() {" &')
if start_idx != -1 and end_idx != -1:
    # Build new calcularSoma
    new_calcular = '''"function calcularSoma(classe) {" &
          "var spans = document.getElementsByClassName(classe);" &
          "var soma = { 'Regional Sul': 0, 'Regional Sudeste': 0, 'Regional Sudeste 2': 0, 'Regional NNCO': 0, 'Total': 0 };" &
          "var prodBox = document.getElementById('global-produto');" &
          "var prod = prodBox ? prodBox.value : '';" &
          "var checkedBoxes = document.querySelectorAll('.mes-checkbox:checked');" &
          "var selectedMeses = {};" &
          "for(var k=0; k<checkedBoxes.length; k++) { selectedMeses[checkedBoxes[k].value] = true; }" &
          "for(var i=0; i<spans.length; i++) {" &
              "var d = spans[i].getAttribute('data-data');" &
              "var pass = true;" &
              "if(!selectedMeses[d]) pass = false;" &
              "var p = spans[i].getAttribute('data-produto');" &
              "if(classe !== 'dado-caixa' && classe !== 'dado-reuniao' && prod !== '' && p !== prod) pass = false;" &
              "if(pass) {" &
                  "var vStr = spans[i].getAttribute('data-valor') || '0';" &
                  "var v = parseFloat(vStr.replace(',', '.')) || 0;" &
                  "var r = spans[i].getAttribute('data-regional');" &
                  "if(soma[r] !== undefined) { soma[r] += v; }" &
                  "soma['Total'] += v;" &
              "}" &
          "}" &
          "return soma;" &
      "}" &
      '''
    
    # We also need to extract everything between start_idx and end_idx to replace it
    old_calcular = dax[start_idx:end_idx]
    dax = dax.replace(old_calcular, new_calcular)

with open(file_path, 'w', encoding='utf8') as f:
    f.write(dax)


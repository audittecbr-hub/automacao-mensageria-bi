import re

filepath = r"C:\Users\cristhofer.maciel.GRUPOSTUDIO\Downloads\honorarios_regionais (2).SemanticModel\definition\tables\medidas_html.tmdl"

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Update calcularSoma function
old_calcular_soma = """			    "function calcularSoma(classe) {" &
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
			      "}" &"""

new_calcular_soma = """			    "function calcularSoma(classe) {" &
			          "var spans = document.getElementsByClassName(classe);" &
			          "var soma = { 'Regional Sul': 0, 'Regional Sudeste': 0, 'Regional Sudeste 2': 0, 'Regional NNCO': 0, 'Total': 0 };" &
			          "var prodBox = document.getElementById('global-produto');" &
			          "var prod = prodBox ? prodBox.value : '';" &
			          "var chkRT = document.getElementById('chkRegraRt');" &
			          "var regraAtiva = chkRT ? chkRT.checked : true;" &
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
			                  "var vStr = '0';" &
			                  "if(regraAtiva && spans[i].hasAttribute('data-valor')) vStr = spans[i].getAttribute('data-valor');" &
			                  "else if(!regraAtiva && spans[i].hasAttribute('data-valor-sr')) vStr = spans[i].getAttribute('data-valor-sr');" &
			                  "else vStr = spans[i].getAttribute('data-valor') || '0';" &
			                  "var v = parseFloat(vStr.replace(',', '.')) || 0;" &
			                  "var r = spans[i].getAttribute('data-regional');" &
			                  "if(soma[r] !== undefined) { soma[r] += v; }" &
			                  "soma['Total'] += v;" &
			              "}" &
			          "}" &
			          "return soma;" &
			      "}" &"""

content = content.replace(old_calcular_soma, new_calcular_soma)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated calcularSoma in JS")

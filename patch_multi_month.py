import re

with open(r'C:\Users\cristhofer.maciel.GRUPOSTUDIO\Desktop\Mockup_Honorarios_Matriz_Corrigido.dax', 'r', encoding='utf8') as f:
    dax = f.read()

# 1. Add _opcoes_meses variable
opcoes_meses_dax = '''
/* GERADOR DAS OPÇÕES PARA O DROPDOWN DE MESES */
VAR _opcoes_meses = 
    CONCATENATEX(
        _datas_meses, 
        "<label class='dropdown-item' style='display:flex; align-items:center; gap:8px; cursor:pointer;'><input type='checkbox' class='mes-checkbox' value='" & [AnoMes] & "' onchange='atualizarMesBtnText(); filtrarTudo();' checked> " & [AnoMes] & "</label>", 
        ""
    )
'''
dax = dax.replace('VAR _opcoes_produtos =', opcoes_meses_dax + '\nVAR _opcoes_produtos =')

# 2. Replace the HTML input for month with a dropdown
old_month_input = '''"<div style='display:flex; align-items:center; background:var(--card); border-radius:12px; border:1px solid rgba(226,179,90,0.2); padding:4px 6px; box-shadow: 0 4px 15px rgba(0,0,0,0.2);'>" &
                     "<div style='padding: 0 10px; font-size:14px; color:var(--accent);'>&#128197;</div>" &
                     "<input type='month' class='header-filter' value='" & _mesAtual & "' style='border:none; background:transparent; color:var(--text-main); font-family:var(--font); font-size:16px; font-weight:500; outline:none; text-transform:uppercase; color-scheme:dark; cursor:pointer; padding:6px;' id='global-mes-ano' onchange='filtrarTudo()'>" &
                  "</div>" &'''

new_month_dropdown = '''"<div class='dropdown-container' style='margin-left:0;'>" &
                     "<button class='dropdown-btn' onclick='toggleMesDropdown()' style='width: 200px;'><span style='color:var(--accent); margin-right:8px;'>&#128197;</span> <span id='mesBtnText'>TODOS (MÊS)</span> <span style='font-size:16px; margin-left:auto;'>&#9660;</span></button>" &
                     "<div class='dropdown-menu' id='mesMenu' style='width: 200px;'>" &
                         "<div class='dropdown-list' style='padding:10px;'>" &
                             "<label class='dropdown-item' style='display:flex; align-items:center; gap:8px; cursor:pointer; border-bottom:1px solid var(--border); padding-bottom:8px; margin-bottom:4px;'><input type='checkbox' id='selectAllMeses' onchange='toggleAllMeses(this); filtrarTudo();' checked> <strong>SELECIONAR TODOS</strong></label>" &
                             _opcoes_meses &
                         "</div>" &
                     "</div>" &
                  "</div>" &'''

if old_month_input in dax:
    dax = dax.replace(old_month_input, new_month_dropdown)
else:
    # Let's use regex if exact match fails
    dax = re.sub(r'"<div style=\'display:flex; align-items:center; background:var\(--card\).*?id=\'global-mes-ano\' onchange=\'filtrarTudo\(\)\'>" &\s*"</div>" &', new_month_dropdown, dax, flags=re.DOTALL)

# 3. Update the JavaScript
# Add JS functions for mes dropdown
js_functions = '''"function toggleMesDropdown() {" &
          "var menu = document.getElementById('mesMenu');" &
          "menu.classList.toggle('show');" &
      "}" &
      "function toggleAllMeses(source) {" &
          "var checkboxes = document.querySelectorAll('.mes-checkbox');" &
          "for(var i=0; i<checkboxes.length; i++) { checkboxes[i].checked = source.checked; }" &
          "atualizarMesBtnText();" &
      "}" &
      "function atualizarMesBtnText() {" &
          "var checkboxes = document.querySelectorAll('.mes-checkbox');" &
          "var checkedBoxes = document.querySelectorAll('.mes-checkbox:checked');" &
          "var btnText = 'TODOS (MÊS)';" &
          "if(checkedBoxes.length === 0) btnText = 'NENHUM MÊS';" &
          "else if(checkedBoxes.length < checkboxes.length) btnText = checkedBoxes.length + ' MESES';" &
          "document.getElementById('mesBtnText').innerText = btnText;" &
          "var allCb = document.getElementById('selectAllMeses');" &
          "if(allCb) allCb.checked = (checkedBoxes.length === checkboxes.length);" &
      "}" &
'''

dax = dax.replace('"function toggleProdDropdown() {" &', js_functions + '\n      "function toggleProdDropdown() {" &')

# Add to document.addEventListener('click')
dax = dax.replace(
    'if (!e.target.closest(\'.dropdown-container\')) {',
    'if (!e.target.closest(\'.dropdown-container\')) {\n              var mesMenu = document.getElementById(\'mesMenu\');\n              if (mesMenu && mesMenu.classList.contains(\'show\')) { mesMenu.classList.remove(\'show\'); }'
)

# Update calcularSoma
old_calcular = '''"function calcularSoma(classe, mesAnoFiltrado) {" &
          "var spans = document.getElementsByClassName(classe);" &
          "var soma = { 'Regional Sul': 0, 'Regional Sudeste': 0, 'Regional Sudeste 2': 0, 'Regional NNCO': 0, 'Total': 0 };" &
          "var prodBox = document.getElementById('global-produto');" &
          "var prod = prodBox ? prodBox.value : '';" &
          "for(var i=0; i<spans.length; i++) {" &
              "var d = spans[i].getAttribute('data-data');" &
              "var pass = true;" &
              "if(mesAnoFiltrado && !d.startsWith(mesAnoFiltrado)) pass = false;" &'''

new_calcular = '''"function calcularSoma(classe) {" &
          "var spans = document.getElementsByClassName(classe);" &
          "var soma = { 'Regional Sul': 0, 'Regional Sudeste': 0, 'Regional Sudeste 2': 0, 'Regional NNCO': 0, 'Total': 0 };" &
          "var prodBox = document.getElementById('global-produto');" &
          "var prod = prodBox ? prodBox.value : '';" &
          "var checkedBoxes = document.querySelectorAll('.mes-checkbox:checked');" &
          "var selectedMeses = [];" &
          "for(var k=0; k<checkedBoxes.length; k++) { selectedMeses.push(checkedBoxes[k].value); }" &
          "for(var i=0; i<spans.length; i++) {" &
              "var d = spans[i].getAttribute('data-data');" &
              "var pass = true;" &
              "if(selectedMeses.indexOf(d) === -1) pass = false;" &'''

# Handle the fact that mesAnoFiltrado might be passed directly
dax = dax.replace(old_calcular, new_calcular)

# Replace all calcularSoma(..., mesAno) with calcularSoma(...)
dax = re.sub(r'calcularSoma\(([^,]+),\s*mesAno\)', r'calcularSoma(\1)', dax)

# Remove the var mesAno = ... line from filtrarTudo
dax = re.sub(r'"var mesAno = document\.getElementById\(\'global-mes-ano\'\)\.value;" &\s*', '', dax)

with open(r'C:\Users\cristhofer.maciel.GRUPOSTUDIO\Desktop\Mockup_Honorarios_Matriz_Corrigido.dax', 'w', encoding='utf8') as f:
    f.write(dax)

import re

file_path = r'C:\Users\cristhofer.maciel.GRUPOSTUDIO\Desktop\HTML_Detalhamento_Aprovados_Corrigido.dax'
with open(file_path, 'r', encoding='utf8') as f:
    dax = f.read()

# 1. Add upper limit filter to DATA_RT
old_filter = 'FILTER(vw_powerbi_relatorio_aprovacao, [Honorários aprovados] > 0 && vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026, 6, 12))'
new_filter = 'FILTER(vw_powerbi_relatorio_aprovacao, [Honorários aprovados] > 0 && vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026, 6, 12) && vw_powerbi_relatorio_aprovacao[DATA_RT] <= DATE(2026, 12, 31))'
dax = dax.replace(old_filter, new_filter)

# 2. Add CSS
css_to_add = '''
/* DROPDOWN CUSTOMIZADO */
.dropdown-container { position: relative; display: inline-flex; align-items: center; width: 100%; font-weight: normal; }
.dropdown-btn { background: rgba(0,0,0,0.2); border: 1px solid var(--border); border-radius: 6px; color: var(--text-main); font-family: var(--font); font-size: 13px; cursor: pointer; padding: 6px; display: flex; align-items: center; justify-content: space-between; width: 100%; outline: none; transition: 0.2s; margin-top: 4px; }
.dropdown-btn:hover { border-color: var(--accent); }
.dropdown-menu { display: none; position: absolute; top: calc(100% + 5px); left: 0; width: 220px; background: var(--bg-card); border: 1px solid var(--border); border-radius: 8px; box-shadow: 0 10px 30px rgba(0,0,0,0.6); z-index: 9999; flex-direction: column; font-weight: normal; text-transform: none; }
.dropdown-menu.show { display: flex; }
.dropdown-list { max-height: 200px; overflow-y: auto; display: flex; flex-direction: column; padding: 10px; }
.dropdown-item { padding: 6px 10px; font-size: 14px; color: var(--text-main); cursor: pointer; transition: 0.2s; border-radius: 4px; }
.dropdown-item:hover { background: rgba(255,255,255,0.05); }
'''
dax = dax.replace('</style>', css_to_add + '\n</style>')

# 3. Add DAX variables for months
dax_vars = '''
VAR _datas_meses = DISTINCT(SELECTCOLUMNS(FILTER(Calendario, Calendario[Date] >= DATE(2026, 6, 1) && Calendario[Date] <= DATE(2026, 12, 31)), "AnoMes", FORMAT(Calendario[Date], "yyyy-MM")))
VAR _opcoes_meses_rt = 
    CONCATENATEX(
        _datas_meses, 
        "<label class='dropdown-item' style='display:flex; align-items:center; gap:8px;'><input type='checkbox' class='mes-rt-cb' value='" & [AnoMes] & "' onchange='atualizarMesBtnText(\\"rt\\"); filtrarTabela();' checked> " & [AnoMes] & "</label>", 
        "",
        [AnoMes], ASC
    )
VAR _opcoes_meses_mov = 
    CONCATENATEX(
        _datas_meses, 
        "<label class='dropdown-item' style='display:flex; align-items:center; gap:8px;'><input type='checkbox' class='mes-mov-cb' value='" & [AnoMes] & "' onchange='atualizarMesBtnText(\\"mov\\"); filtrarTabela();' checked> " & [AnoMes] & "</label>", 
        "",
        [AnoMes], ASC
    )
'''
dax = dax.replace('VAR _linhas_aprovados =', dax_vars + '\nVAR _linhas_aprovados =')

# 4. Replace TH HTML
old_th_rt = "<th><span>Data_RT</span><br><input type='date' id='buscaColData' class='col-filter' onchange='filtrarTabela()'></th>"
new_th_rt = '''"<th><span>Data_RT</span><br>" &
               "<div class='dropdown-container'>" &
                 "<button class='dropdown-btn' onclick='toggleDropdown(\\"rtMenu\\")'><span id='rtBtnText'>TODOS</span> <span>&#9660;</span></button>" &
                 "<div class='dropdown-menu' id='rtMenu'>" &
                   "<div class='dropdown-list'>" &
                     "<label class='dropdown-item' style='display:flex; align-items:center; gap:8px; border-bottom:1px solid var(--border); padding-bottom:8px; margin-bottom:4px;'><input type='checkbox' id='selectAllRt' onchange='toggleAll(\\"rt\\", this); filtrarTabela();' checked> <strong>TODOS</strong></label>" &
                     _opcoes_meses_rt &
                   "</div>" &
                 "</div>" &
               "</div></th>"'''
dax = dax.replace(old_th_rt, new_th_rt)

old_th_mov = "<th><span>Data_Mov</span><br><input type='date' id='buscaColDataMov' class='col-filter' onchange='filtrarTabela()'></th>"
new_th_mov = '''"<th><span>Data_Mov</span><br>" &
               "<div class='dropdown-container'>" &
                 "<button class='dropdown-btn' onclick='toggleDropdown(\\"movMenu\\")'><span id='movBtnText'>TODOS</span> <span>&#9660;</span></button>" &
                 "<div class='dropdown-menu' id='movMenu'>" &
                   "<div class='dropdown-list'>" &
                     "<label class='dropdown-item' style='display:flex; align-items:center; gap:8px; border-bottom:1px solid var(--border); padding-bottom:8px; margin-bottom:4px;'><input type='checkbox' id='selectAllMov' onchange='toggleAll(\\"mov\\", this); filtrarTabela();' checked> <strong>TODOS</strong></label>" &
                     _opcoes_meses_mov &
                   "</div>" &
                 "</div>" &
               "</div></th>"'''
dax = dax.replace(old_th_mov, new_th_mov)

# 5. Add JS functions
js_funcs = '''"function toggleDropdown(id) {" &
    "var m = document.getElementById(id);" &
    "if(m.classList.contains('show')) m.classList.remove('show'); else { document.querySelectorAll('.dropdown-menu').forEach(el=>el.classList.remove('show')); m.classList.add('show'); }" &
"}" &
"function toggleAll(tipo, source) {" &
    "var cbs = document.querySelectorAll('.mes-' + tipo + '-cb');" &
    "cbs.forEach(cb => cb.checked = source.checked);" &
    "atualizarMesBtnText(tipo);" &
"}" &
"function atualizarMesBtnText(tipo) {" &
    "var cbs = document.querySelectorAll('.mes-' + tipo + '-cb');" &
    "var checked = document.querySelectorAll('.mes-' + tipo + '-cb:checked');" &
    "var btnText = 'TODOS';" &
    "if(checked.length === 0) btnText = 'NENHUM';" &
    "else if(checked.length < cbs.length) btnText = checked.length + ' MESES';" &
    "document.getElementById(tipo + 'BtnText').innerText = btnText;" &
    "var allCb = document.getElementById('selectAll' + (tipo === 'rt' ? 'Rt' : 'Mov'));" &
    "if(allCb) allCb.checked = (checked.length === cbs.length);" &
"}" &
"document.addEventListener('click', function(e) {" &
    "if (!e.target.closest('.dropdown-container')) {" &
        "document.querySelectorAll('.dropdown-menu').forEach(el=>el.classList.remove('show'));" &
    "}" &
"});" &
'''
dax = dax.replace('function popularProdutos() {', js_funcs + '\nfunction popularProdutos() {')

# 6. Update filtrarTabela
# Remove the old date input logic
dax = re.sub(r"var eD = document\.getElementById\('buscaColData'\); var qD = eD \? eD\.value\.trim\(\) : '';", '', dax)
dax = re.sub(r"var eDM = document\.getElementById\('buscaColDataMov'\); var qDM = eDM \? eDM\.value\.trim\(\) : '';", '', dax)

# Add reading selected checkboxes
new_selected_reading = '''
    var selRtNodes = document.querySelectorAll('.mes-rt-cb:checked');
    var selRt = {}; selRtNodes.forEach(n => selRt[n.value] = true);
    var selMovNodes = document.querySelectorAll('.mes-mov-cb:checked');
    var selMov = {}; selMovNodes.forEach(n => selMov[n.value] = true);
'''
dax = dax.replace("var rows = document.querySelectorAll('.linha-detalhe');", new_selected_reading + "\n    var rows = document.querySelectorAll('.linha-detalhe');")

# Replace matchD and matchDM inside loop
old_match = '''        var dtRtStr = rows[i].getAttribute('data-rt');
        var dtMovStr = rows[i].getAttribute('data-mov');
        var matchD = (qD === '' || dtRtStr === qD);
        var matchDM = (qDM === '' || dtMovStr === qDM);'''
new_match = '''        var dtRtStr = rows[i].getAttribute('data-rt').substring(0, 7);
        var dtMovStr = rows[i].getAttribute('data-mov').substring(0, 7);
        var matchD = selRt[dtRtStr] ? true : false;
        var matchDM = selMov[dtMovStr] ? true : false;'''
dax = dax.replace(old_match, new_match)

with open(file_path, 'w', encoding='utf8') as f:
    f.write(dax)


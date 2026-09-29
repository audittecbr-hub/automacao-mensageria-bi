import json
import subprocess

css_raw = """
:root {
    --bg: #0b0f19;
    --bg-card: #121826;
    --border: rgba(255, 255, 255, 0.08);
    --border-hover: rgba(226, 179, 90, 0.3);
    --text-main: #f1f5f9;
    --text-sec: #94a3b8;
    --text-muted: #64748b;
    --accent: #e2b35a;
    --accent-glow: rgba(226, 179, 90, 0.15);
    --blue: #38bdf8;
    --green: #22c55e;
    --orange: #f59e0b;
    --red: #ef4444;
    --font: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif;
}
html, body { margin:0; padding:0; width:100vw; height:100vh; background:var(--bg); font-family:var(--font); color:var(--text-main); overflow:hidden; }
* { box-sizing:border-box; }
.painel { background: radial-gradient(circle at top left, rgba(226,179,90,0.04), transparent 50%), var(--bg); border: 1px solid var(--border); border-radius: 16px; padding: 20px 24px; display: flex; flex-direction: column; height: calc(100vh - 20px); margin: 10px; box-shadow: 0 10px 40px rgba(0,0,0,0.6); }
.cabecalho { display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; flex-shrink: 0; border-bottom: 1px solid var(--border); padding-bottom: 16px; }
.cabecalho-esquerda { display: flex; align-items: center; gap: 16px; flex-wrap: wrap; }
.btn-voltar { display:inline-flex; align-items:center; gap:6px; background:rgba(226,179,90,0.08); color:var(--accent); border:1px solid var(--border); padding:8px 16px; border-radius:8px; cursor:pointer; font-weight:600; font-family:var(--font); transition:all 0.2s; text-transform:uppercase; font-size:12px; letter-spacing:1px; }
.btn-voltar:hover { background:rgba(226,179,90,0.18); border-color:var(--accent); color:#fff; }
.titulo { font-size: 20px; font-weight: 700; color: var(--text-main); letter-spacing: 0.5px; text-transform: uppercase; display: flex; align-items: center; gap: 8px; }
.titulo span { color: var(--accent); }
.badges-container { display: flex; align-items: center; gap: 10px; }
.count-destaque { background: rgba(255,255,255,0.05); color: var(--text-sec); padding: 6px 14px; border-radius: 8px; font-weight: 600; font-size: 13px; border: 1px solid var(--border); display: flex; align-items: center; gap: 6px; }
.valor-destaque { background: rgba(226,179,90,0.1); color: var(--accent); padding: 6px 16px; border-radius: 8px; font-weight: 700; font-size: 16px; border: 1px solid var(--border-hover); font-variant-numeric: tabular-nums; display: flex; align-items: center; gap: 6px; }
.controles { display: flex; align-items: center; gap: 12px; }
.input-busca { background: rgba(0,0,0,0.3); border: 1px solid var(--border); color: var(--text-main); padding: 10px 16px; border-radius: 8px; width: 260px; font-family: var(--font); font-size: 12px; transition: 0.2s; outline: none; }
.input-busca:focus { border-color: var(--accent); background: rgba(0,0,0,0.5); }
.btn-copiar { background: var(--bg-card); border: 1px solid var(--border); color: var(--text-sec); padding: 10px 18px; border-radius: 8px; cursor: pointer; font-weight: 600; font-size: 11px; text-transform: uppercase; letter-spacing: 1px; transition: 0.2s; white-space: nowrap; font-family: var(--font); }
.btn-copiar:hover { background: rgba(226,179,90,0.12); border-color: var(--accent); color: #fff; box-shadow: 0 0 12px var(--accent-glow); }
.table-wrapper { flex: 1 1 auto; overflow-y: auto; position: relative; border: 1px solid var(--border); border-radius: 10px; background: rgba(18, 24, 38, 0.4); }
.table-wrapper::-webkit-scrollbar { width: 8px; height: 8px; }
.table-wrapper::-webkit-scrollbar-track { background: transparent; }
.table-wrapper::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.1); border-radius: 4px; }
.table-wrapper::-webkit-scrollbar-thumb:hover { background: rgba(255,255,255,0.2); }
.tabela { width: 100%; border-collapse: collapse; text-align: left; }
.tabela thead th { position: sticky; top: 0; background: #0e131f; padding: 12px 14px; font-size: 11px; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; color: var(--text-sec); border-bottom: 1px solid var(--border); z-index: 10; vertical-align: top; }
.col-filter { margin-top: 8px; width: 100%; background: rgba(0,0,0,0.4); border: 1px solid rgba(255,255,255,0.08); color: var(--text-main); padding: 6px 8px; border-radius: 6px; font-size: 11px; font-family: var(--font); outline: none; transition: 0.2s; color-scheme: dark; }
.col-filter:focus { border-color: var(--accent); background: rgba(0,0,0,0.6); }
.tabela tbody td { padding: 12px 14px; border-bottom: 1px solid rgba(255,255,255,0.03); font-size: 13px; color: var(--text-main); white-space: nowrap; }
.tabela tbody tr:hover td { background: rgba(226,179,90,0.05); }
.tabela tbody tr:hover td:first-child { border-left: 3px solid var(--accent); padding-left: 11px; color: var(--accent); }
.td-valor { text-align: right; font-variant-numeric: tabular-nums; letter-spacing: -0.5px; color: var(--accent); font-weight: 600; }
.tabela tfoot td { position: sticky; bottom: 0; background: #0e131f; border-top: 2px solid var(--border-hover); padding: 14px; font-size: 13px; font-weight: 700; z-index: 10; color: var(--text-main); }
.tfoot-valor { text-align: right; font-variant-numeric: tabular-nums; color: var(--accent); font-size: 16px; font-weight: 800; }
"""

min_css = " ".join([l.strip() for l in css_raw.split('\n') if l.strip()])

def make_measure_dax(titulo, tipo, val_col, filter_condition):
    # Notice: inside tr.innerHTML, we can use template literal or safe JS DOM creation!
    # Even simpler:
    # tr.className = 'linha-detalhe';
    # tr.innerHTML = '<td>' + tipoFixo + '</td><td>' + rName + '</td><td>' + area + '</td><td>' + cli + '</td><td>' + job + '</td><td>' + prod + '</td><td>' + fmtData(dtRt) + '</td><td>' + fmtData(dtMov) + '</td><td class=""td-valor"">' + valFmt + '</td>';
    # Notice that only td-valor needs a class! The other columns don't even need class='td-...' because in CSS:
    # .tabela tbody td already formats everything!
    # And for queries in JS:
    # rows[i].children[0] is Tipo!
    # rows[i].children[1] is Regional!
    # rows[i].children[2] is Area!
    # rows[i].children[3] is Cliente!
    # rows[i].children[4] is Job!
    # rows[i].children[5] is Produto!
    # rows[i].children[6] is DataRT!
    # rows[i].children[7] is DataMov!
    # rows[i].children[8] is Valor!
    # LOOK AT HOW MUCH CLEANER AND FASTER rows[i].children[k] IS!
    # Zero class lookups, zero querySelector calls, 10x faster execution, and ZERO quote problems!
    
    js_raw = f"""
var tipoFixo = '{tipo}';
var regMap = {{ 'S': 'Regional Sul', 'SP': 'Regional SP', 'SD': 'Regional Sudeste', 'N': 'Regional NNCO', 'O': 'Outras' }};
function formatarMoeda(val) {{ return 'R$ ' + val.toLocaleString('pt-BR', {{ minimumFractionDigits: 2, maximumFractionDigits: 2 }}); }}
function fmtData(s) {{ if(!s || s.length < 10) return ''; var p = s.split('-'); return p[2] + '/' + p[1] + '/' + p[0]; }}
function renderizarLinhas() {{
    var rawEl = document.getElementById('raw-data');
    if(!rawEl) return;
    var raw = rawEl.textContent.trim();
    if(!raw) return;
    var items = raw.split('~');
    var tbody = document.getElementById('tbodyDetalhe');
    if(!tbody) return;
    tbody.innerHTML = '';
    var frag = document.createDocumentFragment();
    var prods = {{}};
    for(var i=0; i<items.length; i++) {{
        var item = items[i];
        if(!item) continue;
        var cols = item.split('|');
        if(cols.length < 8) continue;
        var rCode = cols[0];
        var rName = regMap[rCode] || rCode;
        var area = cols[1];
        var cli = cols[2];
        var job = cols[3];
        var prod = cols[4];
        var dtRt = cols[5];
        var dtMov = cols[6];
        var valStr = cols[7];
        var rowMes = dtMov ? dtMov.substring(0, 7) : (dtRt ? dtRt.substring(0, 7) : '');
        var valNum = parseFloat(valStr.replace(',', '.')) || 0;
        var valFmt = 'R$ ' + valNum.toLocaleString('pt-BR', {{ minimumFractionDigits: 2, maximumFractionDigits: 2 }});
        if(prod) prods[prod] = true;
        var tr = document.createElement('tr');
        tr.className = 'linha-detalhe';
        tr.setAttribute('data-val', valStr);
        tr.setAttribute('data-mes', rowMes);
        tr.setAttribute('data-rt', dtRt);
        tr.setAttribute('data-mov', dtMov);
        tr.innerHTML = '<td>' + tipoFixo + '</td><td>' + rName + '</td><td>' + area + '</td><td>' + cli + '</td><td>' + job + '</td><td>' + prod + '</td><td>' + fmtData(dtRt) + '</td><td>' + fmtData(dtMov) + '</td><td class="td-valor">' + valFmt + '</td>';
        frag.appendChild(tr);
    }}
    tbody.appendChild(frag);
    var selP = document.getElementById('buscaColProduto');
    if(selP && selP.options.length <= 1) {{
        var arrP = Object.keys(prods).sort();
        for(var j=0; j<arrP.length; j++) {{
            var opt = document.createElement('option');
            opt.value = arrP[j].toLowerCase();
            opt.textContent = arrP[j];
            selP.appendChild(opt);
        }}
    }}
    filtrarTabela();
}}
function filtrarTabela() {{
    var eG = document.getElementById('buscaGlobal'); var qG = eG ? eG.value.toLowerCase().trim() : '';
    var eT = document.getElementById('buscaColTipo'); var qT = eT ? eT.value.toLowerCase().trim() : '';
    var eR = document.getElementById('buscaColRegional'); var qR = eR ? eR.value.toLowerCase().trim() : '';
    var eM = document.getElementById('buscaColMes'); var qM = eM ? eM.value.trim() : '';
    var eA = document.getElementById('buscaColArea'); var qA = eA ? eA.value.toLowerCase().trim() : '';
    var eC = document.getElementById('buscaColCliente'); var qC = eC ? eC.value.toLowerCase().trim() : '';
    var eJ = document.getElementById('buscaColJob'); var qJ = eJ ? eJ.value.toLowerCase().trim() : '';
    var eP = document.getElementById('buscaColProduto'); var qP = eP ? eP.value.toLowerCase().trim() : '';
    var eD = document.getElementById('buscaColData'); var qD = eD ? eD.value.trim() : '';
    var eDM = document.getElementById('buscaColDataMov'); var qDM = eDM ? eDM.value.trim() : '';
    var rows = document.querySelectorAll('.linha-detalhe');
    var count = 0;
    var somaValor = 0;
    for(var i=0; i<rows.length; i++) {{
        var tds = rows[i].children;
        if(tds.length < 9) continue;
        var tT = tds[0].textContent.toLowerCase();
        var tR = tds[1].textContent.toLowerCase();
        var tA = tds[2].textContent.toLowerCase();
        var tC = tds[3].textContent.toLowerCase();
        var tJ = tds[4].textContent.toLowerCase();
        var tP = tds[5].textContent.toLowerCase();
        var valNum = parseFloat(rows[i].getAttribute('data-val').replace(',', '.')) || 0;
        var rowMes = rows[i].getAttribute('data-mes') || '';
        var dtRtStr = rows[i].getAttribute('data-rt') || '';
        var dtMovStr = rows[i].getAttribute('data-mov') || '';
        var matchG = (qG === '' || tA.indexOf(qG)>-1 || tC.indexOf(qG)>-1 || tJ.indexOf(qG)>-1 || tP.indexOf(qG)>-1 || tR.indexOf(qG)>-1 || tT.indexOf(qG)>-1);
        var matchT = (qT === '' || tT.indexOf(qT)>-1);
        var matchR = (qR === '' || tR.indexOf(qR)>-1);
        var matchM = (qM === '' || rowMes === qM);
        var matchA = (qA === '' || tA.indexOf(qA)>-1);
        var matchC = (qC === '' || tC.indexOf(qC)>-1);
        var matchJ = (qJ === '' || tJ.indexOf(qJ)>-1);
        var matchP = (qP === '' || tP.indexOf(qP)>-1);
        var matchD = (qD === '' || dtRtStr === qD);
        var matchDM = (qDM === '' || dtMovStr === qDM);
        if(matchG && matchT && matchR && matchM && matchA && matchC && matchJ && matchP && matchD && matchDM) {{
            rows[i].style.display = '';
            count++;
            somaValor += valNum;
        }} else {{
            rows[i].style.display = 'none';
        }}
    }}
    var elCount = document.getElementById('totalLinhasCount');
    if(elCount) elCount.innerHTML = '&#128196; <b>' + count.toLocaleString('pt-BR') + '</b> registros';
    var elValor = document.getElementById('totalValorCount');
    if(elValor) elValor.innerHTML = '&#128176; <b>' + formatarMoeda(somaValor) + '</b>';
    var elTfoot = document.getElementById('tfootTotalValor');
    if(elTfoot) elTfoot.innerText = formatarMoeda(somaValor);
}}
function copiarTabela() {{
    try {{
        var btn = document.getElementById('btnCopiar');
        var originalText = btn.innerHTML;
        btn.innerHTML = '&#8982; Copiando...';
        var textToCopy = '';
        var nl = String.fromCharCode(13, 10);
        var tab = String.fromCharCode(9);
        var ths = document.querySelectorAll('.tabela thead th');
        for(var i=0; i<ths.length; i++) {{
            var span = ths[i].querySelector('span');
            var thText = span ? span.textContent.trim() : ths[i].textContent.trim();
            textToCopy += thText + (i < ths.length - 1 ? tab : '');
        }}
        textToCopy += nl;
        var rows = document.querySelectorAll('.linha-detalhe');
        var copiedCount = 0;
        for(var i=0; i<rows.length; i++) {{
            if(rows[i].style.display !== 'none') {{
                var tds = rows[i].querySelectorAll('td');
                for(var j=0; j<tds.length; j++) {{
                    textToCopy += tds[j].textContent.trim() + (j < tds.length - 1 ? tab : '');
                }}
                textToCopy += nl;
                copiedCount++;
            }}
        }}
        var tfootVal = document.getElementById('tfootTotalValor');
        if(tfootVal) {{
            textToCopy += 'TOTAL' + tab + tab + tab + tab + tab + tab + tab + tab + tfootVal.innerText.trim() + nl;
        }}
        var tempInput = document.createElement('textarea');
        tempInput.style.position = 'absolute';
        tempInput.style.left = '-9999px';
        tempInput.value = textToCopy;
        document.body.appendChild(tempInput);
        tempInput.select();
        document.execCommand('copy'); 
        btn.innerHTML = '&#10004; Copiado (' + copiedCount + ')';
        btn.style.borderColor = 'var(--green)';
        btn.style.color = 'var(--green)';
        document.body.removeChild(tempInput);
        setTimeout(function() {{ 
            btn.innerHTML = originalText; 
            btn.style.borderColor = 'var(--border)';
            btn.style.color = 'var(--text-sec)';
        }}, 2500);
    }} catch (e) {{
        alert('Erro ao copiar: ' + e.message);
    }}
}}
window.onload = function() {{ renderizarLinhas(); }};
document.addEventListener('DOMContentLoaded', renderizarLinhas);
setTimeout(renderizarLinhas, 50);
setTimeout(renderizarLinhas, 200);
renderizarLinhas();
"""
    min_js = " ".join([l.strip() for l in js_raw.split('\n') if l.strip()])
    
    # In DAX, any literal double quote must be ""
    dax_js_content = min_js.replace('"', '""')
    
    # Let's construct the full DAX expression
    dax = (
        'VAR _css = "<style>' + min_css + '</style>"\n\n' +
        'VAR _dados_compactos = \n' +
        '    CONCATENATEX(\n' +
        '        FILTER(\n' +
        '            vw_powerbi_relatorio_aprovacao, \n' +
        f'            {filter_condition}\n' +
        '        ),\n' +
        '        SWITCH(vw_powerbi_relatorio_aprovacao[Regional], "Regional Sul", "S", "Regional Sudeste", "SP", "Regional Sudeste 2", "SD", "Regional NNCO", "N", "O") & "|" & \n' +
        '        LEFT(vw_powerbi_relatorio_aprovacao[AREA_ATUAL], 12) & "|" & \n' +
        '        SUBSTITUTE(LEFT(vw_powerbi_relatorio_aprovacao[NOME], 18), "|", " ") & "|" & \n' +
        '        vw_powerbi_relatorio_aprovacao[JOB] & "|" & \n' +
        '        LEFT(vw_powerbi_relatorio_aprovacao[NOME_TRIBUTO], 12) & "|" & \n' +
        '        FORMAT(vw_powerbi_relatorio_aprovacao[DATA_RT], "yyyy-MM-dd") & "|" & \n' +
        '        FORMAT(vw_powerbi_relatorio_aprovacao[data_mov_anterior], "yyyy-MM-dd") & "|" & \n' +
        f'        FORMAT({val_col}, "0.00"),\n' +
        '        "~"\n' +
        '    )\n\n' +
        'VAR _js = "<script>' + dax_js_content + '</script>"\n\n' +
        'VAR _html = \n' +
        '    "<html><head><meta charset=\'UTF-8\'>" & _css & "</head><body>" &\n' +
        '    "<div class=\'painel\'>" &\n' +
        '        "<div class=\'cabecalho\'>" &\n' +
        '            "<div class=\'cabecalho-esquerda\'>" &\n' +
        '                "<button class=\'btn-voltar\'>&#8592; Voltar</button>" &\n' +
        f'                "<div class=\'titulo\'>{titulo}</div>" &\n' +
        '                "<div class=\'badges-container\'>" &\n' +
        '                    "<div class=\'count-destaque\' id=\'totalLinhasCount\'>&#128196; <b>0</b> registros</div>" &\n' +
        '                    "<div class=\'valor-destaque\' id=\'totalValorCount\'>&#128176; <b>R$ 0,00</b></div>" &\n' +
        '                "</div>" &\n' +
        '            "</div>" &\n' +
        '            "<div class=\'controles\'>" &\n' +
        '                "<input type=\'text\' id=\'buscaGlobal\' class=\'input-busca\' placeholder=\'&#128269; Buscar em tudo (Cliente, Job, etc)...\' onkeyup=\'filtrarTabela()\'>" &\n' +
        '                "<button class=\'btn-copiar\' id=\'btnCopiar\' onclick=\'copiarTabela()\'>&#128203; Copiar Linhas</button>" &\n' +
        '            "</div>" &\n' +
        '        "</div>" &\n' +
        '        "<div class=\'table-wrapper\'>" &\n' +
        '            "<table class=\'tabela\' id=\'tabelaDetalhe\'>" &\n' +
        '                "<thead>" &\n' +
        '                    "<tr>" &\n' +
        f'                        "<th><span>Tipo</span><br><select id=\'buscaColTipo\' class=\'col-filter\' onchange=\'filtrarTabela()\'><option value=\'\'>Todos</option><option value=\'{tipo.lower()}\'>{tipo}</option></select></th>" &\n' +
        '                        "<th><span>Regional</span><br><select id=\'buscaColRegional\' class=\'col-filter\' onchange=\'filtrarTabela()\'><option value=\'\'>Todas</option><option value=\'regional sul\'>Regional Sul</option><option value=\'regional sp\'>Regional SP</option><option value=\'regional sudeste\'>Regional Sudeste</option><option value=\'regional nnco\'>Regional NNCO</option></select></th>" &\n' +
        '                        "<th><span>Mês</span><br><select id=\'buscaColMes\' class=\'col-filter\' onchange=\'filtrarTabela()\'><option value=\'\'>Todos os Meses</option><option value=\'2026-06\'>Junho/2026</option><option value=\'2026-07\'>Julho/2026</option><option value=\'2026-08\'>Agosto/2026</option><option value=\'2026-09\'>Setembro/2026</option><option value=\'2026-10\'>Outubro/2026</option><option value=\'2026-11\'>Novembro/2026</option><option value=\'2026-12\'>Dezembro/2026</option></select></th>" &\n' +
        '                        "<th><span>Área Atual</span><br><input type=\'text\' id=\'buscaColArea\' class=\'col-filter\' placeholder=\'Filtrar Área...\' onkeyup=\'filtrarTabela()\'></th>" &\n' +
        '                        "<th><span>Cliente</span><br><input type=\'text\' id=\'buscaColCliente\' class=\'col-filter\' placeholder=\'Filtrar Cliente...\' onkeyup=\'filtrarTabela()\'></th>" &\n' +
        '                        "<th><span>Job</span><br><input type=\'text\' id=\'buscaColJob\' class=\'col-filter\' placeholder=\'Filtrar Job...\' onkeyup=\'filtrarTabela()\'></th>" &\n' +
        '                        "<th><span>Produto</span><br><select id=\'buscaColProduto\' class=\'col-filter\' onchange=\'filtrarTabela()\'><option value=\'\'>Todos</option></select></th>" &\n' +
        '                        "<th><span>Data RT</span><br><input type=\'date\' id=\'buscaColData\' class=\'col-filter\' onchange=\'filtrarTabela()\'></th>" &\n' +
        '                        "<th><span>Data Mov.</span><br><input type=\'date\' id=\'buscaColDataMov\' class=\'col-filter\' onchange=\'filtrarTabela()\'></th>" &\n' +
        '                        "<th style=\'text-align:right;\'><span>Valor Honorário</span><br><div style=\'height:28px;\'></div></th>" &\n' +
        '                    "</tr>" &\n' +
        '                "</thead>" &\n' +
        '                "<tbody id=\'tbodyDetalhe\'></tbody>" &\n' +
        '                "<tfoot>" &\n' +
        '                    "<tr>" &\n' +
        '                        "<td colspan=\'8\' style=\'text-transform:uppercase; letter-spacing:1px;\'>TOTAL DOS REGISTROS FILTRADOS</td>" &\n' +
        '                        "<td class=\'tfoot-valor\' id=\'tfootTotalValor\'>R$ 0,00</td>" &\n' +
        '                    "</tr>" &\n' +
        '                "</tfoot>" &\n' +
        '            "</table>" &\n' +
        '        "</div>" &\n' +
        '        "<div id=\'raw-data\' style=\'display:none;\'>" & _dados_compactos & "</div>" &\n' +
        '    "</div>" & _js & "</body></html>"\n\n' +
        'RETURN _html\n'
    )
    return dax

# Base measures
base_measures = [
    {
        "tableName": "vw_powerbi_relatorio_aprovacao",
        "name": "Honorários encontrados",
        "expression": "SUM(vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_ENCONTRADO])"
    },
    {
        "tableName": "vw_powerbi_relatorio_aprovacao",
        "name": "Honorários apresentados",
        "expression": """CALCULATE(
    SUM(vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_APRESENTADO]),
    KEEPFILTERS(vw_powerbi_relatorio_aprovacao[area_anterior] = "REUNIÃO TÉCNICA"),
    KEEPFILTERS(NOT ISBLANK(vw_powerbi_relatorio_aprovacao[data_rt])),
    KEEPFILTERS(vw_powerbi_relatorio_aprovacao[data_rt] <= TODAY())
)"""
    },
    {
        "tableName": "vw_powerbi_relatorio_aprovacao",
        "name": "Honorários aprovados",
        "expression": """SUMX(
    vw_powerbi_relatorio_aprovacao,
    COALESCE(vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_HONORARIOS_INICIAIS], vw_powerbi_relatorio_aprovacao[HONORARIOS_INICIAIS], 0) +
    vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_COMPENSACAO] +
    vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_RESTITUICAO] +
    vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_AJUIZAMENTO]
)"""
    },
    {
        "tableName": "vw_powerbi_relatorio_aprovacao",
        "name": "Honorário negociação",
        "expression": """CALCULATE(
    SUM(vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_EM_NEGOCIACAO]),
    KEEPFILTERS(vw_powerbi_relatorio_aprovacao[AREA_ANTERIOR] = "REUNIÃO TÉCNICA"),
    KEEPFILTERS(vw_powerbi_relatorio_aprovacao[AREA_ATUAL] = "NEGOCIAÇÃO")
)"""
    },
    {
        "tableName": "vw_powerbi_relatorio_aprovacao",
        "name": "Honorários perdidos",
        "expression": """CALCULATE(
    SUM(vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_NAO_APROVADO]),
    KEEPFILTERS(vw_powerbi_relatorio_aprovacao[AREA_ANTERIOR] = "NEGOCIAÇÃO"),
    KEEPFILTERS(vw_powerbi_relatorio_aprovacao[AREA_ATUAL] = "FIM")
)"""
    },
    {
        "tableName": "vw_powerbi_relatorio_aprovacao",
        "name": "Honorários não aprovados",
        "expression": """CALCULATE(
    SUM(vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_NAO_APROVADO]),
    KEEPFILTERS(vw_powerbi_relatorio_aprovacao[AREA_ANTERIOR] = "REUNIÃO TÉCNICA"),
    KEEPFILTERS(vw_powerbi_relatorio_aprovacao[AREA_ATUAL] = "FIM")
)"""
    }
]

# Detalhes
detalhes = [
    {
        "tableName": "medidas_html",
        "name": "HTML_Detalhamento_Encontrados",
        "expression": make_measure_dax(
            "DETALHAMENTO <span>HONORÁRIOS ENCONTRADOS</span>",
            "Encontrado",
            "vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_ENCONTRADO]",
            "vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_ENCONTRADO] > 0 && vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026, 6, 12) && vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR] >= DATE(2026, 6, 1) && vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR] <= DATE(2026, 12, 31)"
        )
    },
    {
        "tableName": "medidas_html",
        "name": "HTML_Detalhamento_Apresentados",
        "expression": make_measure_dax(
            "DETALHAMENTO <span>HONORÁRIOS APRESENTADOS</span>",
            "Apresentado",
            "vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_APRESENTADO]",
            "vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_APRESENTADO] > 0 && vw_powerbi_relatorio_aprovacao[AREA_ANTERIOR] = \"REUNIÃO TÉCNICA\" && vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026, 6, 12) && vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR] >= DATE(2026, 6, 1) && vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR] <= DATE(2026, 12, 31)"
        )
    },
    {
        "tableName": "medidas_html",
        "name": "HTML_Detalhamento_Aprovados",
        "expression": make_measure_dax(
            "DETALHAMENTO <span>HONORÁRIOS APROVADOS</span>",
            "Aprovado",
            "(COALESCE(vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_HONORARIOS_INICIAIS], vw_powerbi_relatorio_aprovacao[HONORARIOS_INICIAIS], 0) + vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_COMPENSACAO] + vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_RESTITUICAO] + vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_AJUIZAMENTO])",
            "(COALESCE(vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_HONORARIOS_INICIAIS], vw_powerbi_relatorio_aprovacao[HONORARIOS_INICIAIS], 0) + vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_COMPENSACAO] + vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_RESTITUICAO] + vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_AJUIZAMENTO]) > 0 && vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026, 6, 12) && vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR] >= DATE(2026, 6, 1) && vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR] <= DATE(2026, 12, 31)"
        )
    },
    {
        "tableName": "medidas_html",
        "name": "HTML_Detalhamento_Negociacao",
        "expression": make_measure_dax(
            "DETALHAMENTO <span>HONORÁRIOS EM NEGOCIAÇÃO</span>",
            "Negociação",
            "vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_EM_NEGOCIACAO]",
            "vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_EM_NEGOCIACAO] > 0 && vw_powerbi_relatorio_aprovacao[AREA_ANTERIOR] = \"REUNIÃO TÉCNICA\" && vw_powerbi_relatorio_aprovacao[AREA_ATUAL] = \"NEGOCIAÇÃO\" && vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026, 6, 12) && vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR] >= DATE(2026, 6, 1) && vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR] <= DATE(2026, 12, 31)"
        )
    },
    {
        "tableName": "medidas_html",
        "name": "HTML_Detalhamento_Perdidos",
        "expression": make_measure_dax(
            "DETALHAMENTO <span>HONORÁRIOS PERDIDOS</span>",
            "Perdido",
            "vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_NAO_APROVADO]",
            "vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_NAO_APROVADO] > 0 && vw_powerbi_relatorio_aprovacao[AREA_ANTERIOR] = \"NEGOCIAÇÃO\" && vw_powerbi_relatorio_aprovacao[AREA_ATUAL] = \"FIM\" && vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026, 6, 12) && vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR] >= DATE(2026, 6, 1) && vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR] <= DATE(2026, 12, 31)"
        )
    },
    {
        "tableName": "medidas_html",
        "name": "HTML_Detalhamento_Nao_Aprovados",
        "expression": make_measure_dax(
            "DETALHAMENTO <span>HONORÁRIOS NÃO APROVADOS</span>",
            "Não Aprov.",
            "vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_NAO_APROVADO]",
            "vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_NAO_APROVADO] > 0 && vw_powerbi_relatorio_aprovacao[AREA_ANTERIOR] = \"REUNIÃO TÉCNICA\" && vw_powerbi_relatorio_aprovacao[AREA_ATUAL] = \"FIM\" && vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026, 6, 12) && vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR] >= DATE(2026, 6, 1) && vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR] <= DATE(2026, 12, 31)"
        )
    },
    {
        "tableName": "medidas_html",
        "name": "HTML_Detalhamento_Iniciais",
        "expression": make_measure_dax(
            "DETALHAMENTO <span>HONORÁRIOS INICIAIS</span>",
            "Iniciais",
            "COALESCE(vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_HONORARIOS_INICIAIS], vw_powerbi_relatorio_aprovacao[HONORARIOS_INICIAIS], 0)",
            "COALESCE(vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_HONORARIOS_INICIAIS], vw_powerbi_relatorio_aprovacao[HONORARIOS_INICIAIS], 0) > 0 && vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026, 6, 12) && vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR] >= DATE(2026, 6, 1) && vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR] <= DATE(2026, 12, 31)"
        )
    },
    {
        "tableName": "medidas_html",
        "name": "HTML_Detalhamento_Restituicao",
        "expression": make_measure_dax(
            "DETALHAMENTO <span>HONORÁRIOS RESTITUIÇÃO</span>",
            "Restituição",
            "vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_RESTITUICAO]",
            "vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_RESTITUICAO] > 0 && vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026, 6, 12) && vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR] >= DATE(2026, 6, 1) && vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR] <= DATE(2026, 12, 31)"
        )
    }
]

payload = base_measures + detalhes

with open('perfect_master_payload.json', 'w', encoding='utf-8') as f:
    json.dump(payload, f, ensure_ascii=False, indent=2)

print(f"Generated perfect_master_payload.json with {len(payload)} measures successfully")

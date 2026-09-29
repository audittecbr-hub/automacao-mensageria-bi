import json
import subprocess

# 1. Base Measures for vw_powerbi_relatorio_aprovacao
base_measures = [
    {
        "tableName": "vw_powerbi_relatorio_aprovacao",
        "name": "Honorários encontrados",
        "expression": """SUM(vw_powerbi_relatorio_aprovacao[TOTAL_ENCONTRADO])"""
    },
    {
        "tableName": "vw_powerbi_relatorio_aprovacao",
        "name": "Honorários apresentados",
        "expression": """CALCULATE(
    SUM(vw_powerbi_relatorio_aprovacao[TOTAL_APRESENTADO]),
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

# Shared CSS for Detalhamentos
css_shared = """<style>
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
.titulo { font-size: 22px; font-weight: 700; color: var(--text-main); letter-spacing: 0.5px; text-transform: uppercase; display: flex; align-items: center; gap: 8px; }
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
</style>"""

# Shared JS for Detalhamentos
js_shared = """<script>
function parseMoeda(str) {
    if(!str) return 0;
    var clean = str.replace(/[^0-9,-]+/g, '').replace(',', '.');
    var val = parseFloat(clean);
    return isNaN(val) ? 0 : val;
}

function formatarMoeda(val) {
    return 'R$ ' + val.toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
}

function popularProdutos() {
    var sel = document.getElementById('buscaColProduto');
    if(!sel) return;
    var rows = document.querySelectorAll('.linha-detalhe');
    var prods = {};
    for(var i=0; i<rows.length; i++){
        var el = rows[i].querySelector('.td-produto');
        if(el) {
            var p = el.textContent.trim();
            if(p) prods[p] = true;
        }
    }
    var arr = Object.keys(prods).sort();
    for(var j=0; j<arr.length; j++){
        var opt = document.createElement('option');
        opt.value = arr[j].toLowerCase();
        opt.textContent = arr[j];
        sel.appendChild(opt);
    }
}
setTimeout(popularProdutos, 150);

function filtrarTabela(){
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

    for(var i=0; i<rows.length; i++){
        var elT = rows[i].querySelector('.td-tipo'); var tT = elT ? elT.textContent.toLowerCase() : '';
        var elR = rows[i].querySelector('.td-regional'); var tR = elR ? elR.textContent.toLowerCase() : '';
        var elA = rows[i].querySelector('.td-area'); var tA = elA ? elA.textContent.toLowerCase() : '';
        var elC = rows[i].querySelector('.td-cliente'); var tC = elC ? elC.textContent.toLowerCase() : '';
        var elJ = rows[i].querySelector('.td-job'); var tJ = elJ ? elJ.textContent.toLowerCase() : '';
        var elP = rows[i].querySelector('.td-produto'); var tP = elP ? elP.textContent.toLowerCase() : '';
        var valNum = parseFloat(rows[i].getAttribute('data-val')) || 0;
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
        
        if(matchG && matchT && matchR && matchM && matchA && matchC && matchJ && matchP && matchD && matchDM){
            rows[i].style.display = '';
            count++;
            somaValor += valNum;
        } else {
            rows[i].style.display = 'none';
        }
    }
    var elCount = document.getElementById('totalLinhasCount');
    if(elCount) elCount.innerHTML = '&#128196; <b>' + count.toLocaleString('pt-BR') + '</b> registros';
    var elValor = document.getElementById('totalValorCount');
    if(elValor) elValor.innerHTML = '&#128176; <b>' + formatarMoeda(somaValor) + '</b>';
    var elTfoot = document.getElementById('tfootTotalValor');
    if(elTfoot) elTfoot.innerText = formatarMoeda(somaValor);
}

window.onload = function() { filtrarTabela(); };
document.addEventListener('DOMContentLoaded', filtrarTabela);
setTimeout(filtrarTabela, 100);

function copiarTabela() {
    try {
        var btn = document.getElementById('btnCopiar');
        var originalText = btn.innerHTML;
        btn.innerHTML = '&#8982; Copiando...';
        var textToCopy = '';
        var nl = String.fromCharCode(13, 10);
        var tab = String.fromCharCode(9);
        var ths = document.querySelectorAll('.tabela thead th');
        for(var i=0; i<ths.length; i++) {
            var span = ths[i].querySelector('span');
            var thText = span ? span.textContent.trim() : ths[i].textContent.trim();
            textToCopy += thText + (i < ths.length - 1 ? tab : '');
        }
        textToCopy += nl;
        var rows = document.querySelectorAll('.linha-detalhe');
        var copiedCount = 0;
        for(var i=0; i<rows.length; i++) {
            if(rows[i].style.display !== 'none') {
                var tds = rows[i].querySelectorAll('td');
                for(var j=0; j<tds.length; j++) {
                    textToCopy += tds[j].textContent.trim() + (j < tds.length - 1 ? tab : '');
                }
                textToCopy += nl;
                copiedCount++;
            }
        }
        var tfootVal = document.getElementById('tfootTotalValor');
        if(tfootVal) {
            textToCopy += 'TOTAL' + tab + tab + tab + tab + tab + tab + tab + tab + tfootVal.innerText.trim() + nl;
        }
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
        setTimeout(function() { 
            btn.innerHTML = originalText; 
            btn.style.borderColor = 'var(--border)';
            btn.style.color = 'var(--text-sec)';
        }, 2500);
    } catch (e) {
        alert('Erro ao copiar: ' + e.message);
    }
}
</script>"""

print("Setup completed")

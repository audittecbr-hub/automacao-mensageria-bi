import json
import subprocess

hono_enc_expr = """SUM(vw_powerbi_relatorio_aprovacao[TOTAL_ENCONTRADO])"""

html_enc_expr = """
VAR _mesAtual = IF(DAY(TODAY()) < 10, FORMAT(EDATE(TODAY(), -1), "yyyy-MM"), FORMAT(TODAY(), "yyyy-MM"))
VAR _css = "<style>
:root { --bg: #0d1117; --bg-card: #161b22; --border: #30363d; --text-main: #c9d1d9; --text-sec: #8b949e; --text-muted: #484f58; --accent: #58a6ff; --blue: #58a6ff; --green: #2ea043; --orange: #d29922; --red: #f85149; --font: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif; }
body { margin:0; padding:20px; font-family:var(--font); background-color:transparent; color:var(--text-main); }
.painel { background-color:var(--bg); border:1px solid var(--border); border-radius:12px; padding:24px; box-shadow: 0 8px 24px rgba(0,0,0,0.5); display:flex; flex-direction:column; gap:20px; height: calc(100vh - 40px); box-sizing: border-box; }
.cabecalho { display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid var(--border); padding-bottom:16px; }
.cabecalho-esquerda { display:flex; align-items:center; gap:16px; }
.titulo { font-size:24px; font-weight:800; letter-spacing:1px; color:var(--text-main); text-transform:uppercase; }
.titulo span { color:var(--accent); }
.count-destaque { background:var(--accent); color:#000; padding:4px 12px; border-radius:12px; font-weight:800; font-size:16px; }
.btn-voltar { background:transparent; border:1px solid var(--border); color:var(--text-sec); padding:8px 16px; border-radius:6px; cursor:pointer; font-weight:600; transition:0.2s; }
.btn-voltar:hover { background:var(--border); color:var(--text-main); }
.controles { display:flex; gap:12px; }
.input-busca { background:var(--bg-card); border:1px solid var(--border); color:var(--text-main); padding:8px 12px; border-radius:6px; width:250px; font-family:var(--font); }
.input-busca:focus { outline:none; border-color:var(--accent); }
.btn-copiar { background:var(--border); border:none; color:var(--text-main); padding:8px 16px; border-radius:6px; cursor:pointer; font-weight:600; transition:0.2s; }
.btn-copiar:hover { background:var(--accent); color:#000; }
.table-wrapper { flex:1; overflow:auto; border-radius:8px; border:1px solid var(--border); }
.tabela { width:100%; border-collapse:collapse; text-align:left; }
.tabela thead th { position:sticky; top:0; background:var(--bg-card); padding:16px; font-size:13px; text-transform:uppercase; letter-spacing:1px; color:var(--text-sec); border-bottom:1px solid var(--border); z-index:2; box-shadow: 0 4px 6px rgba(0,0,0,0.3); }
.tabela tbody td { padding:14px 16px; border-bottom:1px solid var(--border); font-size:14px; color:var(--text-main); }
.tabela tbody tr:hover { background:rgba(255,255,255,0.03); }
.col-filter { margin-top:8px; width:100%; background:var(--bg); border:1px solid var(--border); color:var(--text-main); padding:6px; border-radius:4px; font-size:12px; font-family:var(--font); box-sizing:border-box; }
.col-filter:focus { outline:none; border-color:var(--accent); }
::-webkit-scrollbar { width:8px; height:8px; }
::-webkit-scrollbar-track { background:var(--bg); }
::-webkit-scrollbar-thumb { background:var(--border); border-radius:4px; }
::-webkit-scrollbar-thumb:hover { background:var(--text-muted); }
</style>"

VAR _linhas_encontrados = 
    CONCATENATEX(
        FILTER(
            vw_powerbi_relatorio_aprovacao, 
            vw_powerbi_relatorio_aprovacao[TOTAL_ENCONTRADO] > 0 
            && vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026, 6, 12)
        ),
        "<tr class='linha-detalhe' data-rt='" & FORMAT(vw_powerbi_relatorio_aprovacao[DATA_RT], "yyyy-MM-dd") & "' data-mov='" & FORMAT(vw_powerbi_relatorio_aprovacao[data_mov_anterior], "yyyy-MM-dd") & "'>" & 
        "<td class='td-tipo'>Encontrado</td>" &
        "<td class='td-regional'>" & vw_powerbi_relatorio_aprovacao[Regional] & "</td>" & 
        "<td class='td-area'>" & vw_powerbi_relatorio_aprovacao[AREA_ATUAL] & "</td>" & 
        "<td class='td-cliente'>" & LEFT(vw_powerbi_relatorio_aprovacao[NOME], 40) & "</td>" & 
        "<td class='td-job'>" & vw_powerbi_relatorio_aprovacao[JOB] & "</td>" & 
        "<td class='td-produto'>" & vw_powerbi_relatorio_aprovacao[NOME_TRIBUTO] & "</td>" & 
        "<td class='td-data-rt'>" & FORMAT(vw_powerbi_relatorio_aprovacao[DATA_RT], "dd/MM/yyyy") & "</td>" & 
        "<td class='td-data-mov'>" & FORMAT(vw_powerbi_relatorio_aprovacao[data_mov_anterior], "dd/MM/yyyy") & "</td>" & 
        "<td class='td-valor' style='text-align:right; font-family:var(--font); font-variant-numeric: tabular-nums; letter-spacing:-0.5px; color:var(--accent); font-weight:600;'>" & FORMAT(vw_powerbi_relatorio_aprovacao[TOTAL_ENCONTRADO], "Currency") & "</td>" & 
        "</tr>",
        "",
        vw_powerbi_relatorio_aprovacao[TOTAL_ENCONTRADO], DESC
    )

VAR _js = "<script>
try {
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
popularProdutos();
function filtrarTabela(){
    var eG = document.getElementById('buscaGlobal'); var qG = eG ? eG.value.toLowerCase().trim() : '';
    var eT = document.getElementById('buscaColTipo'); var qT = eT ? eT.value.toLowerCase().trim() : '';
    var eR = document.getElementById('buscaColRegional'); var qR = eR ? eR.value.toLowerCase().trim() : '';
    var eA = document.getElementById('buscaColArea'); var qA = eA ? eA.value.toLowerCase().trim() : '';
    var eC = document.getElementById('buscaColCliente'); var qC = eC ? eC.value.toLowerCase().trim() : '';
    var eJ = document.getElementById('buscaColJob'); var qJ = eJ ? eJ.value.toLowerCase().trim() : '';
    var eP = document.getElementById('buscaColProduto'); var qP = eP ? eP.value.toLowerCase().trim() : '';
    var eD = document.getElementById('buscaColData'); var qD = eD ? eD.value.trim() : '';
    var eDM = document.getElementById('buscaColDataMov'); var qDM = eDM ? eDM.value.toLowerCase().trim() : '';
    
    var rows=document.querySelectorAll('.linha-detalhe');
    var count=0;
    for(var i=0;i<rows.length;i++){
        var elT = rows[i].querySelector('.td-tipo'); var tT = elT ? elT.textContent.toLowerCase() : '';
        var elR = rows[i].querySelector('.td-regional'); var tR = elR ? elR.textContent.toLowerCase() : '';
        var elA = rows[i].querySelector('.td-area'); var tA = elA ? elA.textContent.toLowerCase() : '';
        var elC = rows[i].querySelector('.td-cliente'); var tC = elC ? elC.textContent.toLowerCase() : '';
        var elJ = rows[i].querySelector('.td-job'); var tJ = elJ ? elJ.textContent.toLowerCase() : '';
        var elP = rows[i].querySelector('.td-produto'); var tP = elP ? elP.textContent.toLowerCase() : '';
        var elDM = rows[i].querySelector('.td-data-mov'); var tDM = elDM ? elDM.textContent.toLowerCase() : '';
        
        var dtRtStr = rows[i].getAttribute('data-rt');
        var dtMovStr = rows[i].getAttribute('data-mov');
        var matchD = (qD === '' || dtRtStr === qD);
        var matchDM = (qDM === '' || dtMovStr === qDM);
        
        var matchG=(qG==='' || tA.indexOf(qG)>-1 || tC.indexOf(qG)>-1 || tJ.indexOf(qG)>-1 || tP.indexOf(qG)>-1 || tR.indexOf(qG)>-1 || tT.indexOf(qG)>-1 || tDM.indexOf(qG)>-1);
        var matchT=(qT==='' || tT.indexOf(qT)>-1);
        var matchR=(qR==='' || tR.indexOf(qR)>-1);
        var matchA=(qA==='' || tA.indexOf(qA)>-1);
        var matchC=(qC==='' || tC.indexOf(qC)>-1);
        var matchJ=(qJ==='' || tJ.indexOf(qJ)>-1);
        var matchP=(qP==='' || tP.indexOf(qP)>-1);
        
        if(matchG && matchT && matchR && matchA && matchC && matchJ && matchP && matchD && matchDM){
            rows[i].style.display='';
            count++;
        }else{
            rows[i].style.display='none';
        }
    }
    var elCount = document.getElementById('totalLinhasCount');
    if(elCount) elCount.textContent=count;
}
window.onload = function() {
    filtrarTabela();
};
document.addEventListener('DOMContentLoaded', filtrarTabela);
setTimeout(filtrarTabela, 100);
} catch (e) {
    console.error(e);
}

function copiarTabela() {
    try {
        var btn = document.getElementById('btnCopiar');
        var originalText = btn.innerHTML;
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
        for(var i=0; i<rows.length; i++) {
            if(rows[i].style.display !== 'none') {
                var tds = rows[i].querySelectorAll('td');
                for(var j=0; j<tds.length; j++) {
                    textToCopy += tds[j].textContent.trim() + (j < tds.length - 1 ? tab : '');
                }
                textToCopy += nl;
            }
        }
        var tempInput = document.createElement('textarea');
        tempInput.style.position = 'absolute';
        tempInput.style.left = '-9999px';
        tempInput.value = textToCopy;
        document.body.appendChild(tempInput);
        tempInput.select();
        document.execCommand('copy'); 
        btn.innerHTML = '&#10004; Copiado!';
        document.body.removeChild(tempInput);
        setTimeout(function() { btn.innerHTML = originalText; }, 2000);
    } catch (e) {
        alert('Erro ao copiar: ' + e.message);
    }
}
</script>"

VAR _html = 
    "<html><head><meta charset='UTF-8'>" & _css & "</head><body>" &
    "<div class='painel'>" &
        "<div class='cabecalho'>" &
            "<div class='cabecalho-esquerda'>" &
                "<button class='btn-voltar'>&#8592; Voltar</button>" &
                "<div class='titulo'>DETALHAMENTO <span>HONORÁRIOS ENCONTRADOS</span></div>" &
                "<div class='count-destaque' id='totalLinhasCount'>0</div>" &
            "</div>" &
            "<div class='controles'>" &
                "<input type='text' id='buscaGlobal' class='busca-global input-busca' placeholder='&#128269; Buscar em tudo...' onkeyup='filtrarTabela()'>" &
                "<button class='btn-copiar' id='btnCopiar' onclick='copiarTabela()'>&#128203; Copiar Linhas</button>" &
            "</div>" &
        "</div>" &
        "<div class='table-wrapper'>" &
            "<table class='tabela' id='tabelaDetalhe'>" &
                "<thead>" &
                    "<tr>" &
                        "<th><span>Tipo</span><br><select id='buscaColTipo' class='col-filter' onchange='filtrarTabela()'><option value=''>Todos</option><option value='encontrado'>Encontrado</option></select></th>" &
                        "<th><span>Regional</span><br><select id='buscaColRegional' class='col-filter' onchange='filtrarTabela()'><option value=''>Todas</option><option value='regional sul'>Regional Sul</option><option value='regional so paulo'>Regional SP</option><option value='regional sudeste'>Regional Sudeste</option><option value='regional nnco'>Regional NNCO</option></select></th>" &
                        "<th><span>Área</span><br><input type='text' id='buscaColArea' class='col-filter' placeholder='Filtrar Área...' onkeyup='filtrarTabela()'></th>" &
                        "<th><span>Cliente</span><br><input type='text' id='buscaColCliente' class='col-filter' placeholder='Filtrar Cliente...' onkeyup='filtrarTabela()'></th>" &
                        "<th><span>Job</span><br><input type='text' id='buscaColJob' class='col-filter' placeholder='Filtrar Job...' onkeyup='filtrarTabela()'></th>" &
                        "<th><span>Produto</span><br><select id='buscaColProduto' class='col-filter' onchange='filtrarTabela()'><option value=''>Todos</option></select></th>" &
                        "<th><span>Data_RT</span><br><input type='date' id='buscaColData' class='col-filter' onchange='filtrarTabela()'></th>" &
                        "<th><span>Data_Mov</span><br><input type='date' id='buscaColDataMov' class='col-filter' onchange='filtrarTabela()'></th>" &
                        "<th style='text-align:right;'><span>Valor Honorário</span><br><div style='height:26px;'></div></th>" &
                    "</tr>" &
                "</thead>" &
                "<tbody id='tbodyDetalhe'>" &
                    _linhas_encontrados &
                "</tbody>" &
            "</table>" &
        "</div>" &
    "</div>" & _js & "</body></html>"

RETURN _html
"""

payload = [
    {
        "tableName": "vw_powerbi_relatorio_aprovacao",
        "name": "Honorários encontrados",
        "expression": hono_enc_expr
    },
    {
        "tableName": "medidas_html",
        "name": "HTML_Detalhamento_Encontrados",
        "expression": html_enc_expr
    }
]

with open('fix_encontrados_payload.json', 'w', encoding='utf-8') as f:
    json.dump(payload, f, ensure_ascii=False, indent=2)

ps_script = """
$dll = "C:\\Program Files\\On-premises data gateway\\FabricIntegrationRuntime\\5.0\\Gateway\\Microsoft.AnalysisServices.Tabular.dll"
[System.Reflection.Assembly]::LoadFrom($dll) | Out-Null
$server = New-Object Microsoft.AnalysisServices.Tabular.Server
$server.Connect("localhost:60593")
$model = $server.Databases[0].Model

$json = Get-Content -Raw -Encoding UTF8 "fix_encontrados_payload.json" | ConvertFrom-Json

foreach ($item in $json) {
    $table = $model.Tables[$item.tableName]
    if ($table) {
        $m = $table.Measures[$item.name]
        if ($m) {
            $m.Expression = $item.expression
            Write-Output "Updated measure: $($item.name) in table $($item.tableName)"
        }
    }
}

$model.SaveChanges()
Write-Output "SUCCESS_SAVED"
$server.Disconnect()
"""

with open('apply_fix_encontrados.ps1', 'w', encoding='utf-8') as f:
    f.write(ps_script)

res = subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-File", "apply_fix_encontrados.ps1"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
print(res.stdout.decode('latin1', errors='replace'))

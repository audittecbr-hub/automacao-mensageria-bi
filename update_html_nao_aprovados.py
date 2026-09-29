import re

filepath = r"C:\Users\cristhofer.maciel.GRUPOSTUDIO\Downloads\honorarios_regionais (2).SemanticModel\definition\tables\medidas_html.tmdl"

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Insert _dadosNaoAprovadosReal after _dadosPerdidos definition
dado_nao_aprovados_real = """
			VAR _dadosNaoAprovadosReal = 
			    CONCATENATEX(
			        _datas_produtos,
			        VAR _d = [AnoMes]
			        VAR _p = [FiltroProduto]
			        VAR _anoSelecionado = VALUE(LEFT(_d, 4))
			        VAR _mesSelecionado = VALUE(RIGHT(_d, 2))
			        VAR _dataUltimoDiaMes = EOMONTH(DATE(_anoSelecionado, _mesSelecionado, 1), 0)
			        VAR _isCurrentMonth = IF(_anoSelecionado = YEAR(TODAY()) && _mesSelecionado = MONTH(TODAY()), TRUE(), FALSE())
			        VAR _dataFinal = IF(_isCurrentMonth, TODAY(), _dataUltimoDiaMes)
			        VAR _dataInicial = _dataFinal - 60
			
			        VAR _vSul = CALCULATE([Honorários não aprovados], vw_powerbi_relatorio_aprovacao[Regional] = "Regional Sul", FORMAT(vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR], "yyyy-MM") = _d, vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026, 6, 12), vw_powerbi_relatorio_aprovacao[NOME_TRIBUTO] = _p) + 0
			        VAR _vSP = CALCULATE([Honorários não aprovados], vw_powerbi_relatorio_aprovacao[Regional] = "Regional Sudeste", FORMAT(vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR], "yyyy-MM") = _d, vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026, 6, 12), vw_powerbi_relatorio_aprovacao[NOME_TRIBUTO] = _p) + 0
			        VAR _vSudeste = CALCULATE([Honorários não aprovados], vw_powerbi_relatorio_aprovacao[Regional] = "Regional Sudeste 2", FORMAT(vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR], "yyyy-MM") = _d, vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026, 6, 12), vw_powerbi_relatorio_aprovacao[NOME_TRIBUTO] = _p) + 0
			        VAR _vNNCO = CALCULATE([Honorários não aprovados], vw_powerbi_relatorio_aprovacao[Regional] = "Regional NNCO", FORMAT(vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR], "yyyy-MM") = _d, vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026, 6, 12), vw_powerbi_relatorio_aprovacao[NOME_TRIBUTO] = _p) + 0
			        VAR _vOutras = CALCULATE([Honorários não aprovados], vw_powerbi_relatorio_aprovacao[Regional] = "Outras", FORMAT(vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR], "yyyy-MM") = _d, vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026, 6, 12), vw_powerbi_relatorio_aprovacao[NOME_TRIBUTO] = _p) + 0
			        VAR _somaDia = _vSul + _vSP + _vSudeste + _vNNCO + _vOutras
			        RETURN IF(_somaDia > 0,
			            "<span class='dado-nao-aprovados-real' data-regional='Regional Sul' data-valor='" & FORMAT(_vSul, "0.00") & "' data-data='" & _d & "' data-produto='" & _p & "'></span>" &
			            "<span class='dado-nao-aprovados-real' data-regional='Regional Sudeste' data-valor='" & FORMAT(_vSP, "0.00") & "' data-data='" & _d & "' data-produto='" & _p & "'></span>" &
			            "<span class='dado-nao-aprovados-real' data-regional='Regional Sudeste 2' data-valor='" & FORMAT(_vSudeste, "0.00") & "' data-data='" & _d & "' data-produto='" & _p & "'></span>" &
			            "<span class='dado-nao-aprovados-real' data-regional='Regional NNCO' data-valor='" & FORMAT(_vNNCO, "0.00") & "' data-data='" & _d & "' data-produto='" & _p & "'></span>" &
			            "<span class='dado-nao-aprovados-real' data-regional='Outras' data-valor='" & FORMAT(_vOutras, "0.00") & "' data-data='" & _d & "' data-produto='" & _p & "'></span>",
			            ""
			        ),
			        ""
			    )
"""
if "_dadosNaoAprovadosReal =" not in content:
    content = content.replace("VAR _dadosAprovadosTotal =", dado_nao_aprovados_real + "\n\t\t\tVAR _dadosAprovadosTotal =")

# 2. Insert container div in _html
if "id='dados-nao-aprovados-real-container'" not in content:
    content = content.replace(
        "\"<div style='display:none;' id='dados-perdidos-container'>\" & _dadosPerdidos & \"</div>\" &",
        "\"<div style='display:none;' id='dados-perdidos-container'>\" & _dadosPerdidos & \"</div>\" &\n\t\t\t    \"<div style='display:none;' id='dados-nao-aprovados-real-container'>\" & _dadosNaoAprovadosReal & \"</div>\" &"
    )

# 3. Add _linha3_nao_aprovados
linha3_nao_aprovados = """
			VAR _linha3_nao_aprovados = 
			    "<tr onmouseover=\\"this.style.background='rgba(239,68,68,0.05)'\\" onmouseout=\\"this.style.background='transparent'\\">" &
			        "<td><div style='font-size:18px; font-weight:600; letter-spacing: 0.5px; color:var(--text-main); margin-bottom:4px;'>&#9888;&#65039; Honorários Não Aprovados</div><div style='font-size:13px; color:var(--text-muted); font-weight:400; text-transform: uppercase; letter-spacing: 0.5px;'>Reunião Técnica para o fim</div></td>" &
			        "<td id='nareal-sul' style='color:var(--red);'>R$ 0,00</td>" &
			        "<td id='nareal-sp' style='color:var(--red);'>R$ 0,00</td>" &
			        "<td id='nareal-sd' style='color:var(--red);'>R$ 0,00</td>" &
			        "<td id='nareal-nn' style='color:var(--red);'>R$ 0,00</td>" &
			        "<td id='nareal-total' style='color:var(--red); font-weight:700; font-size:24px; font-weight:600; font-variant-numeric: tabular-nums; letter-spacing: -1px;'>R$ 0,00</td>" &
			    "</tr>"
"""
if "_linha3_nao_aprovados =" not in content:
    content = content.replace("VAR _linha4 =", linha3_nao_aprovados + "\n\t\t\tVAR _linha4 =")

# 4. Append to table body
content = content.replace("_linha_nao_aprovados & _linha3 & _linha4", "_linha_nao_aprovados & _linha3 & _linha3_nao_aprovados & _linha4")

# 5. Add JS logic
js_logic = """
			        "var sNaoAprovReal = calcularSoma('dado-nao-aprovados-real');" &
			        "document.getElementById('nareal-sul').innerText = formatarMoeda(sNaoAprovReal['Regional Sul']);" &
			        "document.getElementById('nareal-sp').innerText = formatarMoeda(sNaoAprovReal['Regional Sudeste']);" &
			        "document.getElementById('nareal-sd').innerText = formatarMoeda(sNaoAprovReal['Regional Sudeste 2']);" &
			        "document.getElementById('nareal-nn').innerText = formatarMoeda(sNaoAprovReal['Regional NNCO']);" &
			        "document.getElementById('nareal-total').innerText = formatarMoeda(sNaoAprovReal['Total']);" &
			        "var cardNAReal = document.getElementById('card-nao-aprovados-real'); if(cardNAReal) cardNAReal.innerText = formatarMilhoes(sNaoAprovReal['Total']);" &
"""
if "var sNaoAprovReal =" not in content:
    content = content.replace(
        "\"document.getElementById('perdidos-total').innerText = formatarMoeda(sPerd['Total']);\" &",
        "\"document.getElementById('perdidos-total').innerText = formatarMoeda(sPerd['Total']);\" &\n" + js_logic
    )

# 6. Add KPI card
kpi_card = """
			            "<div class='card'>" &
			                "<div class='card-title'>&#9888;&#65039; Honorários Não Aprovados</div>" &
			                "<div class='card-value' id='card-nao-aprovados-real'>R$ 0,00</div>" &
			                "<div><span class='card-indicator ind-down'>&#8595; 0%</span> <span style='font-size:11px;color:var(--text-muted);'>vs mês ant.</span></div>" &
			            "</div>" &
"""
if "id='card-nao-aprovados-real'" not in content:
    content = content.replace(
        "\"<div class='card-value' id='card-perdidos'>R$ 0,00</div>\" &\n\t\t\t                \"<div><span class='card-indicator ind-down'>&#8595; 0%</span> <span style='font-size:11px;color:var(--text-muted);'>vs mês ant.</span></div>\" &\n\t\t\t            \"</div>\" &",
        "\"<div class='card-value' id='card-perdidos'>R$ 0,00</div>\" &\n\t\t\t                \"<div><span class='card-indicator ind-down'>&#8595; 0%</span> <span style='font-size:11px;color:var(--text-muted);'>vs mês ant.</span></div>\" &\n\t\t\t            \"</div>\" &" + kpi_card
    )


# 7. Extract HTML_Detalhamento_Aprovados measure body to create HTML_Detalhamento_Nao_Aprovados
aprovados_match = re.search(r"^\tmeasure HTML_Detalhamento_Aprovados = ```\n(.*?)\n\t\t\t```\n\t\tlineageTag", content, flags=re.MULTILINE | re.DOTALL)
if aprovados_match:
    aprovados_body = aprovados_match.group(1)
    
    # Modify the body to become Não Aprovados
    nao_aprovados_body = aprovados_body.replace("[Honorários aprovados]", "[Honorários não aprovados]")
    nao_aprovados_body = nao_aprovados_body.replace("HONORÁRIOS APROVADOS", "HONORÁRIOS NÃO APROVADOS")
    nao_aprovados_body = nao_aprovados_body.replace("_linhas_aprovados", "_linhas_nao_aprovados")
    nao_aprovados_body = nao_aprovados_body.replace("<td class='td-tipo'>Aprovado</td>", "<td class='td-tipo'>Não Aprov.</td>")
    
    new_measure = "\tmeasure HTML_Detalhamento_Nao_Aprovados = ```\n" + nao_aprovados_body + "\n\t\t\t```\n\t\tlineageTag"
    
    # Replace the old HTML_Detalhamento_Nao_Aprovados
    na_regex = r"^\tmeasure HTML_Detalhamento_Nao_Aprovados = ```\n(.*?)\n\t\t\t```\n\t\tlineageTag"
    content = re.sub(na_regex, new_measure, content, flags=re.MULTILINE | re.DOTALL)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated medidas_html.tmdl")

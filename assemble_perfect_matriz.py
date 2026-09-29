import json

with open('matriz_updated.dax', 'r', encoding='utf-8') as f:
    dax = f.read()

# 1. Update CSS for 8 columns in summary-cards
dax = dax.replace(
    ".summary-cards { display: grid; grid-template-columns: repeat(7, 1fr); gap: 15px; margin-bottom: 30px; position: relative; z-index: 1; }",
    ".summary-cards { display: grid; grid-template-columns: repeat(8, 1fr); gap: 10px; margin-bottom: 30px; position: relative; z-index: 1; }\n.card-title { font-size: 13px; color: var(--text-sec); text-transform: uppercase; letter-spacing: 0.5px; font-weight: 600; display:flex; align-items:center; gap:6px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }\n.card-value { font-size: 24px; font-weight: 700; color: var(--text-main); font-family: var(--font); letter-spacing: -0.5px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }"
)

# 2. Add Data Extraction blocks for Aprovados em Negociação
dados_apneg_total = """VAR _dadosAprovNegocTotal = 
    CONCATENATEX(
        _datas_produtos,
        VAR _d = [AnoMes]
        VAR _p = [FiltroProduto]
        VAR _vSul = CALCULATE([Honorários aprovados em negociação], vw_powerbi_relatorio_aprovacao[Regional] = "Regional Sul", FORMAT(vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR], "yyyy-MM") = _d, vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026, 6, 12), vw_powerbi_relatorio_aprovacao[NOME_TRIBUTO] = _p) + 0
        VAR _vSP = CALCULATE([Honorários aprovados em negociação], vw_powerbi_relatorio_aprovacao[Regional] = "Regional Sudeste", FORMAT(vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR], "yyyy-MM") = _d, vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026, 6, 12), vw_powerbi_relatorio_aprovacao[NOME_TRIBUTO] = _p) + 0
        VAR _vSudeste = CALCULATE([Honorários aprovados em negociação], vw_powerbi_relatorio_aprovacao[Regional] = "Regional Sudeste 2", FORMAT(vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR], "yyyy-MM") = _d, vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026, 6, 12), vw_powerbi_relatorio_aprovacao[NOME_TRIBUTO] = _p) + 0
        VAR _vNNCO = CALCULATE([Honorários aprovados em negociação], vw_powerbi_relatorio_aprovacao[Regional] = "Regional NNCO", FORMAT(vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR], "yyyy-MM") = _d, vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026, 6, 12), vw_powerbi_relatorio_aprovacao[NOME_TRIBUTO] = _p) + 0
        VAR _vOutras = CALCULATE([Honorários aprovados em negociação], vw_powerbi_relatorio_aprovacao[Regional] = "Outras", FORMAT(vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR], "yyyy-MM") = _d, vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026, 6, 12), vw_powerbi_relatorio_aprovacao[NOME_TRIBUTO] = _p) + 0
        VAR _vSul_sr = CALCULATE([Honorários aprovados em negociação], vw_powerbi_relatorio_aprovacao[Regional] = "Regional Sul", FORMAT(vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR], "yyyy-MM") = _d, vw_powerbi_relatorio_aprovacao[NOME_TRIBUTO] = _p) + 0
        VAR _vSP_sr = CALCULATE([Honorários aprovados em negociação], vw_powerbi_relatorio_aprovacao[Regional] = "Regional Sudeste", FORMAT(vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR], "yyyy-MM") = _d, vw_powerbi_relatorio_aprovacao[NOME_TRIBUTO] = _p) + 0
        VAR _vSudeste_sr = CALCULATE([Honorários aprovados em negociação], vw_powerbi_relatorio_aprovacao[Regional] = "Regional Sudeste 2", FORMAT(vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR], "yyyy-MM") = _d, vw_powerbi_relatorio_aprovacao[NOME_TRIBUTO] = _p) + 0
        VAR _vNNCO_sr = CALCULATE([Honorários aprovados em negociação], vw_powerbi_relatorio_aprovacao[Regional] = "Regional NNCO", FORMAT(vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR], "yyyy-MM") = _d, vw_powerbi_relatorio_aprovacao[NOME_TRIBUTO] = _p) + 0
        VAR _vOutras_sr = CALCULATE([Honorários aprovados em negociação], vw_powerbi_relatorio_aprovacao[Regional] = "Outras", FORMAT(vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR], "yyyy-MM") = _d, vw_powerbi_relatorio_aprovacao[NOME_TRIBUTO] = _p) + 0
        VAR _somaDia_sr = _vSul_sr + _vSP_sr + _vSudeste_sr + _vNNCO_sr + _vOutras_sr
        RETURN IF(_somaDia_sr > 0,
            "<span class='dado-apneg-total' data-regional='Regional Sul' data-valor='" & FORMAT(_vSul, "0.00") & "' data-valor-sr='" & FORMAT(_vSul_sr, "0.00") & "' data-data='" & _d & "' data-produto='" & _p & "'></span>" &
            "<span class='dado-apneg-total' data-regional='Regional Sudeste' data-valor='" & FORMAT(_vSP, "0.00") & "' data-valor-sr='" & FORMAT(_vSP_sr, "0.00") & "' data-data='" & _d & "' data-produto='" & _p & "'></span>" &
            "<span class='dado-apneg-total' data-regional='Regional Sudeste 2' data-valor='" & FORMAT(_vSudeste, "0.00") & "' data-valor-sr='" & FORMAT(_vSudeste_sr, "0.00") & "' data-data='" & _d & "' data-produto='" & _p & "'></span>" &
            "<span class='dado-apneg-total' data-regional='Regional NNCO' data-valor='" & FORMAT(_vNNCO, "0.00") & "' data-valor-sr='" & FORMAT(_vNNCO_sr, "0.00") & "' data-data='" & _d & "' data-produto='" & _p & "'></span>" &
            "<span class='dado-apneg-total' data-regional='Outras' data-valor='" & FORMAT(_vOutras, "0.00") & "' data-valor-sr='" & FORMAT(_vOutras_sr, "0.00") & "' data-data='" & _d & "' data-produto='" & _p & "'></span>",
            ""
        ),
        ""
    )

VAR _dadosAprovNegocIniciais = 
    CONCATENATEX(
        _datas_produtos,
        VAR _d = [AnoMes]
        VAR _p = [FiltroProduto]
        VAR _vSul = CALCULATE([Honorários aprovados negociação iniciais], vw_powerbi_relatorio_aprovacao[Regional] = "Regional Sul", FORMAT(vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR], "yyyy-MM") = _d, vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026, 6, 12), vw_powerbi_relatorio_aprovacao[NOME_TRIBUTO] = _p) + 0
        VAR _vSP = CALCULATE([Honorários aprovados negociação iniciais], vw_powerbi_relatorio_aprovacao[Regional] = "Regional Sudeste", FORMAT(vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR], "yyyy-MM") = _d, vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026, 6, 12), vw_powerbi_relatorio_aprovacao[NOME_TRIBUTO] = _p) + 0
        VAR _vSudeste = CALCULATE([Honorários aprovados negociação iniciais], vw_powerbi_relatorio_aprovacao[Regional] = "Regional Sudeste 2", FORMAT(vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR], "yyyy-MM") = _d, vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026, 6, 12), vw_powerbi_relatorio_aprovacao[NOME_TRIBUTO] = _p) + 0
        VAR _vNNCO = CALCULATE([Honorários aprovados negociação iniciais], vw_powerbi_relatorio_aprovacao[Regional] = "Regional NNCO", FORMAT(vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR], "yyyy-MM") = _d, vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026, 6, 12), vw_powerbi_relatorio_aprovacao[NOME_TRIBUTO] = _p) + 0
        VAR _vSul_sr = CALCULATE([Honorários aprovados negociação iniciais], vw_powerbi_relatorio_aprovacao[Regional] = "Regional Sul", FORMAT(vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR], "yyyy-MM") = _d, vw_powerbi_relatorio_aprovacao[NOME_TRIBUTO] = _p) + 0
        VAR _vSP_sr = CALCULATE([Honorários aprovados negociação iniciais], vw_powerbi_relatorio_aprovacao[Regional] = "Regional Sudeste", FORMAT(vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR], "yyyy-MM") = _d, vw_powerbi_relatorio_aprovacao[NOME_TRIBUTO] = _p) + 0
        VAR _vSudeste_sr = CALCULATE([Honorários aprovados negociação iniciais], vw_powerbi_relatorio_aprovacao[Regional] = "Regional Sudeste 2", FORMAT(vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR], "yyyy-MM") = _d, vw_powerbi_relatorio_aprovacao[NOME_TRIBUTO] = _p) + 0
        VAR _vNNCO_sr = CALCULATE([Honorários aprovados negociação iniciais], vw_powerbi_relatorio_aprovacao[Regional] = "Regional NNCO", FORMAT(vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR], "yyyy-MM") = _d, vw_powerbi_relatorio_aprovacao[NOME_TRIBUTO] = _p) + 0
        VAR _somaDia_sr = _vSul_sr + _vSP_sr + _vSudeste_sr + _vNNCO_sr
        RETURN IF(_somaDia_sr > 0,
            "<span class='dado-apneg-iniciais' data-regional='Regional Sul' data-valor='" & FORMAT(_vSul, "0.00") & "' data-valor-sr='" & FORMAT(_vSul_sr, "0.00") & "' data-data='" & _d & "' data-produto='" & _p & "'></span>" &
            "<span class='dado-apneg-iniciais' data-regional='Regional Sudeste' data-valor='" & FORMAT(_vSP, "0.00") & "' data-valor-sr='" & FORMAT(_vSP_sr, "0.00") & "' data-data='" & _d & "' data-produto='" & _p & "'></span>" &
            "<span class='dado-apneg-iniciais' data-regional='Regional Sudeste 2' data-valor='" & FORMAT(_vSudeste, "0.00") & "' data-valor-sr='" & FORMAT(_vSudeste_sr, "0.00") & "' data-data='" & _d & "' data-produto='" & _p & "'></span>" &
            "<span class='dado-apneg-iniciais' data-regional='Regional NNCO' data-valor='" & FORMAT(_vNNCO, "0.00") & "' data-valor-sr='" & FORMAT(_vNNCO_sr, "0.00") & "' data-data='" & _d & "' data-produto='" & _p & "'></span>",
            ""
        ),
        ""
    )

VAR _dadosAprovNegocComp = 
    CONCATENATEX(
        _datas_produtos,
        VAR _d = [AnoMes]
        VAR _p = [FiltroProduto]
        VAR _vSul = CALCULATE([Honorários aprovados negociação compensação], vw_powerbi_relatorio_aprovacao[Regional] = "Regional Sul", FORMAT(vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR], "yyyy-MM") = _d, vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026, 6, 12), vw_powerbi_relatorio_aprovacao[NOME_TRIBUTO] = _p) + 0
        VAR _vSP = CALCULATE([Honorários aprovados negociação compensação], vw_powerbi_relatorio_aprovacao[Regional] = "Regional Sudeste", FORMAT(vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR], "yyyy-MM") = _d, vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026, 6, 12), vw_powerbi_relatorio_aprovacao[NOME_TRIBUTO] = _p) + 0
        VAR _vSudeste = CALCULATE([Honorários aprovados negociação compensação], vw_powerbi_relatorio_aprovacao[Regional] = "Regional Sudeste 2", FORMAT(vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR], "yyyy-MM") = _d, vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026, 6, 12), vw_powerbi_relatorio_aprovacao[NOME_TRIBUTO] = _p) + 0
        VAR _vNNCO = CALCULATE([Honorários aprovados negociação compensação], vw_powerbi_relatorio_aprovacao[Regional] = "Regional NNCO", FORMAT(vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR], "yyyy-MM") = _d, vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026, 6, 12), vw_powerbi_relatorio_aprovacao[NOME_TRIBUTO] = _p) + 0
        VAR _vSul_sr = CALCULATE([Honorários aprovados negociação compensação], vw_powerbi_relatorio_aprovacao[Regional] = "Regional Sul", FORMAT(vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR], "yyyy-MM") = _d, vw_powerbi_relatorio_aprovacao[NOME_TRIBUTO] = _p) + 0
        VAR _vSP_sr = CALCULATE([Honorários aprovados negociação compensação], vw_powerbi_relatorio_aprovacao[Regional] = "Regional Sudeste", FORMAT(vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR], "yyyy-MM") = _d, vw_powerbi_relatorio_aprovacao[NOME_TRIBUTO] = _p) + 0
        VAR _vSudeste_sr = CALCULATE([Honorários aprovados negociação compensação], vw_powerbi_relatorio_aprovacao[Regional] = "Regional Sudeste 2", FORMAT(vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR], "yyyy-MM") = _d, vw_powerbi_relatorio_aprovacao[NOME_TRIBUTO] = _p) + 0
        VAR _vNNCO_sr = CALCULATE([Honorários aprovados negociação compensação], vw_powerbi_relatorio_aprovacao[Regional] = "Regional NNCO", FORMAT(vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR], "yyyy-MM") = _d, vw_powerbi_relatorio_aprovacao[NOME_TRIBUTO] = _p) + 0
        VAR _somaDia_sr = _vSul_sr + _vSP_sr + _vSudeste_sr + _vNNCO_sr
        RETURN IF(_somaDia_sr > 0,
            "<span class='dado-apneg-comp' data-regional='Regional Sul' data-valor='" & FORMAT(_vSul, "0.00") & "' data-valor-sr='" & FORMAT(_vSul_sr, "0.00") & "' data-data='" & _d & "' data-produto='" & _p & "'></span>" &
            "<span class='dado-apneg-comp' data-regional='Regional Sudeste' data-valor='" & FORMAT(_vSP, "0.00") & "' data-valor-sr='" & FORMAT(_vSP_sr, "0.00") & "' data-data='" & _d & "' data-produto='" & _p & "'></span>" &
            "<span class='dado-apneg-comp' data-regional='Regional Sudeste 2' data-valor='" & FORMAT(_vSudeste, "0.00") & "' data-valor-sr='" & FORMAT(_vSudeste_sr, "0.00") & "' data-data='" & _d & "' data-produto='" & _p & "'></span>" &
            "<span class='dado-apneg-comp' data-regional='Regional NNCO' data-valor='" & FORMAT(_vNNCO, "0.00") & "' data-valor-sr='" & FORMAT(_vNNCO_sr, "0.00") & "' data-data='" & _d & "' data-produto='" & _p & "'></span>",
            ""
        ),
        ""
    )

VAR _dadosAprovNegocRest = 
    CONCATENATEX(
        _datas_produtos,
        VAR _d = [AnoMes]
        VAR _p = [FiltroProduto]
        VAR _vSul = CALCULATE([Honorários aprovados negociação restituição], vw_powerbi_relatorio_aprovacao[Regional] = "Regional Sul", FORMAT(vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR], "yyyy-MM") = _d, vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026, 6, 12), vw_powerbi_relatorio_aprovacao[NOME_TRIBUTO] = _p) + 0
        VAR _vSP = CALCULATE([Honorários aprovados negociação restituição], vw_powerbi_relatorio_aprovacao[Regional] = "Regional Sudeste", FORMAT(vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR], "yyyy-MM") = _d, vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026, 6, 12), vw_powerbi_relatorio_aprovacao[NOME_TRIBUTO] = _p) + 0
        VAR _vSudeste = CALCULATE([Honorários aprovados negociação restituição], vw_powerbi_relatorio_aprovacao[Regional] = "Regional Sudeste 2", FORMAT(vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR], "yyyy-MM") = _d, vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026, 6, 12), vw_powerbi_relatorio_aprovacao[NOME_TRIBUTO] = _p) + 0
        VAR _vNNCO = CALCULATE([Honorários aprovados negociação restituição], vw_powerbi_relatorio_aprovacao[Regional] = "Regional NNCO", FORMAT(vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR], "yyyy-MM") = _d, vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026, 6, 12), vw_powerbi_relatorio_aprovacao[NOME_TRIBUTO] = _p) + 0
        VAR _vSul_sr = CALCULATE([Honorários aprovados negociação restituição], vw_powerbi_relatorio_aprovacao[Regional] = "Regional Sul", FORMAT(vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR], "yyyy-MM") = _d, vw_powerbi_relatorio_aprovacao[NOME_TRIBUTO] = _p) + 0
        VAR _vSP_sr = CALCULATE([Honorários aprovados negociação restituição], vw_powerbi_relatorio_aprovacao[Regional] = "Regional Sudeste", FORMAT(vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR], "yyyy-MM") = _d, vw_powerbi_relatorio_aprovacao[NOME_TRIBUTO] = _p) + 0
        VAR _vSudeste_sr = CALCULATE([Honorários aprovados negociação restituição], vw_powerbi_relatorio_aprovacao[Regional] = "Regional Sudeste 2", FORMAT(vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR], "yyyy-MM") = _d, vw_powerbi_relatorio_aprovacao[NOME_TRIBUTO] = _p) + 0
        VAR _vNNCO_sr = CALCULATE([Honorários aprovados negociação restituição], vw_powerbi_relatorio_aprovacao[Regional] = "Regional NNCO", FORMAT(vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR], "yyyy-MM") = _d, vw_powerbi_relatorio_aprovacao[NOME_TRIBUTO] = _p) + 0
        VAR _somaDia_sr = _vSul_sr + _vSP_sr + _vSudeste_sr + _vNNCO_sr
        RETURN IF(_somaDia_sr > 0,
            "<span class='dado-apneg-rest' data-regional='Regional Sul' data-valor='" & FORMAT(_vSul, "0.00") & "' data-valor-sr='" & FORMAT(_vSul_sr, "0.00") & "' data-data='" & _d & "' data-produto='" & _p & "'></span>" &
            "<span class='dado-apneg-rest' data-regional='Regional Sudeste' data-valor='" & FORMAT(_vSP, "0.00") & "' data-valor-sr='" & FORMAT(_vSP_sr, "0.00") & "' data-data='" & _d & "' data-produto='" & _p & "'></span>" &
            "<span class='dado-apneg-rest' data-regional='Regional Sudeste 2' data-valor='" & FORMAT(_vSudeste, "0.00") & "' data-valor-sr='" & FORMAT(_vSudeste_sr, "0.00") & "' data-data='" & _d & "' data-produto='" & _p & "'></span>" &
            "<span class='dado-apneg-rest' data-regional='Regional NNCO' data-valor='" & FORMAT(_vNNCO, "0.00") & "' data-valor-sr='" & FORMAT(_vNNCO_sr, "0.00") & "' data-data='" & _d & "' data-produto='" & _p & "'></span>",
            ""
        ),
        ""
    )

VAR _dadosAprovNegocAjuiz = 
    CONCATENATEX(
        _datas_produtos,
        VAR _d = [AnoMes]
        VAR _p = [FiltroProduto]
        VAR _vSul = CALCULATE([Honorários aprovados negociação ajuizamento], vw_powerbi_relatorio_aprovacao[Regional] = "Regional Sul", FORMAT(vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR], "yyyy-MM") = _d, vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026, 6, 12), vw_powerbi_relatorio_aprovacao[NOME_TRIBUTO] = _p) + 0
        VAR _vSP = CALCULATE([Honorários aprovados negociação ajuizamento], vw_powerbi_relatorio_aprovacao[Regional] = "Regional Sudeste", FORMAT(vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR], "yyyy-MM") = _d, vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026, 6, 12), vw_powerbi_relatorio_aprovacao[NOME_TRIBUTO] = _p) + 0
        VAR _vSudeste = CALCULATE([Honorários aprovados negociação ajuizamento], vw_powerbi_relatorio_aprovacao[Regional] = "Regional Sudeste 2", FORMAT(vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR], "yyyy-MM") = _d, vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026, 6, 12), vw_powerbi_relatorio_aprovacao[NOME_TRIBUTO] = _p) + 0
        VAR _vNNCO = CALCULATE([Honorários aprovados negociação ajuizamento], vw_powerbi_relatorio_aprovacao[Regional] = "Regional NNCO", FORMAT(vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR], "yyyy-MM") = _d, vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026, 6, 12), vw_powerbi_relatorio_aprovacao[NOME_TRIBUTO] = _p) + 0
        VAR _vSul_sr = CALCULATE([Honorários aprovados negociação ajuizamento], vw_powerbi_relatorio_aprovacao[Regional] = "Regional Sul", FORMAT(vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR], "yyyy-MM") = _d, vw_powerbi_relatorio_aprovacao[NOME_TRIBUTO] = _p) + 0
        VAR _vSP_sr = CALCULATE([Honorários aprovados negociação ajuizamento], vw_powerbi_relatorio_aprovacao[Regional] = "Regional Sudeste", FORMAT(vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR], "yyyy-MM") = _d, vw_powerbi_relatorio_aprovacao[NOME_TRIBUTO] = _p) + 0
        VAR _vSudeste_sr = CALCULATE([Honorários aprovados negociação ajuizamento], vw_powerbi_relatorio_aprovacao[Regional] = "Regional Sudeste 2", FORMAT(vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR], "yyyy-MM") = _d, vw_powerbi_relatorio_aprovacao[NOME_TRIBUTO] = _p) + 0
        VAR _vNNCO_sr = CALCULATE([Honorários aprovados negociação ajuizamento], vw_powerbi_relatorio_aprovacao[Regional] = "Regional NNCO", FORMAT(vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR], "yyyy-MM") = _d, vw_powerbi_relatorio_aprovacao[NOME_TRIBUTO] = _p) + 0
        VAR _somaDia_sr = _vSul_sr + _vSP_sr + _vSudeste_sr + _vNNCO_sr
        RETURN IF(_somaDia_sr > 0,
            "<span class='dado-apneg-ajuiz' data-regional='Regional Sul' data-valor='" & FORMAT(_vSul, "0.00") & "' data-valor-sr='" & FORMAT(_vSul_sr, "0.00") & "' data-data='" & _d & "' data-produto='" & _p & "'></span>" &
            "<span class='dado-apneg-ajuiz' data-regional='Regional Sudeste' data-valor='" & FORMAT(_vSP, "0.00") & "' data-valor-sr='" & FORMAT(_vSP_sr, "0.00") & "' data-data='" & _d & "' data-produto='" & _p & "'></span>" &
            "<span class='dado-apneg-ajuiz' data-regional='Regional Sudeste 2' data-valor='" & FORMAT(_vSudeste, "0.00") & "' data-valor-sr='" & FORMAT(_vSudeste_sr, "0.00") & "' data-data='" & _d & "' data-produto='" & _p & "'></span>" &
            "<span class='dado-apneg-ajuiz' data-regional='Regional NNCO' data-valor='" & FORMAT(_vNNCO, "0.00") & "' data-valor-sr='" & FORMAT(_vNNCO_sr, "0.00") & "' data-data='" & _d & "' data-produto='" & _p & "'></span>",
            ""
        ),
        ""
    )
"""

dax = dax.replace("/* ================== ESTRUTURA DAS LINHAS DA TABELA ================== */", dados_apneg_total + "\n/* ================== ESTRUTURA DAS LINHAS DA TABELA ================== */")

# 3. Add Line definitions for Aprovados em Negociação
linhas_apneg = """VAR _linha_apneg = 
    "<tr onclick=""toggleDetails('detalhe-apneg')"" style='cursor:pointer;' onmouseover=""this.style.background='rgba(255,255,255,0.03)'"" onmouseout=""this.style.background='transparent'"">" &
        "<td><div style='display:flex; align-items:flex-start; gap:8px;'><span id='icon-apneg' style='font-size:16px; color:var(--text-muted); margin-top:4px; transition:0.2s;'>&#9654;</span><div><div style='font-size:18px; font-weight:600; letter-spacing: 0.5px; color:var(--text-main); margin-bottom:4px;'>&#129309; Honorários Aprovados em Negociação</div><div style='font-size:13px; color:var(--text-muted); font-weight:400; text-transform: uppercase; letter-spacing: 0.5px;'>Negociação para Execução</div></div></div></td>" &
        "<td id='apneg-sul'>R$ 0,00<div class='progress-container'><div class='progress-bar' style='width: 0%;'></div></div></td>" &
        "<td id='apneg-sp'>R$ 0,00<div class='progress-container'><div class='progress-bar' style='width: 0%;'></div></div></td>" &
        "<td id='apneg-sd'>R$ 0,00<div class='progress-container'><div class='progress-bar' style='width: 0%;'></div></div></td>" &
        "<td id='apneg-nn'>R$ 0,00<div class='progress-container'><div class='progress-bar' style='width: 0%;'></div></div></td>" &
        "<td id='apneg-total' style='color:var(--accent); font-weight:700; font-size:24px; font-weight:600; font-variant-numeric: tabular-nums; letter-spacing: -1px;'>R$ 0,00</td>" &
    "</tr>"

VAR _linha_apneg_detalhes = 
    "<tr class='detalhe-apneg' style='display:none; background: rgba(255,255,255,0.015);'>" &
        "<td style='padding-left: 40px; font-size:12px; color:var(--text-sec); border-left: 2px solid var(--accent);'><div style='display:flex; align-items:center; gap:8px;'><span style='font-size:14px; color:var(--accent);'>&#128269;</span> Honorários Iniciais</div></td>" &
        "<td id='apneg-hi-sul' style='font-size:12px; color:var(--text-sec);'>R$ 0,00</td>" &
        "<td id='apneg-hi-sp' style='font-size:12px; color:var(--text-sec);'>R$ 0,00</td>" &
        "<td id='apneg-hi-sd' style='font-size:12px; color:var(--text-sec);'>R$ 0,00</td>" &
        "<td id='apneg-hi-nn' style='font-size:12px; color:var(--text-sec);'>R$ 0,00</td>" &
        "<td id='apneg-hi-total' style='font-size:24px; font-weight:600; font-variant-numeric: tabular-nums; letter-spacing: -1px; color:var(--accent); font-weight:600;'>R$ 0,00</td>" &
    "</tr>" &
    "<tr class='detalhe-apneg' style='display:none; background: rgba(255,255,255,0.015);'>" &
        "<td style='padding-left: 40px; font-size:12px; color:var(--text-sec); border-left: 2px solid var(--accent);'><div style='display:flex; align-items:center; gap:8px;'><span style='font-size:14px; color:var(--accent);'>&#128269;</span> Honorários Compensação</div></td>" &
        "<td id='apneg-hc-sul' style='font-size:12px; color:var(--text-sec);'>R$ 0,00</td>" &
        "<td id='apneg-hc-sp' style='font-size:12px; color:var(--text-sec);'>R$ 0,00</td>" &
        "<td id='apneg-hc-sd' style='font-size:12px; color:var(--text-sec);'>R$ 0,00</td>" &
        "<td id='apneg-hc-nn' style='font-size:12px; color:var(--text-sec);'>R$ 0,00</td>" &
        "<td id='apneg-hc-total' style='font-size:24px; font-weight:600; font-variant-numeric: tabular-nums; letter-spacing: -1px; color:var(--accent); font-weight:600;'>R$ 0,00</td>" &
    "</tr>" &
    "<tr class='detalhe-apneg' style='display:none; background: rgba(255,255,255,0.015);'>" &
        "<td style='padding-left: 40px; font-size:12px; color:var(--text-sec); border-left: 2px solid var(--accent);'><div style='display:flex; align-items:center; gap:8px;'><span style='font-size:14px; color:var(--accent);'>&#128269;</span> Honorários Restituição</div></td>" &
        "<td id='apneg-hr-sul' style='font-size:12px; color:var(--text-sec);'>R$ 0,00</td>" &
        "<td id='apneg-hr-sp' style='font-size:12px; color:var(--text-sec);'>R$ 0,00</td>" &
        "<td id='apneg-hr-sd' style='font-size:12px; color:var(--text-sec);'>R$ 0,00</td>" &
        "<td id='apneg-hr-nn' style='font-size:12px; color:var(--text-sec);'>R$ 0,00</td>" &
        "<td id='apneg-hr-total' style='font-size:24px; font-weight:600; font-variant-numeric: tabular-nums; letter-spacing: -1px; color:var(--accent); font-weight:600;'>R$ 0,00</td>" &
    "</tr>" &
    "<tr class='detalhe-apneg' style='display:none; background: rgba(255,255,255,0.015);'>" &
        "<td style='padding-left: 40px; font-size:12px; color:var(--text-sec); border-left: 2px solid var(--accent); border-bottom-left-radius: 8px;'><div style='display:flex; align-items:center; gap:8px;'><span style='font-size:14px; color:var(--accent);'>&#128269;</span> Honorários Ajuizamento</div></td>" &
        "<td id='apneg-ha-sul' style='font-size:12px; color:var(--text-sec);'>R$ 0,00</td>" &
        "<td id='apneg-ha-sp' style='font-size:12px; color:var(--text-sec);'>R$ 0,00</td>" &
        "<td id='apneg-ha-sd' style='font-size:12px; color:var(--text-sec);'>R$ 0,00</td>" &
        "<td id='apneg-ha-nn' style='font-size:12px; color:var(--text-sec);'>R$ 0,00</td>" &
        "<td id='apneg-ha-total' style='font-size:24px; font-weight:600; font-variant-numeric: tabular-nums; letter-spacing: -1px; color:var(--accent); font-weight:600;'>R$ 0,00</td>" &
    "</tr>"
"""

dax = dax.replace("VAR _linha2 = ", linhas_apneg + "\nVAR _linha2 = ")

# 4. Add the Card before Honorários Aprovados
card_apneg = """            "<div class='card'>" &
                "<div class='card-title'>&#129309; Honorários Aprov. Negociação</div>" &
                "<div class='card-value' id='card-aprov-negoc'>R$ 0,00</div>" &
                "<div><span class='card-indicator ind-up'>&#8593; 0%</span> <span style='font-size:11px;color:var(--text-muted);'>vs mês ant.</span></div>" &
                "<button class='btn-kpi-detalhar'>DETALHAR</button>" &
            "</div>" &"""

card_aprov_marker = """            "<div class='card'>" &
                "<div class='card-title'>&#10004;&#65039; Honorários Aprovados</div>\""""

dax = dax.replace(card_aprov_marker, card_apneg + "\n" + card_aprov_marker)

# 5. Add to tbody: _linha_apneg & _linha_apneg_detalhes before _linha2
dax = dax.replace("_linha0 & _linha1 &  _linha2 & _linha2_detalhes", "_linha0 & _linha1 & _linha_apneg & _linha_apneg_detalhes & _linha2 & _linha2_detalhes")

# 6. Add hidden containers
containers_apneg = """    "<div style='display:none;' id='dados-apneg-total-container'>" & _dadosAprovNegocTotal & "</div>" &
    "<div style='display:none;' id='dados-apneg-iniciais-container'>" & _dadosAprovNegocIniciais & "</div>" &
    "<div style='display:none;' id='dados-apneg-comp-container'>" & _dadosAprovNegocComp & "</div>" &
    "<div style='display:none;' id='dados-apneg-rest-container'>" & _dadosAprovNegocRest & "</div>" &
    "<div style='display:none;' id='dados-apneg-ajuiz-container'>" & _dadosAprovNegocAjuiz & "</div>" &"""

dax = dax.replace("<div style='display:none;' id='dados-aprov-total-container'>", containers_apneg + "\n    \"<div style='display:none;' id='dados-aprov-total-container'>")

# 7. Add calculation inside filtrarTudo()
calc_apneg_js = """        /* CALCULAR APROVADOS EM NEGOCIAÇÃO */
        var sApNegTotal = calcularSoma('dado-apneg-total');
        var sApNegIniciais = calcularSoma('dado-apneg-iniciais');
        var sApNegComp = calcularSoma('dado-apneg-comp');
        var sApNegRest = calcularSoma('dado-apneg-rest');
        var sApNegAjuiz = calcularSoma('dado-apneg-ajuiz');

        var elCardApNeg = document.getElementById('card-aprov-negoc');
        if(elCardApNeg) elCardApNeg.innerText = formatarMilhoes(sApNegTotal['Total']);

        var elApnSul = document.getElementById('apneg-sul'); if(elApnSul) elApnSul.innerText = formatarMoeda(sApNegTotal['Regional Sul']);
        var elApnSP = document.getElementById('apneg-sp'); if(elApnSP) elApnSP.innerText = formatarMoeda(sApNegTotal['Regional Sudeste']);
        var elApnSD = document.getElementById('apneg-sd'); if(elApnSD) elApnSD.innerText = formatarMoeda(sApNegTotal['Regional Sudeste 2']);
        var elApnNN = document.getElementById('apneg-nn'); if(elApnNN) elApnNN.innerText = formatarMoeda(sApNegTotal['Regional NNCO']);
        var elApnTot = document.getElementById('apneg-total'); if(elApnTot) elApnTot.innerText = formatarMoeda(sApNegTotal['Total']);

        var elApnHiSul = document.getElementById('apneg-hi-sul'); if(elApnHiSul) elApnHiSul.innerText = formatarMoeda(sApNegIniciais['Regional Sul']);
        var elApnHiSP = document.getElementById('apneg-hi-sp'); if(elApnHiSP) elApnHiSP.innerText = formatarMoeda(sApNegIniciais['Regional Sudeste']);
        var elApnHiSD = document.getElementById('apneg-hi-sd'); if(elApnHiSD) elApnHiSD.innerText = formatarMoeda(sApNegIniciais['Regional Sudeste 2']);
        var elApnHiNN = document.getElementById('apneg-hi-nn'); if(elApnHiNN) elApnHiNN.innerText = formatarMoeda(sApNegIniciais['Regional NNCO']);
        var elApnHiTot = document.getElementById('apneg-hi-total'); if(elApnHiTot) elApnHiTot.innerText = formatarMoeda(sApNegIniciais['Total']);

        var elApnHcSul = document.getElementById('apneg-hc-sul'); if(elApnHcSul) elApnHcSul.innerText = formatarMoeda(sApNegComp['Regional Sul']);
        var elApnHcSP = document.getElementById('apneg-hc-sp'); if(elApnHcSP) elApnHcSP.innerText = formatarMoeda(sApNegComp['Regional Sudeste']);
        var elApnHcSD = document.getElementById('apneg-hc-sd'); if(elApnHcSD) elApnHcSD.innerText = formatarMoeda(sApNegComp['Regional Sudeste 2']);
        var elApnHcNN = document.getElementById('apneg-hc-nn'); if(elApnHcNN) elApnHcNN.innerText = formatarMoeda(sApNegComp['Regional NNCO']);
        var elApnHcTot = document.getElementById('apneg-hc-total'); if(elApnHcTot) elApnHcTot.innerText = formatarMoeda(sApNegComp['Total']);

        var elApnHrSul = document.getElementById('apneg-hr-sul'); if(elApnHrSul) elApnHrSul.innerText = formatarMoeda(sApNegRest['Regional Sul']);
        var elApnHrSP = document.getElementById('apneg-hr-sp'); if(elApnHrSP) elApnHrSP.innerText = formatarMoeda(sApNegRest['Regional Sudeste']);
        var elApnHrSD = document.getElementById('apneg-hr-sd'); if(elApnHrSD) elApnHrSD.innerText = formatarMoeda(sApNegRest['Regional Sudeste 2']);
        var elApnHrNN = document.getElementById('apneg-hr-nn'); if(elApnHrNN) elApnHrNN.innerText = formatarMoeda(sApNegRest['Regional NNCO']);
        var elApnHrTot = document.getElementById('apneg-hr-total'); if(elApnHrTot) elApnHrTot.innerText = formatarMoeda(sApNegRest['Total']);

        var elApnHaSul = document.getElementById('apneg-ha-sul'); if(elApnHaSul) elApnHaSul.innerText = formatarMoeda(sApNegAjuiz['Regional Sul']);
        var elApnHaSP = document.getElementById('apneg-ha-sp'); if(elApnHaSP) elApnHaSP.innerText = formatarMoeda(sApNegAjuiz['Regional Sudeste']);
        var elApnHaSD = document.getElementById('apneg-ha-sd'); if(elApnHaSD) elApnHaSD.innerText = formatarMoeda(sApNegAjuiz['Regional Sudeste 2']);
        var elApnHaNN = document.getElementById('apneg-ha-nn'); if(elApnHaNN) elApnHaNN.innerText = formatarMoeda(sApNegAjuiz['Regional NNCO']);
        var elApnHaTot = document.getElementById('apneg-ha-total'); if(elApnHaTot) elApnHaTot.innerText = formatarMoeda(sApNegAjuiz['Total']);"""

dax = dax.replace("/* CALCULAR APROVADOS (INICIAIS + COMP + RETIF + AJUIZ) */", calc_apneg_js + "\n\n        /* CALCULAR APROVADOS (INICIAIS + COMP + RETIF + AJUIZ) */")

with open('matriz_perfect.dax', 'w', encoding='utf-8-sig') as f:
    f.write(dax)

print("Saved matriz_perfect.dax successfully with BOM")

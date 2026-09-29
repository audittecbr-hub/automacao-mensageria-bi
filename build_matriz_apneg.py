import json
import re

with open('matriz_updated.dax', 'r', encoding='utf-8') as f:
    dax = f.read()

# Replace any old measure references with clean unaccented names
dax = dax.replace("[Honorários encontrados]", "[Honorarios encontrados]")
dax = dax.replace("[Honorários apresentados]", "[Honorarios apresentados]")
dax = dax.replace("[Honorários aprovados]", "[Honorarios aprovados]")
dax = dax.replace("[Honorários perdidos]", "[Honorarios perdidos]")
dax = dax.replace("[Honorários não aprovados]", "[Honorarios nao aprovados]")
dax = dax.replace("[Honorários em negociação]", "[Honorarios em negociacao]")
dax = dax.replace("[Honorário negociação]", "[Honorarios em negociacao]")

# 1. Update CSS for 8 columns in summary-cards
dax = dax.replace(
    ".summary-cards { display: grid; grid-template-columns: repeat(7, 1fr); gap: 15px; margin-bottom: 30px; position: relative; z-index: 1; }",
    ".summary-cards { display: grid; grid-template-columns: repeat(8, 1fr); gap: 12px; margin-bottom: 30px; position: relative; z-index: 1; }\n.card-title { font-size: 15px; color: var(--text-sec); text-transform: uppercase; letter-spacing: 0.5px; font-weight: 600; display:flex; align-items:center; gap:6px; }\n.card-value { font-size: 26px; font-weight: 700; color: var(--text-main); font-family: var(--font); letter-spacing: -0.5px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }"
)

# 2. Add Data Extraction blocks for Aprovados em Negociação
dados_apneg_total = """VAR _dadosAprovNegocTotal = 
    CONCATENATEX(
        _datas_produtos,
        VAR _d = [AnoMes]
        VAR _p = [FiltroProduto]
        VAR _vSul = CALCULATE([Honorarios aprovados em negociacao], vw_powerbi_relatorio_aprovacao[Regional] = "Regional Sul", FORMAT(vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR], "yyyy-MM") = _d, vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026, 6, 12), vw_powerbi_relatorio_aprovacao[NOME_TRIBUTO] = _p) + 0
        VAR _vSP = CALCULATE([Honorarios aprovados em negociacao], vw_powerbi_relatorio_aprovacao[Regional] = "Regional Sudeste", FORMAT(vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR], "yyyy-MM") = _d, vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026, 6, 12), vw_powerbi_relatorio_aprovacao[NOME_TRIBUTO] = _p) + 0
        VAR _vSudeste = CALCULATE([Honorarios aprovados em negociacao], vw_powerbi_relatorio_aprovacao[Regional] = "Regional Sudeste 2", FORMAT(vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR], "yyyy-MM") = _d, vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026, 6, 12), vw_powerbi_relatorio_aprovacao[NOME_TRIBUTO] = _p) + 0
        VAR _vNNCO = CALCULATE([Honorarios aprovados em negociacao], vw_powerbi_relatorio_aprovacao[Regional] = "Regional NNCO", FORMAT(vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR], "yyyy-MM") = _d, vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026, 6, 12), vw_powerbi_relatorio_aprovacao[NOME_TRIBUTO] = _p) + 0
        VAR _vOutras = CALCULATE([Honorarios aprovados em negociacao], vw_powerbi_relatorio_aprovacao[Regional] = "Outras", FORMAT(vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR], "yyyy-MM") = _d, vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026, 6, 12), vw_powerbi_relatorio_aprovacao[NOME_TRIBUTO] = _p) + 0
        VAR _vSul_sr = CALCULATE([Honorarios aprovados em negociacao], vw_powerbi_relatorio_aprovacao[Regional] = "Regional Sul", FORMAT(vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR], "yyyy-MM") = _d, vw_powerbi_relatorio_aprovacao[NOME_TRIBUTO] = _p) + 0
        VAR _vSP_sr = CALCULATE([Honorarios aprovados em negociacao], vw_powerbi_relatorio_aprovacao[Regional] = "Regional Sudeste", FORMAT(vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR], "yyyy-MM") = _d, vw_powerbi_relatorio_aprovacao[NOME_TRIBUTO] = _p) + 0
        VAR _vSudeste_sr = CALCULATE([Honorarios aprovados em negociacao], vw_powerbi_relatorio_aprovacao[Regional] = "Regional Sudeste 2", FORMAT(vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR], "yyyy-MM") = _d, vw_powerbi_relatorio_aprovacao[NOME_TRIBUTO] = _p) + 0
        VAR _vNNCO_sr = CALCULATE([Honorarios aprovados em negociacao], vw_powerbi_relatorio_aprovacao[Regional] = "Regional NNCO", FORMAT(vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR], "yyyy-MM") = _d, vw_powerbi_relatorio_aprovacao[NOME_TRIBUTO] = _p) + 0
        VAR _vOutras_sr = CALCULATE([Honorarios aprovados em negociacao], vw_powerbi_relatorio_aprovacao[Regional] = "Outras", FORMAT(vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR], "yyyy-MM") = _d, vw_powerbi_relatorio_aprovacao[NOME_TRIBUTO] = _p) + 0
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
        VAR _vSul = CALCULATE([Honorarios aprovados negociacao iniciais], vw_powerbi_relatorio_aprovacao[Regional] = "Regional Sul", FORMAT(vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR], "yyyy-MM") = _d, vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026, 6, 12), vw_powerbi_relatorio_aprovacao[NOME_TRIBUTO] = _p) + 0
        VAR _vSP = CALCULATE([Honorarios aprovados negociacao iniciais], vw_powerbi_relatorio_aprovacao[Regional] = "Regional Sudeste", FORMAT(vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR], "yyyy-MM") = _d, vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026, 6, 12), vw_powerbi_relatorio_aprovacao[NOME_TRIBUTO] = _p) + 0
        VAR _vSudeste = CALCULATE([Honorarios aprovados negociacao iniciais], vw_powerbi_relatorio_aprovacao[Regional] = "Regional Sudeste 2", FORMAT(vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR], "yyyy-MM") = _d, vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026, 6, 12), vw_powerbi_relatorio_aprovacao[NOME_TRIBUTO] = _p) + 0
        VAR _vNNCO = CALCULATE([Honorarios aprovados negociacao iniciais], vw_powerbi_relatorio_aprovacao[Regional] = "Regional NNCO", FORMAT(vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR], "yyyy-MM") = _d, vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026, 6, 12), vw_powerbi_relatorio_aprovacao[NOME_TRIBUTO] = _p) + 0
        VAR _vSul_sr = CALCULATE([Honorarios aprovados negociacao iniciais], vw_powerbi_relatorio_aprovacao[Regional] = "Regional Sul", FORMAT(vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR], "yyyy-MM") = _d, vw_powerbi_relatorio_aprovacao[NOME_TRIBUTO] = _p) + 0
        VAR _vSP_sr = CALCULATE([Honorarios aprovados negociacao iniciais], vw_powerbi_relatorio_aprovacao[Regional] = "Regional Sudeste", FORMAT(vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR], "yyyy-MM") = _d, vw_powerbi_relatorio_aprovacao[NOME_TRIBUTO] = _p) + 0
        VAR _vSudeste_sr = CALCULATE([Honorarios aprovados negociacao iniciais], vw_powerbi_relatorio_aprovacao[Regional] = "Regional Sudeste 2", FORMAT(vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR], "yyyy-MM") = _d, vw_powerbi_relatorio_aprovacao[NOME_TRIBUTO] = _p) + 0
        VAR _vNNCO_sr = CALCULATE([Honorarios aprovados negociacao iniciais], vw_powerbi_relatorio_aprovacao[Regional] = "Regional NNCO", FORMAT(vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR], "yyyy-MM") = _d, vw_powerbi_relatorio_aprovacao[NOME_TRIBUTO] = _p) + 0
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
        VAR _vSul = CALCULATE([Honorarios aprovados negociacao compensacao], vw_powerbi_relatorio_aprovacao[Regional] = "Regional Sul", FORMAT(vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR], "yyyy-MM") = _d, vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026, 6, 12), vw_powerbi_relatorio_aprovacao[NOME_TRIBUTO] = _p) + 0
        VAR _vSP = CALCULATE([Honorarios aprovados negociacao compensacao], vw_powerbi_relatorio_aprovacao[Regional] = "Regional Sudeste", FORMAT(vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR], "yyyy-MM") = _d, vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026, 6, 12), vw_powerbi_relatorio_aprovacao[NOME_TRIBUTO] = _p) + 0
        VAR _vSudeste = CALCULATE([Honorarios aprovados negociacao compensacao], vw_powerbi_relatorio_aprovacao[Regional] = "Regional Sudeste 2", FORMAT(vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR], "yyyy-MM") = _d, vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026, 6, 12), vw_powerbi_relatorio_aprovacao[NOME_TRIBUTO] = _p) + 0
        VAR _vNNCO = CALCULATE([Honorarios aprovados negociacao compensacao], vw_powerbi_relatorio_aprovacao[Regional] = "Regional NNCO", FORMAT(vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR], "yyyy-MM") = _d, vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026, 6, 12), vw_powerbi_relatorio_aprovacao[NOME_TRIBUTO] = _p) + 0
        VAR _vSul_sr = CALCULATE([Honorarios aprovados negociacao compensacao], vw_powerbi_relatorio_aprovacao[Regional] = "Regional Sul", FORMAT(vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR], "yyyy-MM") = _d, vw_powerbi_relatorio_aprovacao[NOME_TRIBUTO] = _p) + 0
        VAR _vSP_sr = CALCULATE([Honorarios aprovados negociacao compensacao], vw_powerbi_relatorio_aprovacao[Regional] = "Regional Sudeste", FORMAT(vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR], "yyyy-MM") = _d, vw_powerbi_relatorio_aprovacao[NOME_TRIBUTO] = _p) + 0
        VAR _vSudeste_sr = CALCULATE([Honorarios aprovados negociacao compensacao], vw_powerbi_relatorio_aprovacao[Regional] = "Regional Sudeste 2", FORMAT(vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR], "yyyy-MM") = _d, vw_powerbi_relatorio_aprovacao[NOME_TRIBUTO] = _p) + 0
        VAR _vNNCO_sr = CALCULATE([Honorarios aprovados negociacao compensacao], vw_powerbi_relatorio_aprovacao[Regional] = "Regional NNCO", FORMAT(vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR], "yyyy-MM") = _d, vw_powerbi_relatorio_aprovacao[NOME_TRIBUTO] = _p) + 0
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
        VAR _vSul = CALCULATE([Honorarios aprovados negociacao restituicao], vw_powerbi_relatorio_aprovacao[Regional] = "Regional Sul", FORMAT(vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR], "yyyy-MM") = _d, vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026, 6, 12), vw_powerbi_relatorio_aprovacao[NOME_TRIBUTO] = _p) + 0
        VAR _vSP = CALCULATE([Honorarios aprovados negociacao restituicao], vw_powerbi_relatorio_aprovacao[Regional] = "Regional Sudeste", FORMAT(vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR], "yyyy-MM") = _d, vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026, 6, 12), vw_powerbi_relatorio_aprovacao[NOME_TRIBUTO] = _p) + 0
        VAR _vSudeste = CALCULATE([Honorarios aprovados negociacao restituicao], vw_powerbi_relatorio_aprovacao[Regional] = "Regional Sudeste 2", FORMAT(vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR], "yyyy-MM") = _d, vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026, 6, 12), vw_powerbi_relatorio_aprovacao[NOME_TRIBUTO] = _p) + 0
        VAR _vNNCO = CALCULATE([Honorarios aprovados negociacao restituicao], vw_powerbi_relatorio_aprovacao[Regional] = "Regional NNCO", FORMAT(vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR], "yyyy-MM") = _d, vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026, 6, 12), vw_powerbi_relatorio_aprovacao[NOME_TRIBUTO] = _p) + 0
        VAR _vSul_sr = CALCULATE([Honorarios aprovados negociacao restituicao], vw_powerbi_relatorio_aprovacao[Regional] = "Regional Sul", FORMAT(vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR], "yyyy-MM") = _d, vw_powerbi_relatorio_aprovacao[NOME_TRIBUTO] = _p) + 0
        VAR _vSP_sr = CALCULATE([Honorarios aprovados negociacao restituicao], vw_powerbi_relatorio_aprovacao[Regional] = "Regional Sudeste", FORMAT(vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR], "yyyy-MM") = _d, vw_powerbi_relatorio_aprovacao[NOME_TRIBUTO] = _p) + 0
        VAR _vSudeste_sr = CALCULATE([Honorarios aprovados negociacao restituicao], vw_powerbi_relatorio_aprovacao[Regional] = "Regional Sudeste 2", FORMAT(vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR], "yyyy-MM") = _d, vw_powerbi_relatorio_aprovacao[NOME_TRIBUTO] = _p) + 0
        VAR _vNNCO_sr = CALCULATE([Honorarios aprovados negociacao restituicao], vw_powerbi_relatorio_aprovacao[Regional] = "Regional NNCO", FORMAT(vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR], "yyyy-MM") = _d, vw_powerbi_relatorio_aprovacao[NOME_TRIBUTO] = _p) + 0
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
        VAR _vSul = CALCULATE([Honorarios aprovados negociacao ajuizamento], vw_powerbi_relatorio_aprovacao[Regional] = "Regional Sul", FORMAT(vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR], "yyyy-MM") = _d, vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026, 6, 12), vw_powerbi_relatorio_aprovacao[NOME_TRIBUTO] = _p) + 0
        VAR _vSP = CALCULATE([Honorarios aprovados negociacao ajuizamento], vw_powerbi_relatorio_aprovacao[Regional] = "Regional Sudeste", FORMAT(vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR], "yyyy-MM") = _d, vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026, 6, 12), vw_powerbi_relatorio_aprovacao[NOME_TRIBUTO] = _p) + 0
        VAR _vSudeste = CALCULATE([Honorarios aprovados negociacao ajuizamento], vw_powerbi_relatorio_aprovacao[Regional] = "Regional Sudeste 2", FORMAT(vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR], "yyyy-MM") = _d, vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026, 6, 12), vw_powerbi_relatorio_aprovacao[NOME_TRIBUTO] = _p) + 0
        VAR _vNNCO = CALCULATE([Honorarios aprovados negociacao ajuizamento], vw_powerbi_relatorio_aprovacao[Regional] = "Regional NNCO", FORMAT(vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR], "yyyy-MM") = _d, vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026, 6, 12), vw_powerbi_relatorio_aprovacao[NOME_TRIBUTO] = _p) + 0
        VAR _vSul_sr = CALCULATE([Honorarios aprovados negociacao ajuizamento], vw_powerbi_relatorio_aprovacao[Regional] = "Regional Sul", FORMAT(vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR], "yyyy-MM") = _d, vw_powerbi_relatorio_aprovacao[NOME_TRIBUTO] = _p) + 0
        VAR _vSP_sr = CALCULATE([Honorarios aprovados negociacao ajuizamento], vw_powerbi_relatorio_aprovacao[Regional] = "Regional Sudeste", FORMAT(vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR], "yyyy-MM") = _d, vw_powerbi_relatorio_aprovacao[NOME_TRIBUTO] = _p) + 0
        VAR _vSudeste_sr = CALCULATE([Honorarios aprovados negociacao ajuizamento], vw_powerbi_relatorio_aprovacao[Regional] = "Regional Sudeste 2", FORMAT(vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR], "yyyy-MM") = _d, vw_powerbi_relatorio_aprovacao[NOME_TRIBUTO] = _p) + 0
        VAR _vNNCO_sr = CALCULATE([Honorarios aprovados negociacao ajuizamento], vw_powerbi_relatorio_aprovacao[Regional] = "Regional NNCO", FORMAT(vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR], "yyyy-MM") = _d, vw_powerbi_relatorio_aprovacao[NOME_TRIBUTO] = _p) + 0
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

# Insert data extraction before `VAR _linha0`
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
card_apneg = """            <div class='card'>
                <div class='card-title'>&#129309; Honorários Aprov. Negociação</div>
                <div class='card-value' id='card-aprov-negoc'>R$ 0,00</div>
                <div><span class='card-indicator ind-up'>&#8593; 0%</span> <span style='font-size:11px;color:var(--text-muted);'>vs mês ant.</span></div>
                <button class='btn-kpi-detalhar'>DETALHAR</button>
            </div>"""

old_card_aprov = """            <div class='card'>
                <div class='card-title'>&#10004;&#65039; Honorários Aprovados</div>"""

dax = dax.replace(old_card_aprov, card_apneg + "\n" + old_card_aprov)

# 5. Add to tbody: _linha_apneg & _linha_apneg_detalhes before _linha2
dax = dax.replace("_linha0 & _linha1 &  _linha2 & _linha2_detalhes", "_linha0 & _linha1 & _linha_apneg & _linha_apneg_detalhes & _linha2 & _linha2_detalhes")

# 6. Add hidden containers
containers_apneg = """    <div style='display:none;' id='dados-apneg-total-container'>" & _dadosAprovNegocTotal & "</div>" &
    "<div style='display:none;' id='dados-apneg-iniciais-container'>" & _dadosAprovNegocIniciais & "</div>" &
    "<div style='display:none;' id='dados-apneg-comp-container'>" & _dadosAprovNegocComp & "</div>" &
    "<div style='display:none;' id='dados-apneg-rest-container'>" & _dadosAprovNegocRest & "</div>" &
    "<div style='display:none;' id='dados-apneg-ajuiz-container'>" & _dadosAprovNegocAjuiz & "</div>" &"""

dax = dax.replace("<div style='display:none;' id='dados-aprov-total-container'>", containers_apneg + "\n    <div style='display:none;' id='dados-aprov-total-container'>")

# 7. Add calculation inside filtrarTudo()
calc_apneg_js = """        /* CALCULAR APROVADOS EM NEGOCIAÇÃO */
        var sApNegTotal = calcularSoma('dado-apneg-total');
        var sApNegIniciais = calcularSoma('dado-apneg-iniciais');
        var sApNegComp = calcularSoma('dado-apneg-comp');
        var sApNegRest = calcularSoma('dado-apneg-rest');
        var sApNegAjuiz = calcularSoma('dado-apneg-ajuiz');

        document.getElementById('card-aprov-negoc').innerText = formatarMilhoes(sApNegTotal['Total']);
        document.getElementById('apneg-sul').innerText = formatarMoeda(sApNegTotal['Regional Sul']);
        document.getElementById('apneg-sp').innerText = formatarMoeda(sApNegTotal['Regional Sudeste']);
        document.getElementById('apneg-sd').innerText = formatarMoeda(sApNegTotal['Regional Sudeste 2']);
        document.getElementById('apneg-nn').innerText = formatarMoeda(sApNegTotal['Regional NNCO']);
        document.getElementById('apneg-total').innerText = formatarMoeda(sApNegTotal['Total']);

        document.getElementById('apneg-hi-sul').innerText = formatarMoeda(sApNegIniciais['Regional Sul']);
        document.getElementById('apneg-hi-sp').innerText = formatarMoeda(sApNegIniciais['Regional Sudeste']);
        document.getElementById('apneg-hi-sd').innerText = formatarMoeda(sApNegIniciais['Regional Sudeste 2']);
        document.getElementById('apneg-hi-nn').innerText = formatarMoeda(sApNegIniciais['Regional NNCO']);
        document.getElementById('apneg-hi-total').innerText = formatarMoeda(sApNegIniciais['Total']);

        document.getElementById('apneg-hc-sul').innerText = formatarMoeda(sApNegComp['Regional Sul']);
        document.getElementById('apneg-hc-sp').innerText = formatarMoeda(sApNegComp['Regional Sudeste']);
        document.getElementById('apneg-hc-sd').innerText = formatarMoeda(sApNegComp['Regional Sudeste 2']);
        document.getElementById('apneg-hc-nn').innerText = formatarMoeda(sApNegComp['Regional NNCO']);
        document.getElementById('apneg-hc-total').innerText = formatarMoeda(sApNegComp['Total']);

        document.getElementById('apneg-hr-sul').innerText = formatarMoeda(sApNegRest['Regional Sul']);
        document.getElementById('apneg-hr-sp').innerText = formatarMoeda(sApNegRest['Regional Sudeste']);
        document.getElementById('apneg-hr-sd').innerText = formatarMoeda(sApNegRest['Regional Sudeste 2']);
        document.getElementById('apneg-hr-nn').innerText = formatarMoeda(sApNegRest['Regional NNCO']);
        document.getElementById('apneg-hr-total').innerText = formatarMoeda(sApNegRest['Total']);

        document.getElementById('apneg-ha-sul').innerText = formatarMoeda(sApNegAjuiz['Regional Sul']);
        document.getElementById('apneg-ha-sp').innerText = formatarMoeda(sApNegAjuiz['Regional Sudeste']);
        document.getElementById('apneg-ha-sd').innerText = formatarMoeda(sApNegAjuiz['Regional Sudeste 2']);
        document.getElementById('apneg-ha-nn').innerText = formatarMoeda(sApNegAjuiz['Regional NNCO']);
        document.getElementById('apneg-ha-total').innerText = formatarMoeda(sApNegAjuiz['Total']);"""

dax = dax.replace("/* CALCULAR APROVADOS (INICIAIS + COMP + RETIF + AJUIZ) */", calc_apneg_js + "\n\n        /* CALCULAR APROVADOS (INICIAIS + COMP + RETIF + AJUIZ) */")

with open('matriz_with_apneg.dax', 'w', encoding='utf-8') as f:
    f.write(dax)

print("Saved clean matriz_with_apneg.dax successfully")

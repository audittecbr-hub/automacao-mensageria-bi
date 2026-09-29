import json
import re

# 1. Read existing Mockup_Honorarios_Matriz.dax
with open('Mockup_Honorarios_Matriz.dax', 'r', encoding='utf-8') as f:
    mockup_code = f.read()

# Replace _dadosAprovados block
old_dados_aprov = """VAR _dadosAprovados = 
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

        VAR _vSul = CALCULATE(SUMX(vw_powerbi_honorarios_iniciais, vw_powerbi_honorarios_iniciais[RF_VALOR] + 0), vw_powerbi_honorarios_iniciais[REGIONAL_DEFAULT] = 1, FORMAT(vw_powerbi_honorarios_iniciais[DATA_CADASTRO], "yyyy-MM") = _d, vw_powerbi_honorarios_iniciais[PRODUTO] = _p) + 0
        VAR _vSP = CALCULATE(SUMX(vw_powerbi_honorarios_iniciais, vw_powerbi_honorarios_iniciais[RF_VALOR] + 0), vw_powerbi_honorarios_iniciais[REGIONAL_DEFAULT] = 2, FORMAT(vw_powerbi_honorarios_iniciais[DATA_CADASTRO], "yyyy-MM") = _d, vw_powerbi_honorarios_iniciais[PRODUTO] = _p) + 0
        VAR _vSudeste = CALCULATE(SUMX(vw_powerbi_honorarios_iniciais, vw_powerbi_honorarios_iniciais[RF_VALOR] + 0), vw_powerbi_honorarios_iniciais[REGIONAL_DEFAULT] = 3, FORMAT(vw_powerbi_honorarios_iniciais[DATA_CADASTRO], "yyyy-MM") = _d, vw_powerbi_honorarios_iniciais[PRODUTO] = _p) + 0
        VAR _vNNCO = CALCULATE(SUMX(vw_powerbi_honorarios_iniciais, vw_powerbi_honorarios_iniciais[RF_VALOR] + 0), vw_powerbi_honorarios_iniciais[REGIONAL_DEFAULT] = 14, FORMAT(vw_powerbi_honorarios_iniciais[DATA_CADASTRO], "yyyy-MM") = _d, vw_powerbi_honorarios_iniciais[PRODUTO] = _p) + 0
        VAR _somaDia = _vSul + _vSP + _vSudeste + _vNNCO
        RETURN IF(_somaDia > 0,
            "<span class='dado-aprov' data-regional='Regional Sul' data-valor='" & FORMAT(_vSul, "0.00") & "' data-data='" & _d & "' data-produto='" & _p & "'></span>" &
            "<span class='dado-aprov' data-regional='Regional Sudeste' data-valor='" & FORMAT(_vSP, "0.00") & "' data-data='" & _d & "' data-produto='" & _p & "'></span>" &
            "<span class='dado-aprov' data-regional='Regional Sudeste 2' data-valor='" & FORMAT(_vSudeste, "0.00") & "' data-data='" & _d & "' data-produto='" & _p & "'></span>" &
            "<span class='dado-aprov' data-regional='Regional NNCO' data-valor='" & FORMAT(_vNNCO, "0.00") & "' data-data='" & _d & "' data-produto='" & _p & "'></span>",
            ""
        ),
        ""
    )"""

new_dados_aprov = """VAR _dadosAprovados = 
    CONCATENATEX(
        _datas_produtos,
        VAR _d = [AnoMes]
        VAR _p = [FiltroProduto]
        VAR _vSul = CALCULATE(SUMX(vw_powerbi_relatorio_aprovacao, COALESCE(vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_HONORARIOS_INICIAIS], vw_powerbi_relatorio_aprovacao[HONORARIOS_INICIAIS], 0) + 0), vw_powerbi_relatorio_aprovacao[Regional] = "Regional Sul", FORMAT(vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR], "yyyy-MM") = _d, vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026, 6, 12), vw_powerbi_relatorio_aprovacao[NOME_TRIBUTO] = _p) + 0
        VAR _vSP = CALCULATE(SUMX(vw_powerbi_relatorio_aprovacao, COALESCE(vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_HONORARIOS_INICIAIS], vw_powerbi_relatorio_aprovacao[HONORARIOS_INICIAIS], 0) + 0), vw_powerbi_relatorio_aprovacao[Regional] = "Regional Sudeste", FORMAT(vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR], "yyyy-MM") = _d, vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026, 6, 12), vw_powerbi_relatorio_aprovacao[NOME_TRIBUTO] = _p) + 0
        VAR _vSudeste = CALCULATE(SUMX(vw_powerbi_relatorio_aprovacao, COALESCE(vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_HONORARIOS_INICIAIS], vw_powerbi_relatorio_aprovacao[HONORARIOS_INICIAIS], 0) + 0), vw_powerbi_relatorio_aprovacao[Regional] = "Regional Sudeste 2", FORMAT(vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR], "yyyy-MM") = _d, vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026, 6, 12), vw_powerbi_relatorio_aprovacao[NOME_TRIBUTO] = _p) + 0
        VAR _vNNCO = CALCULATE(SUMX(vw_powerbi_relatorio_aprovacao, COALESCE(vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_HONORARIOS_INICIAIS], vw_powerbi_relatorio_aprovacao[HONORARIOS_INICIAIS], 0) + 0), vw_powerbi_relatorio_aprovacao[Regional] = "Regional NNCO", FORMAT(vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR], "yyyy-MM") = _d, vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026, 6, 12), vw_powerbi_relatorio_aprovacao[NOME_TRIBUTO] = _p) + 0
        VAR _somaDia = _vSul + _vSP + _vSudeste + _vNNCO
        RETURN IF(_somaDia > 0,
            "<span class='dado-aprov' data-regional='Regional Sul' data-valor='" & FORMAT(_vSul, "0.00") & "' data-data='" & _d & "' data-produto='" & _p & "'></span>" &
            "<span class='dado-aprov' data-regional='Regional Sudeste' data-valor='" & FORMAT(_vSP, "0.00") & "' data-data='" & _d & "' data-produto='" & _p & "'></span>" &
            "<span class='dado-aprov' data-regional='Regional Sudeste 2' data-valor='" & FORMAT(_vSudeste, "0.00") & "' data-data='" & _d & "' data-produto='" & _p & "'></span>" &
            "<span class='dado-aprov' data-regional='Regional NNCO' data-valor='" & FORMAT(_vNNCO, "0.00") & "' data-data='" & _d & "' data-produto='" & _p & "'></span>",
            ""
        ),
        ""
    )"""

# Replace _dadosCompensacao block
old_dados_comp = """VAR _dadosCompensacao = 
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

        VAR _vSul = CALCULATE(SUMX(vw_powerbi_regionais_hono_compensacao, vw_powerbi_regionais_hono_compensacao[valor_final] + 0), vw_powerbi_regionais_hono_compensacao[REGIONAL_DEFAULT] = 1, FORMAT(vw_powerbi_regionais_hono_compensacao[DATA], "yyyy-MM") = _d, vw_powerbi_regionais_hono_compensacao[PRODUTO] = _p) + 0
        VAR _vSP = CALCULATE(SUMX(vw_powerbi_regionais_hono_compensacao, vw_powerbi_regionais_hono_compensacao[valor_final] + 0), vw_powerbi_regionais_hono_compensacao[REGIONAL_DEFAULT] = 2, FORMAT(vw_powerbi_regionais_hono_compensacao[DATA], "yyyy-MM") = _d, vw_powerbi_regionais_hono_compensacao[PRODUTO] = _p) + 0
        VAR _vSudeste = CALCULATE(SUMX(vw_powerbi_regionais_hono_compensacao, vw_powerbi_regionais_hono_compensacao[valor_final] + 0), vw_powerbi_regionais_hono_compensacao[REGIONAL_DEFAULT] = 3, FORMAT(vw_powerbi_regionais_hono_compensacao[DATA], "yyyy-MM") = _d, vw_powerbi_regionais_hono_compensacao[PRODUTO] = _p) + 0
        VAR _vNNCO = CALCULATE(SUMX(vw_powerbi_regionais_hono_compensacao, vw_powerbi_regionais_hono_compensacao[valor_final] + 0), vw_powerbi_regionais_hono_compensacao[REGIONAL_DEFAULT] = 14, FORMAT(vw_powerbi_regionais_hono_compensacao[DATA], "yyyy-MM") = _d, vw_powerbi_regionais_hono_compensacao[PRODUTO] = _p) + 0
        VAR _somaDia = _vSul + _vSP + _vSudeste + _vNNCO
        RETURN IF(_somaDia > 0,
            "<span class='dado-comp' data-regional='Regional Sul' data-valor='" & FORMAT(_vSul, "0.00") & "' data-data='" & _d & "' data-produto='" & _p & "'></span>" &
            "<span class='dado-comp' data-regional='Regional Sudeste' data-valor='" & FORMAT(_vSP, "0.00") & "' data-data='" & _d & "' data-produto='" & _p & "'></span>" &
            "<span class='dado-comp' data-regional='Regional Sudeste 2' data-valor='" & FORMAT(_vSudeste, "0.00") & "' data-data='" & _d & "' data-produto='" & _p & "'></span>" &
            "<span class='dado-comp' data-regional='Regional NNCO' data-valor='" & FORMAT(_vNNCO, "0.00") & "' data-data='" & _d & "' data-produto='" & _p & "'></span>",
            ""
        ),
        ""
    )"""

new_dados_comp = """VAR _dadosCompensacao = 
    CONCATENATEX(
        _datas_produtos,
        VAR _d = [AnoMes]
        VAR _p = [FiltroProduto]
        VAR _vSul = CALCULATE(SUM(vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_COMPENSACAO]), vw_powerbi_relatorio_aprovacao[Regional] = "Regional Sul", FORMAT(vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR], "yyyy-MM") = _d, vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026, 6, 12), vw_powerbi_relatorio_aprovacao[NOME_TRIBUTO] = _p) + 0
        VAR _vSP = CALCULATE(SUM(vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_COMPENSACAO]), vw_powerbi_relatorio_aprovacao[Regional] = "Regional Sudeste", FORMAT(vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR], "yyyy-MM") = _d, vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026, 6, 12), vw_powerbi_relatorio_aprovacao[NOME_TRIBUTO] = _p) + 0
        VAR _vSudeste = CALCULATE(SUM(vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_COMPENSACAO]), vw_powerbi_relatorio_aprovacao[Regional] = "Regional Sudeste 2", FORMAT(vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR], "yyyy-MM") = _d, vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026, 6, 12), vw_powerbi_relatorio_aprovacao[NOME_TRIBUTO] = _p) + 0
        VAR _vNNCO = CALCULATE(SUM(vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_COMPENSACAO]), vw_powerbi_relatorio_aprovacao[Regional] = "Regional NNCO", FORMAT(vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR], "yyyy-MM") = _d, vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026, 6, 12), vw_powerbi_relatorio_aprovacao[NOME_TRIBUTO] = _p) + 0
        VAR _somaDia = _vSul + _vSP + _vSudeste + _vNNCO
        RETURN IF(_somaDia > 0,
            "<span class='dado-comp' data-regional='Regional Sul' data-valor='" & FORMAT(_vSul, "0.00") & "' data-data='" & _d & "' data-produto='" & _p & "'></span>" &
            "<span class='dado-comp' data-regional='Regional Sudeste' data-valor='" & FORMAT(_vSP, "0.00") & "' data-data='" & _d & "' data-produto='" & _p & "'></span>" &
            "<span class='dado-comp' data-regional='Regional Sudeste 2' data-valor='" & FORMAT(_vSudeste, "0.00") & "' data-data='" & _d & "' data-produto='" & _p & "'></span>" &
            "<span class='dado-comp' data-regional='Regional NNCO' data-valor='" & FORMAT(_vNNCO, "0.00") & "' data-data='" & _d & "' data-produto='" & _p & "'></span>",
            ""
        ),
        ""
    )"""

# Replace _dadosRetificacao block
old_dados_retif = """VAR _dadosRetificacao = 
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

        VAR _vSul = CALCULATE(SUMX(vw_powerbi_regionais_hono_retificacao, vw_powerbi_regionais_hono_retificacao[valor_final] + 0), vw_powerbi_regionais_hono_retificacao[REGIONAL_DEFAULT] = 1, FORMAT(vw_powerbi_regionais_hono_retificacao[DATA], "yyyy-MM") = _d, vw_powerbi_regionais_hono_retificacao[PRODUTO] = _p) + 0
        VAR _vSP = CALCULATE(SUMX(vw_powerbi_regionais_hono_retificacao, vw_powerbi_regionais_hono_retificacao[valor_final] + 0), vw_powerbi_regionais_hono_retificacao[REGIONAL_DEFAULT] = 2, FORMAT(vw_powerbi_regionais_hono_retificacao[DATA], "yyyy-MM") = _d, vw_powerbi_regionais_hono_retificacao[PRODUTO] = _p) + 0
        VAR _vSudeste = CALCULATE(SUMX(vw_powerbi_regionais_hono_retificacao, vw_powerbi_regionais_hono_retificacao[valor_final] + 0), vw_powerbi_regionais_hono_retificacao[REGIONAL_DEFAULT] = 3, FORMAT(vw_powerbi_regionais_hono_retificacao[DATA], "yyyy-MM") = _d, vw_powerbi_regionais_hono_retificacao[PRODUTO] = _p) + 0
        VAR _vNNCO = CALCULATE(SUMX(vw_powerbi_regionais_hono_retificacao, vw_powerbi_regionais_hono_retificacao[valor_final] + 0), vw_powerbi_regionais_hono_retificacao[REGIONAL_DEFAULT] = 14, FORMAT(vw_powerbi_regionais_hono_retificacao[DATA], "yyyy-MM") = _d, vw_powerbi_regionais_hono_retificacao[PRODUTO] = _p) + 0
        VAR _somaDia = _vSul + _vSP + _vSudeste + _vNNCO
        RETURN IF(_somaDia > 0,
            "<span class='dado-retif' data-regional='Regional Sul' data-valor='" & FORMAT(_vSul, "0.00") & "' data-data='" & _d & "' data-produto='" & _p & "'></span>" &
            "<span class='dado-retif' data-regional='Regional Sudeste' data-valor='" & FORMAT(_vSP, "0.00") & "' data-data='" & _d & "' data-produto='" & _p & "'></span>" &
            "<span class='dado-retif' data-regional='Regional Sudeste 2' data-valor='" & FORMAT(_vSudeste, "0.00") & "' data-data='" & _d & "' data-produto='" & _p & "'></span>" &
            "<span class='dado-retif' data-regional='Regional NNCO' data-valor='" & FORMAT(_vNNCO, "0.00") & "' data-data='" & _d & "' data-produto='" & _p & "'></span>",
            ""
        ),
        ""
    )"""

new_dados_retif = """VAR _dadosRetificacao = 
    CONCATENATEX(
        _datas_produtos,
        VAR _d = [AnoMes]
        VAR _p = [FiltroProduto]
        VAR _vSul = CALCULATE(SUM(vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_RESTITUICAO]), vw_powerbi_relatorio_aprovacao[Regional] = "Regional Sul", FORMAT(vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR], "yyyy-MM") = _d, vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026, 6, 12), vw_powerbi_relatorio_aprovacao[NOME_TRIBUTO] = _p) + 0
        VAR _vSP = CALCULATE(SUM(vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_RESTITUICAO]), vw_powerbi_relatorio_aprovacao[Regional] = "Regional Sudeste", FORMAT(vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR], "yyyy-MM") = _d, vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026, 6, 12), vw_powerbi_relatorio_aprovacao[NOME_TRIBUTO] = _p) + 0
        VAR _vSudeste = CALCULATE(SUM(vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_RESTITUICAO]), vw_powerbi_relatorio_aprovacao[Regional] = "Regional Sudeste 2", FORMAT(vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR], "yyyy-MM") = _d, vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026, 6, 12), vw_powerbi_relatorio_aprovacao[NOME_TRIBUTO] = _p) + 0
        VAR _vNNCO = CALCULATE(SUM(vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_RESTITUICAO]), vw_powerbi_relatorio_aprovacao[Regional] = "Regional NNCO", FORMAT(vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR], "yyyy-MM") = _d, vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026, 6, 12), vw_powerbi_relatorio_aprovacao[NOME_TRIBUTO] = _p) + 0
        VAR _somaDia = _vSul + _vSP + _vSudeste + _vNNCO
        RETURN IF(_somaDia > 0,
            "<span class='dado-retif' data-regional='Regional Sul' data-valor='" & FORMAT(_vSul, "0.00") & "' data-data='" & _d & "' data-produto='" & _p & "'></span>" &
            "<span class='dado-retif' data-regional='Regional Sudeste' data-valor='" & FORMAT(_vSP, "0.00") & "' data-data='" & _d & "' data-produto='" & _p & "'></span>" &
            "<span class='dado-retif' data-regional='Regional Sudeste 2' data-valor='" & FORMAT(_vSudeste, "0.00") & "' data-data='" & _d & "' data-produto='" & _p & "'></span>" &
            "<span class='dado-retif' data-regional='Regional NNCO' data-valor='" & FORMAT(_vNNCO, "0.00") & "' data-data='" & _d & "' data-produto='" & _p & "'></span>",
            ""
        ),
        ""
    )"""

# Replace _dadosAjuizamento block
old_dados_ajuiz = """VAR _dadosAjuizamento = 
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

        VAR _vSul = CALCULATE(SUMX(vw_powerbi_regionais_hono_ajuizamento, vw_powerbi_regionais_hono_ajuizamento[valor_final] + 0), vw_powerbi_regionais_hono_ajuizamento[REGIONAL_DEFAULT] = 1, FORMAT(vw_powerbi_regionais_hono_ajuizamento[DATA], "yyyy-MM") = _d, vw_powerbi_regionais_hono_ajuizamento[PRODUTO] = _p) + 0
        VAR _vSP = CALCULATE(SUMX(vw_powerbi_regionais_hono_ajuizamento, vw_powerbi_regionais_hono_ajuizamento[valor_final] + 0), vw_powerbi_regionais_hono_ajuizamento[REGIONAL_DEFAULT] = 2, FORMAT(vw_powerbi_regionais_hono_ajuizamento[DATA], "yyyy-MM") = _d, vw_powerbi_regionais_hono_ajuizamento[PRODUTO] = _p) + 0
        VAR _vSudeste = CALCULATE(SUMX(vw_powerbi_regionais_hono_ajuizamento, vw_powerbi_regionais_hono_ajuizamento[valor_final] + 0), vw_powerbi_regionais_hono_ajuizamento[REGIONAL_DEFAULT] = 3, FORMAT(vw_powerbi_regionais_hono_ajuizamento[DATA], "yyyy-MM") = _d, vw_powerbi_regionais_hono_ajuizamento[PRODUTO] = _p) + 0
        VAR _vNNCO = CALCULATE(SUMX(vw_powerbi_regionais_hono_ajuizamento, vw_powerbi_regionais_hono_ajuizamento[valor_final] + 0), vw_powerbi_regionais_hono_ajuizamento[REGIONAL_DEFAULT] = 14, FORMAT(vw_powerbi_regionais_hono_ajuizamento[DATA], "yyyy-MM") = _d, vw_powerbi_regionais_hono_ajuizamento[PRODUTO] = _p) + 0
        VAR _somaDia = _vSul + _vSP + _vSudeste + _vNNCO
        RETURN IF(_somaDia > 0,
            "<span class='dado-ajuiz' data-regional='Regional Sul' data-valor='" & FORMAT(_vSul, "0.00") & "' data-data='" & _d & "' data-produto='" & _p & "'></span>" &
            "<span class='dado-ajuiz' data-regional='Regional Sudeste' data-valor='" & FORMAT(_vSP, "0.00") & "' data-data='" & _d & "' data-produto='" & _p & "'></span>" &
            "<span class='dado-ajuiz' data-regional='Regional Sudeste 2' data-valor='" & FORMAT(_vSudeste, "0.00") & "' data-data='" & _d & "' data-produto='" & _p & "'></span>" &
            "<span class='dado-ajuiz' data-regional='Regional NNCO' data-valor='" & FORMAT(_vNNCO, "0.00") & "' data-data='" & _d & "' data-produto='" & _p & "'></span>",
            ""
        ),
        ""
    )"""

new_dados_ajuiz = """VAR _dadosAjuizamento = 
    CONCATENATEX(
        _datas_produtos,
        VAR _d = [AnoMes]
        VAR _p = [FiltroProduto]
        VAR _vSul = CALCULATE(SUM(vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_AJUIZAMENTO]), vw_powerbi_relatorio_aprovacao[Regional] = "Regional Sul", FORMAT(vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR], "yyyy-MM") = _d, vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026, 6, 12), vw_powerbi_relatorio_aprovacao[NOME_TRIBUTO] = _p) + 0
        VAR _vSP = CALCULATE(SUM(vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_AJUIZAMENTO]), vw_powerbi_relatorio_aprovacao[Regional] = "Regional Sudeste", FORMAT(vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR], "yyyy-MM") = _d, vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026, 6, 12), vw_powerbi_relatorio_aprovacao[NOME_TRIBUTO] = _p) + 0
        VAR _vSudeste = CALCULATE(SUM(vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_AJUIZAMENTO]), vw_powerbi_relatorio_aprovacao[Regional] = "Regional Sudeste 2", FORMAT(vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR], "yyyy-MM") = _d, vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026, 6, 12), vw_powerbi_relatorio_aprovacao[NOME_TRIBUTO] = _p) + 0
        VAR _vNNCO = CALCULATE(SUM(vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_AJUIZAMENTO]), vw_powerbi_relatorio_aprovacao[Regional] = "Regional NNCO", FORMAT(vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR], "yyyy-MM") = _d, vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026, 6, 12), vw_powerbi_relatorio_aprovacao[NOME_TRIBUTO] = _p) + 0
        VAR _somaDia = _vSul + _vSP + _vSudeste + _vNNCO
        RETURN IF(_somaDia > 0,
            "<span class='dado-ajuiz' data-regional='Regional Sul' data-valor='" & FORMAT(_vSul, "0.00") & "' data-data='" & _d & "' data-produto='" & _p & "'></span>" &
            "<span class='dado-ajuiz' data-regional='Regional Sudeste' data-valor='" & FORMAT(_vSP, "0.00") & "' data-data='" & _d & "' data-produto='" & _p & "'></span>" &
            "<span class='dado-ajuiz' data-regional='Regional Sudeste 2' data-valor='" & FORMAT(_vSudeste, "0.00") & "' data-data='" & _d & "' data-produto='" & _p & "'></span>" &
            "<span class='dado-ajuiz' data-regional='Regional NNCO' data-valor='" & FORMAT(_vNNCO, "0.00") & "' data-data='" & _d & "' data-produto='" & _p & "'></span>",
            ""
        ),
        ""
    )"""

mockup_updated = mockup_code.replace(old_dados_aprov, new_dados_aprov)
mockup_updated = mockup_updated.replace(old_dados_comp, new_dados_comp)
mockup_updated = mockup_updated.replace(old_dados_retif, new_dados_retif)
mockup_updated = mockup_updated.replace(old_dados_ajuiz, new_dados_ajuiz)

# 2. Update [Honorários aprovados]
hono_aprov_expr = """SUMX(
    vw_powerbi_relatorio_aprovacao,
    COALESCE(vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_HONORARIOS_INICIAIS], vw_powerbi_relatorio_aprovacao[HONORARIOS_INICIAIS], 0) +
    COALESCE(vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_COMPENSACAO], 0) +
    COALESCE(vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_RESTITUICAO], 0) +
    COALESCE(vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_AJUIZAMENTO], 0) +
    COALESCE(vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_HONORARIOS_MENSAIS], 0)
)"""

payload = [
    {
        "tableName": "vw_powerbi_relatorio_aprovacao",
        "name": "Honorários aprovados",
        "expression": hono_aprov_expr
    },
    {
        "tableName": "medidas_html",
        "name": "Mockup_Honorarios_Matriz",
        "expression": mockup_updated
    }
]

with open('update_aprovados_payload.json', 'w', encoding='utf-8') as f:
    json.dump(payload, f, ensure_ascii=False, indent=2)

print("Saved update_aprovados_payload.json")

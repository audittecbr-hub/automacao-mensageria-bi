import re

filepath = r"C:\Users\cristhofer.maciel.GRUPOSTUDIO\Downloads\honorarios_regionais (2).SemanticModel\definition\tables\medidas_html.tmdl"

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update _dadosPerdidos block using exact string replacement
old_dados_perdidos = """			VAR _dadosPerdidos = 
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
			
			        VAR _vSul = CALCULATE(SUMX(vw_powerbi_regionais_hono_perdidos, vw_powerbi_regionais_hono_perdidos[VALOR_FINAL] + 0), vw_powerbi_regionais_hono_perdidos[REGIONAL_DEFAULT] = 1, FORMAT(vw_powerbi_regionais_hono_perdidos[DATA], "yyyy-MM") = _d, vw_powerbi_regionais_hono_perdidos[PRODUTO] = _p) + 0
			        VAR _vSP = CALCULATE(SUMX(vw_powerbi_regionais_hono_perdidos, vw_powerbi_regionais_hono_perdidos[VALOR_FINAL] + 0), vw_powerbi_regionais_hono_perdidos[REGIONAL_DEFAULT] = 2, FORMAT(vw_powerbi_regionais_hono_perdidos[DATA], "yyyy-MM") = _d, vw_powerbi_regionais_hono_perdidos[PRODUTO] = _p) + 0
			        VAR _vSudeste = CALCULATE(SUMX(vw_powerbi_regionais_hono_perdidos, vw_powerbi_regionais_hono_perdidos[VALOR_FINAL] + 0), vw_powerbi_regionais_hono_perdidos[REGIONAL_DEFAULT] = 3, FORMAT(vw_powerbi_regionais_hono_perdidos[DATA], "yyyy-MM") = _d, vw_powerbi_regionais_hono_perdidos[PRODUTO] = _p) + 0
			        VAR _vNNCO = CALCULATE(SUMX(vw_powerbi_regionais_hono_perdidos, vw_powerbi_regionais_hono_perdidos[VALOR_FINAL] + 0), vw_powerbi_regionais_hono_perdidos[REGIONAL_DEFAULT] = 14, FORMAT(vw_powerbi_regionais_hono_perdidos[DATA], "yyyy-MM") = _d, vw_powerbi_regionais_hono_perdidos[PRODUTO] = _p) + 0
			        VAR _somaDia = _vSul + _vSP + _vSudeste + _vNNCO
			        RETURN IF(_somaDia > 0,
			            "<span class='dado-perdidos' data-regional='Regional Sul' data-valor='" & FORMAT(_vSul, "0.00") & "' data-data='" & _d & "' data-produto='" & _p & "'></span>" &
			            "<span class='dado-perdidos' data-regional='Regional Sudeste' data-valor='" & FORMAT(_vSP, "0.00") & "' data-data='" & _d & "' data-produto='" & _p & "'></span>" &
			            "<span class='dado-perdidos' data-regional='Regional Sudeste 2' data-valor='" & FORMAT(_vSudeste, "0.00") & "' data-data='" & _d & "' data-produto='" & _p & "'></span>" &
			            "<span class='dado-perdidos' data-regional='Regional NNCO' data-valor='" & FORMAT(_vNNCO, "0.00") & "' data-data='" & _d & "' data-produto='" & _p & "'></span>",
			            ""
			        ),
			        ""
			    )"""

new_dados_perdidos = """			VAR _dadosPerdidos = 
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
			
			        VAR _vSul = CALCULATE([Honorários perdidos], vw_powerbi_relatorio_aprovacao[Regional] = "Regional Sul", FORMAT(vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR], "yyyy-MM") = _d, vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026, 6, 12), vw_powerbi_relatorio_aprovacao[NOME_TRIBUTO] = _p) + 0
			        VAR _vSP = CALCULATE([Honorários perdidos], vw_powerbi_relatorio_aprovacao[Regional] = "Regional Sudeste", FORMAT(vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR], "yyyy-MM") = _d, vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026, 6, 12), vw_powerbi_relatorio_aprovacao[NOME_TRIBUTO] = _p) + 0
			        VAR _vSudeste = CALCULATE([Honorários perdidos], vw_powerbi_relatorio_aprovacao[Regional] = "Regional Sudeste 2", FORMAT(vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR], "yyyy-MM") = _d, vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026, 6, 12), vw_powerbi_relatorio_aprovacao[NOME_TRIBUTO] = _p) + 0
			        VAR _vNNCO = CALCULATE([Honorários perdidos], vw_powerbi_relatorio_aprovacao[Regional] = "Regional NNCO", FORMAT(vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR], "yyyy-MM") = _d, vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026, 6, 12), vw_powerbi_relatorio_aprovacao[NOME_TRIBUTO] = _p) + 0
			        VAR _vOutras = CALCULATE([Honorários perdidos], vw_powerbi_relatorio_aprovacao[Regional] = "Outras", FORMAT(vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR], "yyyy-MM") = _d, vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026, 6, 12), vw_powerbi_relatorio_aprovacao[NOME_TRIBUTO] = _p) + 0
			        VAR _somaDia = _vSul + _vSP + _vSudeste + _vNNCO + _vOutras
			        RETURN IF(_somaDia > 0,
			            "<span class='dado-perdidos' data-regional='Regional Sul' data-valor='" & FORMAT(_vSul, "0.00") & "' data-data='" & _d & "' data-produto='" & _p & "'></span>" &
			            "<span class='dado-perdidos' data-regional='Regional Sudeste' data-valor='" & FORMAT(_vSP, "0.00") & "' data-data='" & _d & "' data-produto='" & _p & "'></span>" &
			            "<span class='dado-perdidos' data-regional='Regional Sudeste 2' data-valor='" & FORMAT(_vSudeste, "0.00") & "' data-data='" & _d & "' data-produto='" & _p & "'></span>" &
			            "<span class='dado-perdidos' data-regional='Regional NNCO' data-valor='" & FORMAT(_vNNCO, "0.00") & "' data-data='" & _d & "' data-produto='" & _p & "'></span>" &
			            "<span class='dado-perdidos' data-regional='Outras' data-valor='" & FORMAT(_vOutras, "0.00") & "' data-data='" & _d & "' data-produto='" & _p & "'></span>",
			            ""
			        ),
			        ""
			    )"""

content = content.replace(old_dados_perdidos, new_dados_perdidos)

# 2. Extract HTML_Detalhamento_Aprovados measure body
aprovados_match = re.search(r"^\tmeasure HTML_Detalhamento_Aprovados = ```\n(.*?)\n\t\t\t```\n\t\tlineageTag", content, flags=re.MULTILINE | re.DOTALL)
if not aprovados_match:
    print("Could not find HTML_Detalhamento_Aprovados")
else:
    aprovados_body = aprovados_match.group(1)
    
    # Modify the body to become Perdidos
    perdidos_body = aprovados_body.replace("[Honorários aprovados]", "[Honorários perdidos]")
    perdidos_body = perdidos_body.replace("HONORÁRIOS APROVADOS", "HONORÁRIOS PERDIDOS")
    perdidos_body = perdidos_body.replace("_linhas_aprovados", "_linhas_perdidos")
    perdidos_body = perdidos_body.replace("<td class='td-tipo'>Aprovado</td>", "<td class='td-tipo'>Perdido</td>")
    # replace "detalhe-aprovados" with "detalhe-perdidos" in case they were there
    
    new_measure = "\tmeasure HTML_Detalhamento_Perdidos = ```\n" + perdidos_body + "\n\t\t\t```\n\t\tlineageTag"
    
    # 3. Replace the old HTML_Detalhamento_Perdidos
    perdidos_regex = r"^\tmeasure HTML_Detalhamento_Perdidos = ```\n(.*?)\n\t\t\t```\n\t\tlineageTag"
    content = re.sub(perdidos_regex, new_measure, content, flags=re.MULTILINE | re.DOTALL)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("Successfully updated file via python script.")

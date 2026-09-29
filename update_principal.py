import re

filepath = r"C:\Users\cristhofer.maciel.GRUPOSTUDIO\Downloads\honorarios_regionais (2).SemanticModel\definition\tables\medidas_html.tmdl"

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Reverse the previous replacement
content = content.replace(
    "FILTER(ALL(vw_powerbi_relatorio_aprovacao[DATA_RT]), SELECTEDVALUE('Filtro Regra RT'[Opção], \"Habilitar Regra RT\") = \"Desabilitar Regra RT\" || vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026, 6, 12))",
    "vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026, 6, 12)"
)
content = content.replace(
    "(SELECTEDVALUE('Filtro Regra RT'[Opção], \"Habilitar Regra RT\") = \"Desabilitar Regra RT\" || vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026, 6, 12))",
    "vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026, 6, 12)"
)

# 2. Add toggle button to HTML header (in _html)
header_button = "\"<label class='dropdown-btn' style='cursor:pointer; user-select:none; width:auto; border-color:var(--orange); color:var(--orange);'><input type='checkbox' id='chkRegraRt' onchange='filtrarTudo();' style='margin-right:8px;' checked> REGRA RT 12/06/2026</label>\" &"
content = content.replace(
    "\"<div class='dropdown' id='produtoDropdown'>\" &",
    header_button + "\n\t\t\t                     " + "\"<div class='dropdown' id='produtoDropdown'>\" &"
)

# 3. Modify HTML_Principal blocks
# We will use regex to find the blocks that calculate the spans
pattern = re.compile(
    r"(VAR _vSul = CALCULATE\(\[([^\]]+)\].*?vw_powerbi_relatorio_aprovacao\[DATA_RT\] >= DATE\(2026, 6, 12\).*?\)\s*\+\s*0\n"
    r"\s*VAR _vSP =.*?\n"
    r"\s*VAR _vSudeste =.*?\n"
    r"\s*VAR _vNNCO =.*?\n"
    r"\s*VAR _vOutras =.*?\n"
    r"\s*VAR _somaDia =.*?_vOutras\n"
    r"\s*RETURN IF\(_somaDia > 0,\n"
    r"(?:\s*\"<span class='([^']+)' data-regional='[^']+' data-valor='\" & FORMAT\(_[^,]+, \"0\.00\"\) & \"' data-data='\" & _d & \"' data-produto='\" & _p & \"'></span>\" &\n){4}"
    r"\s*\"<span class='([^']+)' data-regional='[^']+' data-valor='\" & FORMAT\(_[^,]+, \"0\.00\"\) & \"' data-data='\" & _d & \"' data-produto='\" & _p & \"'></span>\",\n"
    r"\s*\"\"\n"
    r"\s*\),\n"
    r"\s*\"\""
    r")", re.DOTALL
)

def replace_block(match):
    original_block = match.group(1)
    measure_name = match.group(2)
    span_class = match.group(3)
    
    # We reconstruct the whole block
    new_block = f"""VAR _vSul = CALCULATE([{measure_name}], vw_powerbi_relatorio_aprovacao[Regional] = "Regional Sul", FORMAT(vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR], "yyyy-MM") = _d, vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026, 6, 12), vw_powerbi_relatorio_aprovacao[NOME_TRIBUTO] = _p) + 0
			        VAR _vSP = CALCULATE([{measure_name}], vw_powerbi_relatorio_aprovacao[Regional] = "Regional Sudeste", FORMAT(vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR], "yyyy-MM") = _d, vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026, 6, 12), vw_powerbi_relatorio_aprovacao[NOME_TRIBUTO] = _p) + 0
			        VAR _vSudeste = CALCULATE([{measure_name}], vw_powerbi_relatorio_aprovacao[Regional] = "Regional Sudeste 2", FORMAT(vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR], "yyyy-MM") = _d, vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026, 6, 12), vw_powerbi_relatorio_aprovacao[NOME_TRIBUTO] = _p) + 0
			        VAR _vNNCO = CALCULATE([{measure_name}], vw_powerbi_relatorio_aprovacao[Regional] = "Regional NNCO", FORMAT(vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR], "yyyy-MM") = _d, vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026, 6, 12), vw_powerbi_relatorio_aprovacao[NOME_TRIBUTO] = _p) + 0
			        VAR _vOutras = CALCULATE([{measure_name}], vw_powerbi_relatorio_aprovacao[Regional] = "Outras", FORMAT(vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR], "yyyy-MM") = _d, vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026, 6, 12), vw_powerbi_relatorio_aprovacao[NOME_TRIBUTO] = _p) + 0
			        VAR _vSul_sr = CALCULATE([{measure_name}], vw_powerbi_relatorio_aprovacao[Regional] = "Regional Sul", FORMAT(vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR], "yyyy-MM") = _d, vw_powerbi_relatorio_aprovacao[NOME_TRIBUTO] = _p) + 0
			        VAR _vSP_sr = CALCULATE([{measure_name}], vw_powerbi_relatorio_aprovacao[Regional] = "Regional Sudeste", FORMAT(vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR], "yyyy-MM") = _d, vw_powerbi_relatorio_aprovacao[NOME_TRIBUTO] = _p) + 0
			        VAR _vSudeste_sr = CALCULATE([{measure_name}], vw_powerbi_relatorio_aprovacao[Regional] = "Regional Sudeste 2", FORMAT(vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR], "yyyy-MM") = _d, vw_powerbi_relatorio_aprovacao[NOME_TRIBUTO] = _p) + 0
			        VAR _vNNCO_sr = CALCULATE([{measure_name}], vw_powerbi_relatorio_aprovacao[Regional] = "Regional NNCO", FORMAT(vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR], "yyyy-MM") = _d, vw_powerbi_relatorio_aprovacao[NOME_TRIBUTO] = _p) + 0
			        VAR _vOutras_sr = CALCULATE([{measure_name}], vw_powerbi_relatorio_aprovacao[Regional] = "Outras", FORMAT(vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR], "yyyy-MM") = _d, vw_powerbi_relatorio_aprovacao[NOME_TRIBUTO] = _p) + 0
			        VAR _somaDia_sr = _vSul_sr + _vSP_sr + _vSudeste_sr + _vNNCO_sr + _vOutras_sr
			        RETURN IF(_somaDia_sr > 0,
			            "<span class='{span_class}' data-regional='Regional Sul' data-valor='" & FORMAT(_vSul, "0.00") & "' data-valor-sr='" & FORMAT(_vSul_sr, "0.00") & "' data-data='" & _d & "' data-produto='" & _p & "'></span>" &
			            "<span class='{span_class}' data-regional='Regional Sudeste' data-valor='" & FORMAT(_vSP, "0.00") & "' data-valor-sr='" & FORMAT(_vSP_sr, "0.00") & "' data-data='" & _d & "' data-produto='" & _p & "'></span>" &
			            "<span class='{span_class}' data-regional='Regional Sudeste 2' data-valor='" & FORMAT(_vSudeste, "0.00") & "' data-valor-sr='" & FORMAT(_vSudeste_sr, "0.00") & "' data-data='" & _d & "' data-produto='" & _p & "'></span>" &
			            "<span class='{span_class}' data-regional='Regional NNCO' data-valor='" & FORMAT(_vNNCO, "0.00") & "' data-valor-sr='" & FORMAT(_vNNCO_sr, "0.00") & "' data-data='" & _d & "' data-produto='" & _p & "'></span>" &
			            "<span class='{span_class}' data-regional='Outras' data-valor='" & FORMAT(_vOutras, "0.00") & "' data-valor-sr='" & FORMAT(_vOutras_sr, "0.00") & "' data-data='" & _d & "' data-produto='" & _p & "'></span>",
			            ""
			        ),
			        \"\""""
    return new_block

content = pattern.sub(replace_block, content)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated HTML_Principal variables")

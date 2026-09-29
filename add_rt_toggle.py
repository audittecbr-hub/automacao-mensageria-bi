import re

filepath = r"C:\Users\cristhofer.maciel.GRUPOSTUDIO\Downloads\honorarios_regionais (2).SemanticModel\definition\tables\medidas_html.tmdl"

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace(
    ", vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026, 6, 12),",
    ", FILTER(ALL(vw_powerbi_relatorio_aprovacao[DATA_RT]), SELECTEDVALUE('Filtro Regra RT'[Opção], \"Habilitar Regra RT\") = \"Desabilitar Regra RT\" || vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026, 6, 12)),"
)

content = content.replace(
    "&& vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026, 6, 12)",
    "&& (SELECTEDVALUE('Filtro Regra RT'[Opção], \"Habilitar Regra RT\") = \"Desabilitar Regra RT\" || vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026, 6, 12))"
)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Toggle capability added to medidas_html.tmdl")

import re

filepath = r"C:\Users\cristhofer.maciel.GRUPOSTUDIO\Downloads\honorarios_regionais (2).SemanticModel\definition\tables\vw_powerbi_relatorio_aprovacao.tmdl"

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace measure 'Honorários não aprovados'
old_measure = r"\tmeasure 'Honorários não aprovados' = ```\n\t\t\tSUMX\(\n\t\t\t    vw_powerbi_relatorio_aprovacao,\n\t\t\t    VAR _passivo.*?\n\t\t\t\)\n\t\t\t```\n\t\tlineageTag: [a-z0-9\-]+"

new_measure = """\tmeasure 'Honorários não aprovados' =
			CALCULATE(
			    SUM(vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_NAO_APROVADO]),
			    KEEPFILTERS(vw_powerbi_relatorio_aprovacao[AREA_ANTERIOR] = "REUNIÃO TÉCNICA"),
			    KEEPFILTERS(vw_powerbi_relatorio_aprovacao[AREA_ATUAL] = "FIM")
			)
		lineageTag: 3f99ad7a-a60d-4852-9a3e-a886e47dcc47"""

content = re.sub(old_measure, new_measure, content, flags=re.MULTILINE | re.DOTALL)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated vw_powerbi_relatorio_aprovacao.tmdl")

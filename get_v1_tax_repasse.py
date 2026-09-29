v1_medidas = r'C:\Users\cristhofer.maciel.GRUPOSTUDIO\Downloads\Ranking_Metas.SemanticModel\definition\tables\Medidas_Repasse.tmdl'
with open(v1_medidas, 'r', encoding='utf-8') as f:
    text = f.read()

import re
m = re.search(r'measure valor_Tax_Repasse = ```([\s\S]*?)```', text)
if m:
    print("=== valor_Tax_Repasse from Ranking_Metas (V1) ===")
    print(m.group(1))
else:
    print("Not found.")

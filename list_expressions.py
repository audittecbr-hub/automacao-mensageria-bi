import re

exp_path = r'C:\Users\cristhofer.maciel.GRUPOSTUDIO\Downloads\Ranking_Metas_V2.SemanticModel\definition\expressions.tmdl'
with open(exp_path, 'r', encoding='utf-8') as f:
    text = f.read()

names = re.findall(r'^expression\s+([^\=]+)=', text, re.MULTILINE)
for n in names:
    print("Expression:", n.strip())

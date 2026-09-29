import os

rel_path = r'C:\Users\cristhofer.maciel.GRUPOSTUDIO\Downloads\Ranking_Metas_V2.SemanticModel\definition\relationships.tmdl'
with open(rel_path, 'r', encoding='utf-8') as f:
    text = f.read()

print("=== CURRENT relationships.tmdl ===")
print(text)

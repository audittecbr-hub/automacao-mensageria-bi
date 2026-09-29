exp_path = r'C:\Users\cristhofer.maciel.GRUPOSTUDIO\Downloads\Ranking_Metas_V2.SemanticModel\definition\expressions.tmdl'
try:
    with open(exp_path, 'r', encoding='utf-8') as f:
        print(f.read())
except Exception as e:
    print("Error:", e)

import json

measures = [
    "HTML_Detalhamento_Metas_Tax",
    "HTML_Detalhamento_Metas_Corporate",
    "HTML_Detalhamento_Metas_Tecnologia",
    "HTML_Detalhamento_Metas_Educacao",
    "HTML_Detalhamento_Metas_Franchising",
    "HTML_Detalhamento_Metas_Expansao"
]

for name in measures:
    with open(f"final_{name}.dax", "r", encoding="utf-8") as f:
        expr = f.read()
    
    assert '\\' not in expr
    
    req = {
        "connectionName": "PBIDesktop-Ranking_Metas-62970",
        "operation": "Update",
        "definitions": [
            {
                "tableName": "Medidas_HTML",
                "name": name,
                "expression": expr
            }
        ]
    }
    with open(f"req_{name}.json", "w", encoding="utf-8") as out:
        json.dump(req, out, ensure_ascii=False)

print("Generated individual request json files!")

import json

measures = [
    "HTML_Detalhamento_Metas_Tax",
    "HTML_Detalhamento_Metas_Corporate",
    "HTML_Detalhamento_Metas_Tecnologia",
    "HTML_Detalhamento_Metas_Educacao",
    "HTML_Detalhamento_Metas_Franchising",
    "HTML_Detalhamento_Metas_Expansao"
]

all_payloads = []
for name in measures:
    with open(f"final_{name}.dax", "r", encoding="utf-8") as f:
        expr = f.read()
    
    # Assert ZERO backslashes
    assert '\\' not in expr, f"Backslash found in {name}"
    
    payload = {
        "tableName": "Medidas_HTML",
        "name": name,
        "expression": expr
    }
    all_payloads.append(payload)

with open("all_clean_payloads.json", "w", encoding="utf-8") as out:
    json.dump(all_payloads, out, ensure_ascii=False)

print("Saved all_clean_payloads.json successfully!")

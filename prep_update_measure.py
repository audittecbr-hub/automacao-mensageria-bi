import json

with open("Painel_Repasses_dax.txt", "r", encoding="utf-8") as f:
    dax_code = f.read()

payload = {
    "request": {
        "operation": "Update",
        "definitions": [
            {
                "name": "Painel_Repasses",
                "tableName": "medidas_html",
                "expression": dax_code
            }
        ]
    }
}

with open("payload_update_measure.json", "w", encoding="utf-8") as f:
    json.dump(payload, f, ensure_ascii=False, indent=2)

print("Saved payload_update_measure.json")

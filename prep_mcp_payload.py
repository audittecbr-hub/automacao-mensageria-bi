with open('Painel_Repasses_Codigo.txt', 'r', encoding='utf8') as f:
    text = f.read()

text = text.replace('👀', 'Ver')

with open('Painel_Repasses_Codigo.txt', 'w', encoding='utf8') as f:
    f.write(text)

import json
payload = {
    "operation": "Update",
    "definitions": [
        {
            "name": "Painel_Repasses",
            "tableName": "medidas_html",
            "expression": text
        }
    ]
}

with open('mcp_payload.json', 'w', encoding='utf8') as f:
    json.dump({"request": payload}, f)

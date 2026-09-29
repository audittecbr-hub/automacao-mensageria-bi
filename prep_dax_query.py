with open('Painel_Repasses_Codigo.txt', 'r', encoding='utf8') as f:
    text = f.read()

# Wrap in EVALUATE
query = "EVALUATE { " + text + " }"

import json
payload = {
    "operation": "Execute",
    "query": query
}

with open('dax_query.json', 'w', encoding='utf8') as f:
    json.dump({"request": payload}, f)

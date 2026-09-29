import json
import urllib.request

with open("Painel_Repasses_dax.txt", "r", encoding="utf-8") as f:
    dax_code = f.read()

# Let's check update_measure.tmsl in automacao-mensageria-bi
tmsl = {
    "createOrReplace": {
        "object": {
            "database": "332a910b-3b5c-4946-8f2e-64833bc4ea95",
            "table": "medidas_html",
            "measure": "Painel_Repasses"
        },
        "measure": {
            "name": "Painel_Repasses",
            "expression": dax_code
        }
    }
}

with open("update_measure.tmsl", "w", encoding="utf-8") as f:
    json.dump(tmsl, f, ensure_ascii=False, indent=2)

print("Saved update_measure.tmsl")

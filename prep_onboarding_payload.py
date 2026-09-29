import json

with open('HTML_Onboarding_Executivo.dax', 'r', encoding='utf-8') as f:
    expression = f.read()

payload = {
    "connectionName": "PBIDesktop-onboarding-57961",
    "operation": "Update",
    "definitions": [
        {
            "tableName": "vw_powerbi_empresas_Onboarding",
            "name": "HTML_Onboarding_Executivo",
            "expression": expression
        }
    ]
}

with open('measure_payload_onboarding.json', 'w', encoding='utf-8') as f:
    json.dump(payload, f, ensure_ascii=False)

print("Saved measure_payload_onboarding.json")

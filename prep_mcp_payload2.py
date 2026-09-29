with open('Painel_Repasses_Codigo.txt', 'r', encoding='utf8') as f:
    text = f.read()

# Let's find VAR _html = 
start = text.find('VAR _html = ')
if start != -1:
    # Just take everything before _html and return it as a string
    short_dax = text[:start] + 'RETURN "Short DAX test"'
    import json
    payload = {
        "operation": "Update",
        "definitions": [
            {
                "name": "Painel_Repasses",
                "tableName": "medidas_html",
                "expression": short_dax
            }
        ]
    }
    with open('mcp_payload2.json', 'w', encoding='utf8') as f:
        json.dump({"request": payload}, f)

import os
import json
import urllib.request

path = r'c:\Users\cristhofer.maciel.GRUPOSTUDIO\OneDrive\repasse.SemanticModel\definition\tables\medidas_html.tmdl'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Extract measure Painel_Repasses
idx = content.find('measure Painel_Repasses =')
if idx == -1:
    idx = content.find("measure 'Painel_Repasses' =")

measure_chunk = content[idx:]
# The expression in TMDL is after `measure Painel_Repasses = ` or `measure Painel_Repasses =\n```\n`
# Let's extract the DAX expression
if '```' in measure_chunk:
    start_expr = measure_chunk.find('```') + 3
    end_expr = measure_chunk.find('```', start_expr)
    expr = measure_chunk[start_expr:end_expr].strip()
else:
    # multi-line indented
    lines = measure_chunk.splitlines()
    expr_lines = []
    for line in lines[1:]:
        if line.startswith('\t\t') or line.startswith('\t\t\t') or line.startswith('    '):
            expr_lines.append(line.lstrip('\t'))
        elif line.startswith('\tformatString:') or line.startswith('\tlineageTag:') or line.startswith('\tmeasure '):
            break
        else:
            expr_lines.append(line)
    expr = '\n'.join(expr_lines).strip()

print('Extracted DAX length:', len(expr))
print('Contains SB_URL:', 'SB_URL' in expr)
print('Contains Supabase:', 'supabase.co' in expr)

# Write to json request for measure_operations
req_data = {
    "request": {
        "connectionName": "PBIDesktop-repasse-57503",
        "operation": "Update",
        "definitions": [
            {
                "tableName": "medidas_html",
                "name": "Painel_Repasses",
                "expression": expr
            }
        ]
    }
}

with open('update_repasse_mcp_req.json', 'w', encoding='utf-8') as f_out:
    json.dump(req_data, f_out, ensure_ascii=False, indent=2)
print('Saved update_repasse_mcp_req.json')

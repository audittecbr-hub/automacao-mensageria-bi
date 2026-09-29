import json

def get_expr(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data['results']

for r in get_expr(r'C:\Users\cristhofer.maciel.GRUPOSTUDIO\.gemini\antigravity-ide\brain\86a55459-41f9-4a50-8a31-1a8a8f9a51d5\.system_generated\steps\2279\output.txt'):
    name = r['data']['name']
    expr = r['data']['expression']
    # find where _tabelaRaw or _tabelaCalc starts
    lines = expr.split('\n')
    print(f"=== {name} ===")
    for i, line in enumerate(lines):
        if '_tabelaRaw' in line or '_tabelaCalc' in line or '_Total' in line or 'CONCATENATEX' in line:
            print(f"L{i+1}: {line}")

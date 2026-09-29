import json

with open(r'C:\Users\cristhofer.maciel.GRUPOSTUDIO\.gemini\antigravity-ide\brain\86a55459-41f9-4a50-8a31-1a8a8f9a51d5\.system_generated\steps\2058\output.txt', 'r', encoding='utf-8') as f:
    data = json.load(f)

for r in data['results']:
    name = r['data']['name']
    if name == 'KPI_TAX':
        expr = r['data'].get('expression', '')
        print("=== KPI_TAX ===")
        # Print the bottom HTML where REPASSE and TOTAL are formatted
        lines = expr.split('\n')
        for idx, l in enumerate(lines, 1):
            if any(k in l.lower() for k in ['total', 'repasse', 'liquido', 'tax']):
                print(f"Line {idx}: {l}")

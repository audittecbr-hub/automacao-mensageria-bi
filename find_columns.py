import json

with open(r'C:\Users\cristhofer.maciel.GRUPOSTUDIO\.gemini\antigravity-ide\brain\86a55459-41f9-4a50-8a31-1a8a8f9a51d5\.system_generated\steps\2326\output.txt', 'r', encoding='utf-8') as f:
    data = json.load(f)

for table in data['data']:
    tname = table['tableName']
    cols = [c['name'] for c in table['columns']]
    for c in cols:
        if 'ENCONTRADO' in c.upper() or 'TOTAL' in c.upper() or 'HONORARIO' in c.upper():
            print(f"Table: {tname} -> Column: {c}")

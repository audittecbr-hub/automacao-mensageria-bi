import json

with open(r'C:\Users\cristhofer.maciel.GRUPOSTUDIO\.gemini\antigravity-ide\brain\86a55459-41f9-4a50-8a31-1a8a8f9a51d5\.system_generated\steps\1678\output.txt', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"Total measures: {len(data['measures'])}")
measures = data['measures']

for m in measures:
    name = m['name']
    table = m['tableName']
    expr = m.get('expression', '')
    
    # Check if there is any backslash in DAX part (outside strings or inside strings where not allowed)
    lines = expr.split('\n')
    for idx, line in enumerate(lines, 1):
        if '\\' in line:
            print(f"[{table}].[{name}] line {idx}: {line}")

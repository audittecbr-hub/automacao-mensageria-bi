import json

with open(r'C:\Users\cristhofer.maciel.GRUPOSTUDIO\.gemini\antigravity-ide\brain\86a55459-41f9-4a50-8a31-1a8a8f9a51d5\.system_generated\steps\2048\output.txt', 'r', encoding='utf-8') as f:
    data = json.load(f)

for r in data['results']:
    name = r['data']['name']
    table = r['data']['tableName']
    expr = r['data'].get('expression', '')
    print(f"=== {table}[{name}] ===")
    print(expr)
    print()

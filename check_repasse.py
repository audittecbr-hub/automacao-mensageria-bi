import json

with open(r'C:\Users\cristhofer.maciel.GRUPOSTUDIO\.gemini\antigravity-ide\brain\86a55459-41f9-4a50-8a31-1a8a8f9a51d5\.system_generated\steps\1821\output.txt', 'r', encoding='utf-8') as f:
    data = json.load(f)

for r in data['results']:
    if not r.get('success', False):
        print("Failed ref in Repasse:", r)
        continue
    name = r['data']['name']
    expr = r['data'].get('expression', '')
    if 'SYNTAXERROR' in expr or '\\' in expr:
        print(f"REPASSE FOUND: {name}")
print("Repasse checked")

import json

with open(r'C:\Users\cristhofer.maciel.GRUPOSTUDIO\.gemini\antigravity-ide\brain\86a55459-41f9-4a50-8a31-1a8a8f9a51d5\.system_generated\steps\1797\output.txt', 'r', encoding='utf-8') as f:
    data = json.load(f)

for r in data['results']:
    name = r['data']['name']
    if name in ['HTML_Detalhamento_Metas_Franchising', 'HTML_Detalhamento_Metas_Expansao']:
        expr = r['data'].get('expression', '')
        lines = expr.split('\n')
        print(f"=== {name} ({len(lines)} lines) ===")
        for idx, l in enumerate(lines, 1):
            if '\\' in l:
                print(f"Line {idx}: {repr(l)}")

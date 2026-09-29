import json

with open(r'C:\Users\cristhofer.maciel.GRUPOSTUDIO\.gemini\antigravity-ide\brain\86a55459-41f9-4a50-8a31-1a8a8f9a51d5\.system_generated\steps\1628\output.txt', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Let's inspect where backslashes are in each result
for r in data['results']:
    name = r['data']['name']
    expr = r['data']['expression']
    lines = expr.split('\n')
    for idx, l in enumerate(lines, 1):
        if '\\' in l:
            print(f"{name} Line {idx}: {repr(l)}")

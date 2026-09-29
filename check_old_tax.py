import json

with open(r'C:\Users\cristhofer.maciel.GRUPOSTUDIO\.gemini\antigravity-ide\brain\86a55459-41f9-4a50-8a31-1a8a8f9a51d5\.system_generated\steps\1749\output.txt', 'r', encoding='utf-8') as f:
    data = json.load(f)

expr = data['results'][0]['data'].get('expression', '')
print("Length of HTML_Detalhamento_Tax:", len(expr))
lines = expr.split('\n')
for idx, l in enumerate(lines, 1):
    if '\\' in l or 'SYNTAXERROR' in l:
        print(f"Line {idx}: {repr(l)}")

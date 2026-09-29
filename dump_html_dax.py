import json

with open(r'C:\Users\cristhofer.maciel.GRUPOSTUDIO\.gemini\antigravity-ide\brain\86a55459-41f9-4a50-8a31-1a8a8f9a51d5\.system_generated\steps\2342\output.txt', 'r', encoding='utf-8') as f:
    data = json.load(f)

for r in data['results']:
    name = r['data']['name']
    expr = r['data']['expression']
    if name == 'Mockup_Honorarios_Matriz':
        with open('Mockup_Honorarios_Matriz.dax', 'w', encoding='utf-8') as f:
            f.write(expr)
        print("Saved Mockup_Honorarios_Matriz.dax")
    elif name == 'HTML_Detalhamento_Encontrados':
        with open('HTML_Detalhamento_Encontrados.dax', 'w', encoding='utf-8') as f:
            f.write(expr)
        print("Saved HTML_Detalhamento_Encontrados.dax")

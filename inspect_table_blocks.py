import json

# Let's inspect the exact lines around _tabelaRaw and _tabelaCalc for all 6 measures
measures_to_check = [
    ("HTML_Detalhamento_Metas_Tax", r"C:\Users\cristhofer.maciel.GRUPOSTUDIO\.gemini\antigravity-ide\brain\86a55459-41f9-4a50-8a31-1a8a8f9a51d5\.system_generated\steps\2269\output.txt"),
    ("HTML_Detalhamento_Metas_Corporate", r"C:\Users\cristhofer.maciel.GRUPOSTUDIO\.gemini\antigravity-ide\brain\86a55459-41f9-4a50-8a31-1a8a8f9a51d5\.system_generated\steps\2279\output.txt"),
    ("HTML_Detalhamento_Metas_Tecnologia", r"C:\Users\cristhofer.maciel.GRUPOSTUDIO\.gemini\antigravity-ide\brain\86a55459-41f9-4a50-8a31-1a8a8f9a51d5\.system_generated\steps\2279\output.txt"),
    ("HTML_Detalhamento_Metas_Educacao", r"C:\Users\cristhofer.maciel.GRUPOSTUDIO\.gemini\antigravity-ide\brain\86a55459-41f9-4a50-8a31-1a8a8f9a51d5\.system_generated\steps\2279\output.txt"),
    ("HTML_Detalhamento_Metas_Franchising", r"C:\Users\cristhofer.maciel.GRUPOSTUDIO\.gemini\antigravity-ide\brain\86a55459-41f9-4a50-8a31-1a8a8f9a51d5\.system_generated\steps\2279\output.txt"),
    ("HTML_Detalhamento_Metas_Expansao", r"C:\Users\cristhofer.maciel.GRUPOSTUDIO\.gemini\antigravity-ide\brain\86a55459-41f9-4a50-8a31-1a8a8f9a51d5\.system_generated\steps\2279\output.txt")
]

for mname, fpath in measures_to_check:
    with open(fpath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    for r in data['results']:
        if r['data']['name'] == mname:
            expr = r['data']['expression']
            lines = expr.split('\n')
            print(f"================== {mname} ==================")
            for i, l in enumerate(lines):
                if 170 <= i <= 215:
                    print(f"{i+1}: {l}")

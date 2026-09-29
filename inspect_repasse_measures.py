import pandas as pd
import io

step_path = r"C:\Users\cristhofer.maciel.GRUPOSTUDIO\.gemini\antigravity-ide\brain\53a8a01a-da38-486b-92ec-ae80b30b913e\.system_generated\steps\966\output.txt"
with open(step_path, 'r', encoding='utf-8') as f:
    text = f.read()

if text.startswith('{"success":true}'): text = text.split('\n', 1)[1]
df = pd.read_csv(io.StringIO(text))

repasse_measures = [
    'valor_Tax_Repasse', 'Valor_Corporate_Repasse', 'Valor_PJ_Repasse',
    'Valor_Expansao_Repasse', 'Valor_Franchising_Repasse', 'Valor_Educacao_Repasse'
]

for idx, r in df.iterrows():
    name = str(r.get('[Name]') or r.get('Name') or '')
    if name in repasse_measures or 'repasse' in name.lower() or 'honorario' in name.lower():
        expr = str(r.get('[Expression]') or r.get('Expression') or '')
        print(f"\n==========================================")
        print(f"MEDIDA: {name}")
        print(f"EXPRESSÃO COMPLETA:\n{expr}")

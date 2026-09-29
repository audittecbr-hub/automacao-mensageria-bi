import pandas as pd
import io

step_path = r"C:\Users\cristhofer.maciel.GRUPOSTUDIO\.gemini\antigravity-ide\brain\53a8a01a-da38-486b-92ec-ae80b30b913e\.system_generated\steps\730\output.txt"
with open(step_path, 'r', encoding='utf-8') as f:
    text = f.read()

if text.startswith('{"success":true}'): text = text.split('\n', 1)[1]
df = pd.read_csv(io.StringIO(text))

print("=== VERIFICANDO PERCENTUAL EM TODAS AS MEDIDAS DO MODELO ===")
for idx, r in df.iterrows():
    name = str(r.get('[Name]') or r.get('Name') or '')
    expr = str(r.get('[Expression]') or r.get('Expression') or '')
    if 'perc_honorarios_job' in expr.lower() or 'vw_powerbi_job_repasse' in expr.lower():
        print(f"\nMeasure: {name}")
        for line in expr.split('\n'):
            if any(k in line.lower() for k in ['perc', 'honorario', 'bloqueado', '1960', 'unidade']):
                print("  ", line.strip()[:100])

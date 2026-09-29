import pandas as pd
import io

step_output_path = r"C:\Users\cristhofer.maciel.GRUPOSTUDIO\.gemini\antigravity-ide\brain\53a8a01a-da38-486b-92ec-ae80b30b913e\.system_generated\steps\593\output.txt"
with open(step_output_path, 'r', encoding='utf-8') as f:
    text = f.read()

if text.startswith('{"success":true}'):
    text = text.split('\n', 1)[1]

df = pd.read_csv(io.StringIO(text))

print("=== BUSCA POR ODACIR / 1960 / JOBS DA UNIDADE 1960 NA METAS ===")
for idx, r in df.iterrows():
    r_str = str(r.to_dict()).upper()
    if any(k in r_str for k in ['1960', 'ODACIR', '84951', '85206', '86675', '85208', '85770', '85771', '364']):
        print(f"ID={r.get('public metas_bruto[id]')} | Omie={r.get('public metas_bruto[codigo_lancamento_omie]')} | Job={r.get('public metas_bruto[numero_contrato]')} | Razao={r.get('public metas_bruto[razao_social]')} | Valor={r.get('public metas_bruto[valor_bruto]')} | Cat={r.get('public metas_bruto[descricao_cat]')} | Dept={r.get('public metas_bruto[descricao_dept]')}")

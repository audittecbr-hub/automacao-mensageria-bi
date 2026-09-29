import pandas as pd

# Load Metas
step_output_path = r"C:\Users\cristhofer.maciel.GRUPOSTUDIO\.gemini\antigravity-ide\brain\53a8a01a-da38-486b-92ec-ae80b30b913e\.system_generated\steps\593\output.txt"
with open(step_output_path, 'r', encoding='utf-8') as f:
    text = f.read()

import io, re
if text.startswith('{"success":true}'): text = text.split('\n', 1)[1]
df_metas = pd.read_csv(io.StringIO(text))

clean_cols = {}
for c in df_metas.columns:
    clean_name = re.sub(r"^public metas_bruto\[(.*)\]$", r"\1", c)
    clean_cols[c] = clean_name
df_metas = df_metas.rename(columns=clean_cols)

print("Total Metas rows:", len(df_metas))

# Filter >= 2026-08-03
df_metas['data_lancamento_clean'] = df_metas['data_lancamento'].fillna('')
df_filtered = df_metas[df_metas['data_lancamento_clean'] >= '2026-08-03'].copy()
print(f"Lançamentos filtrados >= 2026-08-03: {len(df_filtered)}")

# Grouped like in DAX
grouped = df_filtered.groupby(['numero_contrato', 'numero_documento_fiscal', 'bandeira'], dropna=False).agg({
    'cnpj_cpf': 'max',
    'razao_social': 'max',
    'descricao_cat': 'max',
    'data_lancamento': 'max',
    'HonorariosPorJob.honorario': 'max',
    'valor_bruto': 'sum',
    'codigo_lancamento_omie': 'max'
}).reset_index()

print(f"Total de linhas agrupadas no Painel_Repasses: {len(grouped)}")

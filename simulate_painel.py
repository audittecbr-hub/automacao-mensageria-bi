import pandas as pd
import io, re

# Load Metas
step_output_path = r"C:\Users\cristhofer.maciel.GRUPOSTUDIO\.gemini\antigravity-ide\brain\53a8a01a-da38-486b-92ec-ae80b30b913e\.system_generated\steps\593\output.txt"
with open(step_output_path, 'r', encoding='utf-8') as f:
    text = f.read()

if text.startswith('{"success":true}'):
    text = text.split('\n', 1)[1]

df_metas = pd.read_csv(io.StringIO(text))

clean_cols = {}
for c in df_metas.columns:
    clean_name = re.sub(r"^public metas_bruto\[(.*)\]$", r"\1", c)
    clean_cols[c] = clean_name
df_metas = df_metas.rename(columns=clean_cols)

# Load jobs dump
df_jobs = pd.read_csv('vw_jobs_dump.csv', dtype=str)
df_jobs_clean = df_jobs.sort_values(by=['DATA_CADASTRO', 'PERC_HONORARIOS_JOB'], ascending=[False, False]).drop_duplicates(subset=['JOB'])

df_metas['numero_contrato_clean'] = df_metas['numero_contrato'].fillna('').astype(str).str.strip()
df_jobs_clean['JOB_clean'] = df_jobs_clean['JOB'].fillna('').astype(str).str.strip()

merged = pd.merge(
    df_metas,
    df_jobs_clean,
    left_on='numero_contrato_clean',
    right_on='JOB_clean',
    how='left'
)

print(f"Total de registros mesclados: {len(merged)}")

# Check Unidade 1960 specifically
u1960 = merged[merged['UNIDADE_ID'] == '1960']
print(f"\n--- UNIDADE 1960 NO METAS --- ({len(u1960)} registros)")
for idx, r in u1960.iterrows():
    print(f"Omie: {r['codigo_lancamento_omie']} | Job: {r['numero_contrato']} | Razao: {r['razao_social']} | Valor: {r['valor_bruto']} | Perc_Job: {r['PERC_HONORARIOS_JOB']} | Perc_Franq: {r['PERC_HONORARIOS_FRANQUEADO']}")

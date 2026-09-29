import pandas as pd
import io, re

step_output_path = r"C:\Users\cristhofer.maciel.GRUPOSTUDIO\.gemini\antigravity-ide\brain\53a8a01a-da38-486b-92ec-ae80b30b913e\.system_generated\steps\593\output.txt"
with open(step_output_path, 'r', encoding='utf-8') as f:
    text = f.read()

if text.startswith('{"success":true}'): text = text.split('\n', 1)[1]
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

# Filter >= 2026-08-03
merged_aug = merged[merged['data_lancamento'].fillna('') >= '2026-08-03'].copy()

# Anomaly inspection
print(f"Total registros >= 03/08/2026: {len(merged_aug)}")

sem_job = merged_aug[merged_aug['numero_contrato_clean'] == '']
print(f"Sem Contrato / JOB: {len(sem_job)}")

job_nao_cad = merged_aug[(merged_aug['numero_contrato_clean'] != '') & (merged_aug['JOB'].isna())]
print(f"JOB Não Cadastrado na View: {len(job_nao_cad)}")

sem_unidade = merged_aug[(merged_aug['UNIDADE_ID'].isna()) | (merged_aug['UNIDADE_ID'] == '')]
print(f"Sem Unidade Identificada: {len(sem_unidade)}")

print("\n--- AMOSTRA DE JOBS NÃO CADASTRADOS NO PAINEL ---")
for idx, r in job_nao_cad.head(10).iterrows():
    print(f"Omie: {r['codigo_lancamento_omie']} | Contrato: {r['numero_contrato']} | Cliente: {r['razao_social']} | Valor: {r['valor_bruto']}")

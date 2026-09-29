import pandas as pd
import io
import os
import shutil
import re

# 1. Load metas_bruto data from step 593 output.txt
step_output_path = r"C:\Users\cristhofer.maciel.GRUPOSTUDIO\.gemini\antigravity-ide\brain\53a8a01a-da38-486b-92ec-ae80b30b913e\.system_generated\steps\593\output.txt"

with open(step_output_path, 'r', encoding='utf-8') as f:
    raw_text = f.read()

# Remove the first JSON line '{"success":true}\n' if present
if raw_text.startswith('{"success":true}'):
    raw_text = raw_text.split('\n', 1)[1]

df_metas = pd.read_csv(io.StringIO(raw_text))
print(f"Loaded df_metas: {len(df_metas)} rows")

# Rename columns to clean names
clean_cols = {}
for c in df_metas.columns:
    clean_name = re.sub(r"^public metas_bruto\[(.*)\]$", r"\1", c)
    clean_cols[c] = clean_name
df_metas = df_metas.rename(columns=clean_cols)

# 2. Load jobs dump
csv_jobs_path = r"c:\Users\cristhofer.maciel.GRUPOSTUDIO\.gemini\antigravity\scratch\automacao-mensageria-bi\vw_jobs_dump.csv"
df_jobs = pd.read_csv(csv_jobs_path, dtype=str)
print(f"Loaded df_jobs: {len(df_jobs)} rows")

# Deduplicate jobs by taking the row with non-null DATA_CADASTRO and highest PERC_HONORARIOS_JOB
df_jobs_clean = df_jobs.sort_values(by=['DATA_CADASTRO', 'PERC_HONORARIOS_JOB'], ascending=[False, False]).drop_duplicates(subset=['JOB'])

# 3. Merge df_metas with df_jobs_clean on numero_contrato == JOB
df_metas['numero_contrato_str'] = df_metas['numero_contrato'].fillna('').astype(str).str.strip()
df_jobs_clean['JOB_str'] = df_jobs_clean['JOB'].fillna('').astype(str).str.strip()

merged = pd.merge(
    df_metas,
    df_jobs_clean,
    left_on='numero_contrato_str',
    right_on='JOB_str',
    how='left',
    suffixes=('', '_job')
)

print(f"Merged total rows: {len(merged)}")

# Check 75902-AL and 61713 specifically
r_75902 = merged[merged['numero_contrato_str'].str.contains('75902', na=False)]
print(f"Rows for 75902 in merged: {len(r_75902)}")
for _, r in r_75902.iterrows():
    print(f"  ID: {r['id']} | Job: {r['numero_contrato']} | DtCad: {r['DATA_CADASTRO']} | Perc: {r['PERC_HONORARIOS_JOB']} | Unidade: {r['UNIDADE_NOME']}")

r_61713 = merged[merged['numero_contrato_str'] == '61713']
print(f"Rows for 61713 in merged: {len(r_61713)}")
for _, r in r_61713.iterrows():
    print(f"  ID: {r['id']} | Job: {r['numero_contrato']} | DtCad: {r['DATA_CADASTRO']} | Perc: {r['PERC_HONORARIOS_JOB']} | Unidade: {r['UNIDADE_NOME']}")

# Rule Flags
merged['REDE_DISTRIBUICAO'] = merged['REDE_DISTRIBUICAO'].fillna('')
merged['REDE_DISTRIBUICAO_OLD'] = merged['REDE_DISTRIBUICAO_OLD'].fillna('')
merged['UNIDADE_ID'] = merged['UNIDADE_ID'].fillna('')
merged['UNIDADE_NOME'] = merged['UNIDADE_NOME'].fillna('')
merged['PARTICIPANTE_FRANQUEADO'] = merged['PARTICIPANTE_FRANQUEADO'].fillna('')
merged['PARTICIPANTE_CLIENTE'] = merged['PARTICIPANTE_CLIENTE'].fillna('')

merged['is_rede_store_xp'] = merged['REDE_DISTRIBUICAO'].str.upper().str.contains('STORE|XP') | \
                             merged['REDE_DISTRIBUICAO_OLD'].str.upper().str.contains('STORE|XP')

merged['is_piloto_2153'] = (merged['UNIDADE_ID'].astype(str) == '2153') | \
                          merged['UNIDADE_NOME'].str.upper().str.contains('STUDIO CONTABILIDADE LTDA - PILOTO')

part_f = merged['PARTICIPANTE_FRANQUEADO'].str.strip().str.upper()
part_c = merged['PARTICIPANTE_CLIENTE'].str.strip().str.upper()
merged['is_autoconsumo'] = (part_f != '') & (part_c != '') & (part_f == part_c)

merged['is_bloqueado_regra'] = merged['is_rede_store_xp'] | merged['is_piloto_2153'] | merged['is_autoconsumo']

# 1. Sem Contrato / Job lançado
df_sem_contrato = merged[merged['numero_contrato_str'] == ''].copy()

# 2. Com Job mas Sem Data Cadastro
df_com_job = merged[merged['numero_contrato_str'] != ''].copy()
df_sem_data_cad = df_com_job[df_com_job['DATA_CADASTRO'].isna() | (df_com_job['DATA_CADASTRO'].astype(str).str.strip() == '')].copy()

# 3. Anomalias Percentuais (com Job, não bloqueado por regra, mas com % zerado ou nulo)
df_com_job['PERC_HONORARIOS_JOB_num'] = pd.to_numeric(df_com_job['PERC_HONORARIOS_JOB'], errors='coerce').fillna(0)
df_com_job['HonorariosPorJob_honorario_num'] = pd.to_numeric(df_com_job['HonorariosPorJob.honorario'], errors='coerce').fillna(0)
df_com_job['perc_final'] = df_com_job['PERC_HONORARIOS_JOB_num'].where(df_com_job['PERC_HONORARIOS_JOB_num'] > 0, df_com_job['HonorariosPorJob_honorario_num'])

df_anomalia_perc = df_com_job[
    (~df_com_job['is_bloqueado_regra']) & 
    (df_com_job['perc_final'] == 0)
].copy()

print("\n=== RESUMO DAS ABAS ===")
print(f"Aba 1 - Sem Data de Cadastro: {len(df_sem_data_cad)} lançamentos")
print(f"Aba 2 - Sem Contrato/Job: {len(df_sem_contrato)} lançamentos")
print(f"Aba 3 - Anomalias de Percentual Zerado: {len(df_anomalia_perc)} lançamentos")
print(f"Aba 4 - Base Completa Tax/Corporate: {len(merged)} lançamentos")

# Columns to export
export_cols = [
    'id', 'codigo_lancamento_omie', 'data_emissao', 'data_lancamento', 'data_vencimento',
    'bandeira', 'categoria', 'cnpj_cpf', 'razao_social', 'numero_contrato',
    'DATA_CADASTRO', 'PERC_HONORARIOS_JOB', 'HonorariosPorJob.honorario',
    'UNIDADE_ID', 'UNIDADE_NOME', 'PARTICIPANTE_CLIENTE', 'PARTICIPANTE_FRANQUEADO',
    'REDE_DISTRIBUICAO', 'REDE_DISTRIBUICAO_OLD',
    'descricao_cat', 'percentual_categoria', 'ccoddep', 'percentual_departamento',
    'descricao_dept', 'valor_bruto', 'numero_documento', 'numero_documento_fiscal'
]

# Ensure only existing columns
export_cols = [c for c in export_cols if c in merged.columns]

excel_path = r"c:\Users\cristhofer.maciel.GRUPOSTUDIO\.gemini\antigravity\scratch\automacao-mensageria-bi\Relatorio_Anomalias_Tax_Corporate_Ago_Set_2026.xlsx"

with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
    df_sem_data_cad[export_cols].to_excel(writer, sheet_name='Sem_Data_Cadastro', index=False)
    df_sem_contrato[export_cols].to_excel(writer, sheet_name='Sem_Contrato_Job', index=False)
    df_anomalia_perc[export_cols].to_excel(writer, sheet_name='Anomalias_Percentuais', index=False)
    merged[export_cols].to_excel(writer, sheet_name='Base_Completa_Tax_Corp', index=False)

print("\nExcel gravado localmente com sucesso!")

# Copy to Desktop
desktop_path_atualizado = os.path.join(os.path.expanduser("~"), "Desktop", "Relatorio_Anomalias_Tax_Corporate_Ago_Set_2026_Atualizado.xlsx")
shutil.copy2(excel_path, desktop_path_atualizado)
print(f"Excel salvo na Área de Trabalho como: {desktop_path_atualizado}")

try:
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop", "Relatorio_Anomalias_Tax_Corporate_Ago_Set_2026.xlsx")
    shutil.copy2(excel_path, desktop_path)
    print(f"Excel original sobrescrito: {desktop_path}")
except Exception as e:
    print("O arquivo original está aberto no Excel. Criamos a versão atualizada com sufixo _Atualizado.")

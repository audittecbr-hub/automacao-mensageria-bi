import pyodbc
import pandas as pd
import os
import shutil

conn_str = "DRIVER={ODBC Driver 17 for SQL Server};SERVER=192.168.2.34;DATABASE=STUDIO_FISCAL;UID=sa;PWD=Studio@2021;TrustServerCertificate=yes;"
conn = pyodbc.connect(conn_str)

# Query metas_bruto filtered for Tax and Corporate launches >= 2026-08-01
# We join with vw_powerbi_job_repasse to get full job details (including newly fixed data_cadastro)
sql_all = """
SELECT
    m.id,
    m.codigo_lancamento_omie,
    m.data_emissao,
    m.data_lancamento,
    m.data_vencimento,
    m.bandeira,
    m.cnpj_cpf,
    m.razao_social,
    m.numero_contrato,
    m.descricao_cat,
    m.percentual_categoria,
    m.ccoddep,
    m.percentual_departamento,
    m.descricao_dept,
    m.valor_bruto,
    m.categoria,
    m.situacao,
    m.numero_documento,
    m.numero_documento_fiscal,
    j.JOB AS Job_Encontrado,
    j.DATA_CADASTRO AS Job_Data_Cadastro,
    j.PERC_HONORARIOS_JOB AS Job_Perc_Honorarios,
    j.UNIDADE_ID AS Job_Unidade_Id,
    j.UNIDADE_NOME AS Job_Unidade_Nome,
    j.PARTICIPANTE_CLIENTE AS Job_Participante_Cliente,
    j.PARTICIPANTE_FRANQUEADO AS Job_Participante_Franqueado,
    j.REDE_DISTRIBUICAO AS Job_Rede_Distribuicao,
    j.REDE_DISTRIBUICAO_OLD AS Job_Rede_Distribuicao_Old
FROM [public metas_bruto] m WITH (NOLOCK)
LEFT JOIN (
    SELECT 
        JOB,
        MAX(DATA_CADASTRO) AS DATA_CADASTRO,
        MAX(PERC_HONORARIOS_JOB) AS PERC_HONORARIOS_JOB,
        MAX(UNIDADE_ID) AS UNIDADE_ID,
        MAX(UNIDADE_NOME) AS UNIDADE_NOME,
        MAX(PARTICIPANTE_CLIENTE) AS PARTICIPANTE_CLIENTE,
        MAX(PARTICIPANTE_FRANQUEADO) AS PARTICIPANTE_FRANQUEADO,
        MAX(REDE_DISTRIBUICAO) AS REDE_DISTRIBUICAO,
        MAX(REDE_DISTRIBUICAO_OLD) AS REDE_DISTRIBUICAO_OLD
    FROM dbo.vw_powerbi_job_repasse WITH (NOLOCK)
    GROUP BY JOB
) j ON j.JOB = m.numero_contrato
WHERE m.data_lancamento >= '2026-08-01'
  AND (
      m.categoria IN ('TAX', 'Corporate')
      OR m.bandeira LIKE '%TAX%'
      OR m.bandeira LIKE '%CORP%'
      OR m.descricao_dept LIKE '%TAX%'
      OR m.descricao_dept LIKE '%CORP%'
      OR m.descricao_dept LIKE '%Repasse%'
      OR m.descricao_dept LIKE '%Franchising%'
  )
ORDER BY m.data_lancamento DESC, m.id DESC
"""

df = pd.read_sql(sql_all, conn)
conn.close()

print(f"Total registros Tax/Corporate lidos: {len(df)}")

# Flags de regras de bloqueio
df['is_rede_store_xp'] = df['Job_Rede_Distribuicao'].fillna('').str.upper().str.contains('STORE|XP') | \
                          df['Job_Rede_Distribuicao_Old'].fillna('').str.upper().str.contains('STORE|XP')

df['is_piloto_2153'] = (df['Job_Unidade_Id'].astype(str) == '2153') | \
                       df['Job_Unidade_Nome'].fillna('').str.upper().str.contains('STUDIO CONTABILIDADE LTDA - PILOTO')

part_f = df['Job_Participante_Franqueado'].fillna('').str.strip().str.upper()
part_c = df['Job_Participante_Cliente'].fillna('').str.strip().str.upper()
df['is_autoconsumo'] = (part_f != '') & (part_c != '') & (part_f == part_c)

df['is_bloqueado_regra'] = df['is_rede_store_xp'] | df['is_piloto_2153'] | df['is_autoconsumo']

# 1. Sem Contrato / Job lançado
df_sem_contrato = df[df['numero_contrato'].isna() | (df['numero_contrato'].str.strip() == '') | (df['numero_contrato'].str.strip() == '-')].copy()

# 2. Com Job mas Sem Data Cadastro
df_com_job = df[df['numero_contrato'].notna() & (df['numero_contrato'].str.strip() != '') & (df['numero_contrato'].str.strip() != '-')].copy()
df_sem_data_cad = df_com_job[df_com_job['Job_Data_Cadastro'].isna()].copy()

# 3. Anomalias Percentuais (com Job, não bloqueado por regra, mas com % zerado ou nulo)
df_anomalia_perc = df_com_job[
    (~df_com_job['is_bloqueado_regra']) & 
    (df_com_job['Job_Perc_Honorarios'].isna() | (df_com_job['Job_Perc_Honorarios'] == 0))
].copy()

print(f"1. Sem Contrato/Job: {len(df_sem_contrato)}")
print(f"2. Com Job mas SEM Data Cadastro: {len(df_sem_data_cad)}")
print(f"3. Anomalia Percentual (% zerado sem ser regra): {len(df_anomalia_perc)}")

excel_path = r"c:\Users\cristhofer.maciel.GRUPOSTUDIO\.gemini\antigravity\scratch\automacao-mensageria-bi\Relatorio_Anomalias_Tax_Corporate_Ago_Set_2026.xlsx"

with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
    df_sem_data_cad.to_excel(writer, sheet_name='Sem_Data_Cadastro', index=False)
    df_sem_contrato.to_excel(writer, sheet_name='Sem_Contrato_Job', index=False)
    df_anomalia_perc.to_excel(writer, sheet_name='Anomalias_Percentuais', index=False)
    df.to_excel(writer, sheet_name='Base_Completa_Tax_Corp', index=False)

print("Excel gerado com sucesso!")

desktop_path = os.path.join(os.path.expanduser("~"), "Desktop", "Relatorio_Anomalias_Tax_Corporate_Ago_Set_2026.xlsx")
shutil.copy2(excel_path, desktop_path)
print(f"Arquivo copiado para o Desktop: {desktop_path}")

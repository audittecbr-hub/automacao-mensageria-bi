import pandas as pd

excel_path = r"c:\Users\cristhofer.maciel.GRUPOSTUDIO\.gemini\antigravity\scratch\automacao-mensageria-bi\Relatorio_Anomalias_Tax_Corporate_Ago_Set_2026.xlsx"
df = pd.read_excel(excel_path, sheet_name='JOB Nao Cadastrado', header=3)
print(f"Total de registros na aba 'JOB Nao Cadastrado': {len(df)}")

print("\n--- DISTRIBUIÇÃO POR CATEGORIA ---")
print(df['Categoria'].value_counts())

print("\n--- DISTRIBUIÇÃO POR BANDEIRA ---")
print(df['Bandeira'].value_counts())

print("\n--- TOP CONTRATOS/JOBS DESSA ABA ---")
print(df['Nº Contrato / JOB'].value_counts().head(25))

print("\n--- AMOSTRA DE 15 LANÇAMENTOS ---")
for idx, r in df.head(15).iterrows():
    print(f"Omie: {r['Cód. Omie']} | Job: {r['Nº Contrato / JOB']} | Cat: {r['Categoria']} | Band: {r['Bandeira']} | Cliente: {r['Razão Social Cliente']} | Valor: R$ {r['Valor Conta (R$)']:,.2f}")

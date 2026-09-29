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

print(f"Total Metas rows: {len(df_metas)}")

test_keys = ['422', '408', '210', '399', '419', '409', '48653', '81298', '83164', '83779', '83671', '86081', '85206', '84951', '86675']

for k in test_keys:
    matches = df_metas[df_metas['numero_contrato'].fillna('').astype(str).str.contains(f"^{k}$|{k}", regex=True)]
    print(f"\nBusca por '{k}' em numero_contrato: {len(matches)} ocorrências")
    for idx, r in matches.iterrows():
        print(f"  ID: {r['id']} | Omie: {r['codigo_lancamento_omie']} | Contrato: {r['numero_contrato']} | Cliente: {r['razao_social']} | Valor: R$ {r['valor_bruto']} | Cat: {r['descricao_cat']}")

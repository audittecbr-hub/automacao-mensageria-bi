import pandas as pd
import io

step_output_path = r"C:\Users\cristhofer.maciel.GRUPOSTUDIO\.gemini\antigravity-ide\brain\53a8a01a-da38-486b-92ec-ae80b30b913e\.system_generated\steps\593\output.txt"
with open(step_output_path, 'r', encoding='utf-8') as f:
    text = f.read()

if text.startswith('{"success":true}'):
    text = text.split('\n', 1)[1]

df = pd.read_csv(io.StringIO(text))
print("Total rows in metas:", len(df))
print("\n--- CATEGORIAS ---")
print(df['public metas_bruto[categoria]'].value_counts(dropna=False))

print("\n--- BANDEIRAS ---")
print(df['public metas_bruto[bandeira]'].value_counts(dropna=False).head(15))

print("\n--- SITUAÇÃO ---")
print(df['public metas_bruto[situacao]'].value_counts(dropna=False))

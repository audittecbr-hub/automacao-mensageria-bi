import pandas as pd
import io

with open(r"C:\Users\cristhofer.maciel.GRUPOSTUDIO\.gemini\antigravity-ide\brain\53a8a01a-da38-486b-92ec-ae80b30b913e\.system_generated\steps\744\output.txt", 'r', encoding='utf-8') as f:
    text = f.read()

if text.startswith('{"success":true}'):
    text = text.split('\n', 1)[1]

df = pd.read_csv(io.StringIO(text))
print("Tabelas no modelo:")
for idx, r in df.iterrows():
    name = r.get('[Name]') or r.get('Name')
    print(f"- Table: {name}")

import pandas as pd
import io

with open(r"C:\Users\cristhofer.maciel.GRUPOSTUDIO\.gemini\antigravity-ide\brain\53a8a01a-da38-486b-92ec-ae80b30b913e\.system_generated\steps\804\output.txt", 'r', encoding='utf-8') as f:
    text = f.read()

if text.startswith('{"success":true}'):
    text = text.split('\n', 1)[1]

df = pd.read_csv(io.StringIO(text))
print(f"Total columns: {len(df)}")
for idx, r in df.iterrows():
    table = r.get('[TableID]') or r.get('TableID')
    name = r.get('[ExplicitName]') or r.get('ExplicitName') or r.get('[InferredName]') or r.get('InferredName')
    expr = r.get('[Expression]') or r.get('Expression')
    print(f"TableID: {table} | Col: {name} | Expr: {expr if pd.notna(expr) else ''}")

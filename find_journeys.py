import pandas as pd
import io

step_path = r"C:\Users\cristhofer.maciel.GRUPOSTUDIO\.gemini\antigravity-ide\brain\53a8a01a-da38-486b-92ec-ae80b30b913e\.system_generated\steps\730\output.txt"
with open(step_path, 'r', encoding='utf-8') as f: text = f.read()
if text.startswith('{"success":true}'): text = text.split('\n', 1)[1]
df = pd.read_csv(io.StringIO(text))

for idx, r in df.iterrows():
    name = str(r.get('[Name]') or r.get('Name') or '')
    expr = str(r.get('[Expression]') or r.get('Expression') or '')
    if 'journeys' in expr.lower():
        print(f"Measure referencing journeys: {name}")

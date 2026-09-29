import pandas as pd
import io

with open(r"C:\Users\cristhofer.maciel.GRUPOSTUDIO\.gemini\antigravity-ide\brain\53a8a01a-da38-486b-92ec-ae80b30b913e\.system_generated\steps\810\output.txt", 'r', encoding='utf-8') as f:
    text = f.read()

if text.startswith('{"success":true}'):
    text = text.split('\n', 1)[1]

df = pd.read_csv(io.StringIO(text))
for idx, r in df.iterrows():
    print(f"JOB: {r.get('vw_powerbi_job_repasse[JOB]')} | UNIDADE: {r.get('vw_powerbi_job_repasse[UNIDADE_ID]')} | PERC_JOB: {r.get('vw_powerbi_job_repasse[PERC_HONORARIOS_JOB]')} | PERC_FRANQ: {r.get('vw_powerbi_job_repasse[PERC_HONORARIOS_FRANQUEADO]')}")

import json

with open(r"c:\Users\cristhofer.maciel.GRUPOSTUDIO\.gemini\antigravity\scratch\automacao-mensageria-bi\Painel_Repasses_dax.txt", "r", encoding="utf-8") as f:
    dax_content = f.read()

# Replace the honorario calculation lines
old_block = """        VAR percFromTable = CALCULATE(MAX('HonorariosPorJob'[honorario]), FILTER('HonorariosPorJob', 'HonorariosPorJob'[numero_contrato] = [JOB_VAL]))
        VAR curPercHonorario = COALESCE(percFromTable, [HonorariosPorJob.honorario], 0)"""

new_block = """        VAR percFromJob = CALCULATE(MAX('vw_powerbi_job_repasse'[PERC_HONORARIOS_JOB]), FILTER('vw_powerbi_job_repasse', 'vw_powerbi_job_repasse'[JOB] = [JOB_VAL]))
        VAR percFromTable = CALCULATE(MAX('HonorariosPorJob'[honorario]), FILTER('HonorariosPorJob', 'HonorariosPorJob'[numero_contrato] = [JOB_VAL]))
        VAR curPercHonorario = COALESCE(percFromJob, percFromTable, [HonorariosPorJob.honorario], 0)"""

if old_block in dax_content:
    dax_content = dax_content.replace(old_block, new_block)
    print("Successfully replaced honorario calculation in DAX")
else:
    print("Old block not found directly, checking variations...")

with open(r"c:\Users\cristhofer.maciel.GRUPOSTUDIO\.gemini\antigravity\scratch\automacao-mensageria-bi\Painel_Repasses_dax.txt", "w", encoding="utf-8") as f:
    f.write(dax_content)

payload = {
    "request": {
        "connectionName": "PBIDesktop-repasse-52151",
        "operation": "Update",
        "definitions": [
            {
                "name": "Painel_Repasses",
                "tableName": "medidas_html",
                "expression": dax_content
            }
        ]
    }
}

with open(r"c:\Users\cristhofer.maciel.GRUPOSTUDIO\.gemini\antigravity\scratch\automacao-mensageria-bi\payload_repasse.json", "w", encoding="utf-8") as f:
    json.dump(payload, f, indent=2, ensure_ascii=False)

print("Payload created.")

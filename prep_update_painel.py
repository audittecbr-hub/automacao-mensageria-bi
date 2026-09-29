import json

with open('current_painel_repasses.dax', 'r', encoding='utf-8') as f:
    dax_code = f.read()

# Replace percentage calculation logic
old_perc_logic = """        VAR percFromJob = CALCULATE(MAX('vw_powerbi_job_repasse'[PERC_HONORARIOS_JOB]), FILTER('vw_powerbi_job_repasse', 'vw_powerbi_job_repasse'[JOB] = [JOB_VAL]))
        VAR percFromTable = CALCULATE(MAX('HonorariosPorJob'[honorario]), FILTER('HonorariosPorJob', 'HonorariosPorJob'[numero_contrato] = [JOB_VAL]))
        VAR curPercHonorario = IF(isBloqueado, 0, COALESCE(percFromJob, percFromTable, [HonorariosPorJob.honorario], 0))"""

new_perc_logic = """        VAR percFromJob = CALCULATE(MAX('vw_powerbi_job_repasse'[PERC_HONORARIOS_JOB]), FILTER('vw_powerbi_job_repasse', 'vw_powerbi_job_repasse'[JOB] = [JOB_VAL]))
        VAR percFromTable = CALCULATE(MAX('HonorariosPorJob'[honorario]), FILTER('HonorariosPorJob', 'HonorariosPorJob'[numero_contrato] = [JOB_VAL]))
        VAR curUidNum = IF(ISBLANK(curUnidadeId) || curUnidadeId = "", BLANK(), VALUE(curUnidadeId))
        VAR percFromPU = CALCULATE(MAX('vw_participantes_unidades'[PERC_FRANQUEADO]), FILTER('vw_participantes_unidades', 'vw_participantes_unidades'[UNIDADE_ID] = curUidNum))
        VAR curPercHonorario = IF(
            isBloqueado, 
            0, 
            COALESCE(
                IF(percFromPU > 0, percFromPU, BLANK()),
                IF(percFromJob > 0, percFromJob, BLANK()), 
                IF(percFromTable > 0, percFromTable, BLANK()), 
                [HonorariosPorJob.honorario], 
                0
            )
        )"""

if old_perc_logic in dax_code:
    dax_code_updated = dax_code.replace(old_perc_logic, new_perc_logic)
    print("Substituição do cálculo de percentual realizada com sucesso!")
    with open('updated_painel_repasses.dax', 'w', encoding='utf-8') as out:
        out.write(dax_code_updated)
else:
    print("Aviso: Trecho exato de percentual não encontrado diretamente. Procurando linhas...")
    # Find and replace line by line
    import re
    dax_code_updated = re.sub(
        r"VAR percFromJob = CALCULATE\(MAX\('vw_powerbi_job_repasse'\[PERC_HONORARIOS_JOB\]\).*?VAR curPercHonorario = IF\(isBloqueado, 0, COALESCE\(percFromJob, percFromTable, \[HonorariosPorJob\.honorario\], 0\)\)",
        new_perc_logic,
        dax_code,
        flags=re.DOTALL
    )
    with open('updated_painel_repasses.dax', 'w', encoding='utf-8') as out:
        out.write(dax_code_updated)
    print("Substituição via regex realizada!")

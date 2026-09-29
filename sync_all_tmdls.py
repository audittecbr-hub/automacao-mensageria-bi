import os, re

paths = [
    r"c:\Users\cristhofer.maciel.GRUPOSTUDIO\Downloads\repasse.SemanticModel\definition\tables\medidas_html.tmdl",
    r"c:\Users\cristhofer.maciel.GRUPOSTUDIO\Downloads\repasse (3).SemanticModel\definition\tables\medidas_html.tmdl",
    r"c:\Users\cristhofer.maciel.GRUPOSTUDIO\Downloads\painel_corporate.SemanticModel\definition\tables\medidas_html.tmdl"
]

old_pattern = r"(VAR percFromJob = CALCULATE\(MAX\('vw_powerbi_job_repasse'\[PERC_HONORARIOS_JOB\]\).*?VAR curPercHonorario = IF\(isBloqueado, 0, COALESCE\(percFromJob, percFromTable, \[HonorariosPorJob\.honorario\], 0\)\))"

new_block = """VAR percFromJob = CALCULATE(MAX('vw_powerbi_job_repasse'[PERC_HONORARIOS_JOB]), FILTER('vw_powerbi_job_repasse', 'vw_powerbi_job_repasse'[JOB] = [JOB_VAL]))
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

for p in paths:
    if os.path.exists(p):
        with open(p, 'r', encoding='utf-8') as f:
            content = f.read()
        match = re.search(old_pattern, content, flags=re.DOTALL)
        if match:
            content_updated = content[:match.start()] + new_block + content[match.end():]
            with open(p, 'w', encoding='utf-8') as f:
                f.write(content_updated)
            print(f"Atualizado: {p}")
        else:
            print(f"Padrão não encontrado ou já atualizado em: {p}")

import os, re

tmdl_path = r"c:\Users\cristhofer.maciel.GRUPOSTUDIO\Downloads\repasse (3).SemanticModel\definition\tables\medidas_html.tmdl"

with open(tmdl_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace percentage calculation in TMDL
# Notice lines in TMDL have leading tabs (\t\t\t)
old_pattern = r"(VAR percFromJob = CALCULATE\(MAX\('vw_powerbi_job_repasse'\[PERC_HONORARIOS_JOB\]\).*?VAR curPercHonorario = IF\(isBloqueado, 0, COALESCE\(percFromJob, percFromTable, \[HonorariosPorJob\.honorario\], 0\)\))"

match = re.search(old_pattern, content, flags=re.DOTALL)
if match:
    print("Encontrado bloco de cálculo de percentual no TMDL!")
    
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
    
    content_updated = content[:match.start()] + new_block + content[match.end():]
    
    with open(tmdl_path, 'w', encoding='utf-8') as f:
        f.write(content_updated)
    print("Arquivo TMDL atualizado com sucesso!")
else:
    print("Padrão não encontrado diretamente. Vamos verificar trechos...")

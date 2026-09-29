import os
import re
import json
import subprocess

exe_path = r'C:\Users\cristhofer.maciel.GRUPOSTUDIO\.vscode\extensions\analysis-services.powerbi-modeling-mcp-0.4.0-win32-x64\server\powerbi-modeling-mcp.exe'

def update_ranking_tmdl(file_path):
    if not os.path.exists(file_path):
        print('File not found:', file_path)
        return
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Remove NOT ISBLANK(Metas[cnpj_cpf]) && Metas[cnpj_cpf] <> "",
    content = re.sub(r'[ \t]*NOT ISBLANK\(Metas\[cnpj_cpf\]\)\s*&&\s*Metas\[cnpj_cpf\]\s*<>\s*\"\",\r?\n', '', content)

    # 2. Replace @unidade_id block
    old_target = """\t\t\t        "@unidade_id",
\t\t\t            VAR curJob = [numero_contrato]
\t\t\t            VAR curCnpj = [cnpj_cpf]
\t\t\t            VAR idFromJob = CALCULATE(MAX('vw_powerbi_job_repasse'[UNIDADE_ID]), FILTER('vw_powerbi_job_repasse', 'vw_powerbi_job_repasse'[JOB] = curJob))
\t\t\t            VAR idFromTable = CALCULATE(MAX(UnidadesPorCNPJ[unidade_id]), FILTER(UnidadesPorCNPJ, UnidadesPorCNPJ[cnpj_cpf] = curCnpj))
\t\t\t            RETURN COALESCE(idFromJob, idFromTable),"""

    new_target = """\t\t\t        "@unidade_id",
\t\t\t            VAR curJob = [numero_contrato]
\t\t\t            RETURN CALCULATE(MAX('vw_powerbi_job_repasse'[UNIDADE_ID]), FILTER('vw_powerbi_job_repasse', 'vw_powerbi_job_repasse'[JOB] = curJob)),"""

    content = content.replace(old_target.replace('\r\n', '\n'), new_target.replace('\r\n', '\n'))

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'Successfully updated {file_path}')

# Update TMDL files for Ranking
ranking_paths = [
    r'C:\Users\cristhofer.maciel.GRUPOSTUDIO\Downloads\Ranking_Metas_V2.SemanticModel\definition\tables\Medidas_Repasse.tmdl',
    r'C:\Users\cristhofer.maciel.GRUPOSTUDIO\Downloads\Ranking_Metas.SemanticModel\definition\tables\Medidas_Repasse.tmdl',
    r'C:\Users\cristhofer.maciel.GRUPOSTUDIO\OneDrive\Ranking_Metas2.SemanticModel\definition\tables\Medidas_Repasse.tmdl'
]
for p in ranking_paths:
    update_ranking_tmdl(p)

import os
import re

tmdl_path = r'c:\Users\cristhofer.maciel.GRUPOSTUDIO\Downloads\Ranking_Metas_V2.SemanticModel\definition\tables\Medidas_Repasse.tmdl'

with open(tmdl_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace "@unidade_id" definition in all measures:
old_unidade_block = re.compile(
    r'\"@unidade_id\",\s*\n\s*VAR curJob = \[numero_contrato\]\s*\n\s*VAR curCnpj = \[cnpj_cpf\]\s*\n\s*VAR idFromJob = CALCULATE\(MAX\(\'vw_powerbi_job_repasse\'\[UNIDADE_ID\]\), FILTER\(\'vw_powerbi_job_repasse\', \'vw_powerbi_job_repasse\'\[JOB\] = curJob\)\)\s*\n\s*VAR idFromTable = CALCULATE\(MAX\(UnidadesPorCNPJ\[unidade_id\]\), FILTER\(UnidadesPorCNPJ, UnidadesPorCNPJ\[cnpj_cpf\] = curCnpj\)\)\s*\n\s*RETURN COALESCE\(idFromJob, idFromTable\),',
    re.MULTILINE
)

new_unidade_block = '''"@unidade_id",
\t\t\t    VAR curJob = [numero_contrato]
\t\t\t    RETURN CALCULATE(MAX('vw_powerbi_job_repasse'[UNIDADE_ID]), FILTER('vw_powerbi_job_repasse', 'vw_powerbi_job_repasse'[JOB] = curJob)),'''

if old_unidade_block.search(content):
    content = old_unidade_block.sub(new_unidade_block, content)
    print("Replaced with regex.")
else:
    print("Regex didn't match, doing line-by-line replacement...")
    lines = content.splitlines()
    new_lines = []
    i = 0
    count = 0
    while i < len(lines):
        line = lines[i]
        if '"@unidade_id",' in line:
            indent = line[:line.find('"@unidade_id",')]
            # Look ahead for RETURN
            j = i
            while j < len(lines) and 'RETURN' not in lines[j]:
                j += 1
            if j < len(lines):
                j += 1 # past RETURN line
            replacement = [
                f'{indent}"@unidade_id",\n',
                f'{indent}    VAR curJob = [numero_contrato]\n',
                f"{indent}    RETURN CALCULATE(MAX('vw_powerbi_job_repasse'[UNIDADE_ID]), FILTER('vw_powerbi_job_repasse', 'vw_powerbi_job_repasse'[JOB] = curJob)),\n"
            ]
            new_lines.extend(replacement)
            count += 1
            i = j
        else:
            new_lines.append(line + '\n')
            i += 1
    content = ''.join(new_lines)
    print(f"Replaced {count} occurrences line-by-line.")

with open(tmdl_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Saved updated Medidas_Repasse.tmdl successfully.")

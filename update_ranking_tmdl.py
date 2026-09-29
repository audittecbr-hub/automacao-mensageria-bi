import os
import re

path = r"c:\Users\cristhofer.maciel.GRUPOSTUDIO\Downloads\Ranking_Metas_V2.SemanticModel\definition\tables\Medidas_Repasse.tmdl"

with open(path, "r", encoding="utf-8") as f:
    lines = f.readlines()

new_lines = []
i = 0
replaced_count = 0

target_pattern = re.compile(r'^\s*\"@honorario_job\",\s*$')

while i < len(lines):
    line = lines[i]
    if target_pattern.match(line) or '"@honorario_job",' in line:
        indent = line[:line.find('"@honorario_job",')]
        # Find where RETURN ... ends
        j = i
        while j < len(lines) and "RETURN" not in lines[j]:
            j += 1
        # Include the RETURN line
        if j < len(lines):
            j += 1
        
        replacement = [
            f'{indent}"@honorario_job", \n',
            f'{indent}    VAR curJob = [numero_contrato]\n',
            f"{indent}    VAR percFromJob = CALCULATE(MAX('vw_powerbi_job_repasse'[PERC_HONORARIOS_JOB]), FILTER('vw_powerbi_job_repasse', 'vw_powerbi_job_repasse'[JOB] = curJob))\n",
            f"{indent}    VAR percFromFranq = CALCULATE(MAX('vw_powerbi_job_repasse'[PERC_HONORARIOS_FRANQUEADO]), FILTER('vw_powerbi_job_repasse', 'vw_powerbi_job_repasse'[JOB] = curJob))\n",
            f"{indent}    VAR percFromFranq2 = CALCULATE(MAX('vw_powerbi_job_repasse'[PERC_FRANQUEADO]), FILTER('vw_powerbi_job_repasse', 'vw_powerbi_job_repasse'[JOB] = curJob))\n",
            f"{indent}    VAR percFromTable = CALCULATE(MAX(HonorariosPorJob[honorario]), FILTER(HonorariosPorJob, HonorariosPorJob[numero_contrato] = curJob))\n",
            f'{indent}    RETURN COALESCE(\n',
            f'{indent}        IF(percFromFranq > 0, percFromFranq, BLANK()),\n',
            f'{indent}        IF(percFromFranq2 > 0, percFromFranq2, BLANK()),\n',
            f'{indent}        IF(percFromJob > 0, percFromJob, BLANK()),\n',
            f'{indent}        IF(percFromTable > 0, percFromTable, BLANK()),\n',
            f'{indent}        0\n',
            f'{indent}    ),\n'
        ]
        new_lines.extend(replacement)
        replaced_count += 1
        i = j
    else:
        new_lines.append(line)
        i += 1

print(f"Replaced {replaced_count} occurrences.")

with open(path, "w", encoding="utf-8") as f:
    f.writelines(new_lines)

print("Saved updated TMDL file successfully.")

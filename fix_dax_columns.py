import re

with open('Painel_Repasses_Codigo.txt', 'r', encoding='utf8') as f:
    text = f.read()

# Replace valor_conta with valor_bruto
text = text.replace('[valor_conta]', '[valor_bruto]')

# Remove PERC_FRANQUEADO_VAL references since we don't have it anymore. Just use HonorariosPorJob.honorario
# Old: COALESCE([PERC_JOB_REPASSE_VAL], [PERC_FRANQUEADO_VAL], 0)
# It was already updated to: COALESCE([HonorariosPorJob.honorario], [PERC_FRANQUEADO_VAL], 0)
text = text.replace('COALESCE([HonorariosPorJob.honorario], [PERC_FRANQUEADO_VAL], 0)', 'COALESCE([HonorariosPorJob.honorario], 0)')
text = text.replace('COALESCE([PERC_FRANQUEADO_VAL], 0)', '0') # For percUnidade

with open('Painel_Repasses_Codigo.txt', 'w', encoding='utf8') as f:
    f.write(text)

with open(r'C:\Users\cristhofer.maciel.GRUPOSTUDIO\.gemini\antigravity-ide\brain\295cbf89-2513-4d5c-86a1-fc95a552fa3c\Painel_Repasses_Codigo.md', 'w', encoding='utf8') as f:
    f.write('`dax\n' + text + '\n`')

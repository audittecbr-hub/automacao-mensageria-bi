import re

with open('Painel_Repasses_Codigo.txt', 'r', encoding='utf8') as f:
    text = f.read()

# Replace the ADDCOLUMNS block that references vw_powerbi_job_repasse
old_dax = '''			VAR vRecebido = 
			    ADDCOLUMNS(
			        vBase,
			        "NOME_UNIDADE_VAL", 
			        VAR curUnidade = [unidade_id]
			        RETURN
			        CALCULATE(
			            MAX('vw_powerbi_job_repasse'[UNIDADE_NOME]),
			            FILTER('vw_powerbi_job_repasse', FORMAT('vw_powerbi_job_repasse'[UNIDADE_ID], "0") = curUnidade)
			        ),
			        "JOB_VAL", 'public metas_bruto'[numero_contrato],
			        "DATA_CADASTRO_VAL", 
			        VAR curJob = 'public metas_bruto'[numero_contrato]
			        RETURN
			        CALCULATE(
			            MAX('vw_powerbi_job_repasse'[DATA_CADASTRO]),
			            FILTER('vw_powerbi_job_repasse', 'vw_powerbi_job_repasse'[JOB] = curJob)
			        )
			    )'''

new_dax = '''			VAR vRecebido = 
			    ADDCOLUMNS(
			        vBase,
			        "NOME_UNIDADE_VAL", BLANK(),
			        "JOB_VAL", 'public metas_bruto'[numero_contrato],
			        "DATA_CADASTRO_VAL", BLANK()
			    )'''

text = text.replace(old_dax, new_dax)

with open('Painel_Repasses_Codigo.txt', 'w', encoding='utf8') as f:
    f.write(text)

with open(r'C:\Users\cristhofer.maciel.GRUPOSTUDIO\.gemini\antigravity-ide\brain\295cbf89-2513-4d5c-86a1-fc95a552fa3c\Painel_Repasses_Codigo.md', 'w', encoding='utf8') as f:
    f.write('`dax\n' + text + '\n`')

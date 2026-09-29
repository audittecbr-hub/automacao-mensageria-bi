import json

with open("Painel_Repasses_dax.txt", "r", encoding="utf-8") as f:
    dax = f.read()

# Replace the data block in DAX
old_block = """VAR vRecebido = 
    ADDCOLUMNS(
        vBase,
        "UNIDADE_ID_VAL",
        VAR curJob = [numero_contrato]
        VAR idFromJob = CALCULATE(
            MAX('vw_powerbi_job_repasse'[UNIDADE_ID]),
            FILTER('vw_powerbi_job_repasse', 'vw_powerbi_job_repasse'[JOB] = curJob)
        )
        RETURN
        IF(ISBLANK(idFromJob), "", FORMAT(idFromJob, "0")),
        "NOME_UNIDADE_VAL", 
        VAR curJob = [numero_contrato]
        RETURN
        CALCULATE(
            MAX('vw_powerbi_job_repasse'[UNIDADE_NOME]),
            FILTER('vw_powerbi_job_repasse', 'vw_powerbi_job_repasse'[JOB] = curJob)
        ),
        "JOB_VAL", [numero_contrato],
        "DATA_CADASTRO_VAL", 
        VAR curJob = [numero_contrato]
        RETURN
        CALCULATE(
            MAX('vw_powerbi_job_repasse'[DATA_CADASTRO]),
            FILTER('vw_powerbi_job_repasse', 'vw_powerbi_job_repasse'[JOB] = curJob)
        ),
        "GROSSUP_VAL",
        VAR curJob = [numero_contrato]
        VAR valGrossup = CALCULATE(
            MAX('vw_powerbi_job_repasse'[COBRANCA_GROSSUP]),
            FILTER('vw_powerbi_job_repasse', 'vw_powerbi_job_repasse'[JOB] = curJob)
        )
        RETURN
        IF(ISBLANK(valGrossup), "-", IF(valGrossup = "S" || valGrossup = "Sim" || valGrossup = "1", "Sim", "Não")),
        "IMPOSTO_VAL",
        VAR curJob = [numero_contrato]
        VAR valImposto = CALCULATE(
            MAX('vw_powerbi_job_repasse'[UNIRETEMIMPOSTO]),
            FILTER('vw_powerbi_job_repasse', 'vw_powerbi_job_repasse'[JOB] = curJob)
        )
        RETURN
        IF(ISBLANK(valImposto), "-", IF(valImposto = 0, "Sim", "Não")),
        "RETENCAO_VAL",
        VAR curJob = [numero_contrato]
        RETURN
        CALCULATE(
            MAX('vw_powerbi_job_repasse'[RETENCAO]),
            FILTER('vw_powerbi_job_repasse', 'vw_powerbi_job_repasse'[JOB] = curJob)
        )
    )

VAR vJsonRows =
    CONCATENATEX(
        vRecebido,
        VAR isGrossup = ([GROSSUP_VAL] = "Sim")
        VAR curBaseValor = IF(isGrossup, DIVIDE([valor_bruto], 1.1425, 0), [valor_bruto])
        VAR curPercHonorario = IF(ISBLANK([DATA_CADASTRO_VAL]), 0, COALESCE([HonorariosPorJob.honorario], 0))"""

new_block = """VAR vRecebido = 
    ADDCOLUMNS(
        vBase,
        "UNIDADE_ID_VAL",
        VAR curJob = [numero_contrato]
        VAR curCnpj = [cnpj_cpf]
        VAR idFromJob = CALCULATE(
            MAX('vw_powerbi_job_repasse'[UNIDADE_ID]),
            FILTER('vw_powerbi_job_repasse', 'vw_powerbi_job_repasse'[JOB] = curJob)
        )
        VAR idFromPU = CALCULATE(
            MAX('vw_participantes_unidades'[UNIDADE_ID]),
            FILTER('vw_participantes_unidades', 
                (NOT ISBLANK('vw_participantes_unidades'[PARTICIPANTE_CPF]) && 'vw_participantes_unidades'[PARTICIPANTE_CPF] = curCnpj) || 
                (NOT ISBLANK('vw_participantes_unidades'[CNPJ_UNIDADE]) && 'vw_participantes_unidades'[CNPJ_UNIDADE] = curCnpj)
            )
        )
        VAR finalId = COALESCE(idFromJob, idFromPU)
        RETURN
        IF(ISBLANK(finalId), "", FORMAT(finalId, "0")),

        "NOME_UNIDADE_VAL", 
        VAR curJob = [numero_contrato]
        VAR curCnpj = [cnpj_cpf]
        VAR nomeFromJob = CALCULATE(
            MAX('vw_powerbi_job_repasse'[UNIDADE_NOME]),
            FILTER('vw_powerbi_job_repasse', 'vw_powerbi_job_repasse'[JOB] = curJob)
        )
        VAR nomeFromPU = CALCULATE(
            MAX('vw_participantes_unidades'[UNIDADE_NOME]),
            FILTER('vw_participantes_unidades', 
                (NOT ISBLANK('vw_participantes_unidades'[PARTICIPANTE_CPF]) && 'vw_participantes_unidades'[PARTICIPANTE_CPF] = curCnpj) || 
                (NOT ISBLANK('vw_participantes_unidades'[CNPJ_UNIDADE]) && 'vw_participantes_unidades'[CNPJ_UNIDADE] = curCnpj)
            )
        )
        RETURN
        COALESCE(nomeFromJob, nomeFromPU, ""),

        "JOB_VAL", [numero_contrato],
        "DATA_CADASTRO_VAL", 
        VAR curJob = [numero_contrato]
        VAR curCnpj = [cnpj_cpf]
        VAR dtFromJob = CALCULATE(
            MAX('vw_powerbi_job_repasse'[DATA_CADASTRO]),
            FILTER('vw_powerbi_job_repasse', 'vw_powerbi_job_repasse'[JOB] = curJob)
        )
        VAR dtFromPU = CALCULATE(
            MAX('vw_participantes_unidades'[VIGENCIA_INICIO]),
            FILTER('vw_participantes_unidades', 
                (NOT ISBLANK('vw_participantes_unidades'[PARTICIPANTE_CPF]) && 'vw_participantes_unidades'[PARTICIPANTE_CPF] = curCnpj) || 
                (NOT ISBLANK('vw_participantes_unidades'[CNPJ_UNIDADE]) && 'vw_participantes_unidades'[CNPJ_UNIDADE] = curCnpj)
            )
        )
        RETURN
        COALESCE(dtFromJob, dtFromPU, [data_lancamento]),

        "GROSSUP_VAL",
        VAR curJob = [numero_contrato]
        VAR valGrossup = CALCULATE(
            MAX('vw_powerbi_job_repasse'[COBRANCA_GROSSUP]),
            FILTER('vw_powerbi_job_repasse', 'vw_powerbi_job_repasse'[JOB] = curJob)
        )
        RETURN
        IF(ISBLANK(valGrossup), "-", IF(valGrossup = "S" || valGrossup = "Sim" || valGrossup = "1", "Sim", "Não")),
        "IMPOSTO_VAL",
        VAR curJob = [numero_contrato]
        VAR valImposto = CALCULATE(
            MAX('vw_powerbi_job_repasse'[UNIRETEMIMPOSTO]),
            FILTER('vw_powerbi_job_repasse', 'vw_powerbi_job_repasse'[JOB] = curJob)
        )
        RETURN
        IF(ISBLANK(valImposto), "-", IF(valImposto = 0, "Sim", "Não")),
        "RETENCAO_VAL",
        VAR curJob = [numero_contrato]
        RETURN
        CALCULATE(
            MAX('vw_powerbi_job_repasse'[RETENCAO]),
            FILTER('vw_powerbi_job_repasse', 'vw_powerbi_job_repasse'[JOB] = curJob)
        )
    )

VAR vJsonRows =
    CONCATENATEX(
        vRecebido,
        VAR isGrossup = ([GROSSUP_VAL] = "Sim")
        VAR curBaseValor = IF(isGrossup, DIVIDE([valor_bruto], 1.1425, 0), [valor_bruto])
        VAR percFromTable = CALCULATE(MAX('HonorariosPorJob'[honorario]), FILTER('HonorariosPorJob', 'HonorariosPorJob'[numero_contrato] = [JOB_VAL]))
        VAR curPercHonorario = COALESCE(percFromTable, [HonorariosPorJob.honorario], 0)"""

if old_block in dax:
    dax_updated = dax.replace(old_block, new_block)
    with open("Painel_Repasses_dax.txt", "w", encoding="utf-8") as f:
        f.write(dax_updated)
    print("Painel_Repasses_dax.txt updated successfully.")
else:
    print("Could not find old_block in Painel_Repasses_dax.txt")

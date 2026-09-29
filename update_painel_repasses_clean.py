import os
import re
import json
import subprocess

exe_path = r'C:\Users\cristhofer.maciel.GRUPOSTUDIO\.vscode\extensions\analysis-services.powerbi-modeling-mcp-0.4.0-win32-x64\server\powerbi-modeling-mcp.exe'

# Read current Painel_Repasses expression from file or TMDL
tmdl_path = r'C:\Users\cristhofer.maciel.GRUPOSTUDIO\OneDrive\repasse.SemanticModel\definition\tables\medidas_html.tmdl'

with open(tmdl_path, 'r', encoding='utf-8') as f:
    full_tmdl = f.read()

# Extract Painel_Repasses definition
pos_start = full_tmdl.find('measure Painel_Repasses =')
pos_end = full_tmdl.find('\n\tmeasure ', pos_start + 1)
if pos_end == -1:
    pos_end = len(full_tmdl)

painel_def = full_tmdl[pos_start:pos_end]

# 1. Replace UNIDADE_ID_VAL block
old_unidade_id = """\t\t\t        "UNIDADE_ID_VAL",
\t\t\t        VAR curJob = [numero_contrato]
\t\t\t        VAR curCnpj = [cnpj_cpf]
\t\t\t        VAR idFromJob = CALCULATE(
\t\t\t            MAX('vw_powerbi_job_repasse'[UNIDADE_ID]),
\t\t\t            FILTER('vw_powerbi_job_repasse', 'vw_powerbi_job_repasse'[JOB] = curJob)
\t\t\t        )
\t\t\t        VAR idFromPU = CALCULATE(
\t\t\t            MAX('vw_participantes_unidades'[UNIDADE_ID]),
\t\t\t            FILTER('vw_participantes_unidades', 
\t\t\t                (NOT ISBLANK('vw_participantes_unidades'[PARTICIPANTE_CPF]) && 'vw_participantes_unidades'[PARTICIPANTE_CPF] = curCnpj) || 
\t\t\t                (NOT ISBLANK('vw_participantes_unidades'[CNPJ_UNIDADE]) && 'vw_participantes_unidades'[CNPJ_UNIDADE] = curCnpj)
\t\t\t            )
\t\t\t        )
\t\t\t        VAR finalId = COALESCE(idFromJob, idFromPU)
\t\t\t        RETURN
\t\t\t        IF(ISBLANK(finalId), "", FORMAT(finalId, "0")),"""

new_unidade_id = """\t\t\t        "UNIDADE_ID_VAL",
\t\t\t        VAR curJob = [numero_contrato]
\t\t\t        VAR idFromJob = CALCULATE(
\t\t\t            MAX('vw_powerbi_job_repasse'[UNIDADE_ID]),
\t\t\t            FILTER('vw_powerbi_job_repasse', 'vw_powerbi_job_repasse'[JOB] = curJob)
\t\t\t        )
\t\t\t        RETURN
\t\t\t        IF(ISBLANK(idFromJob), "", FORMAT(idFromJob, "0")),"""

# 2. Replace NOME_UNIDADE_VAL block
old_nome_unidade = """\t\t\t        "NOME_UNIDADE_VAL", 
\t\t\t        VAR curJob = [numero_contrato]
\t\t\t        VAR curCnpj = [cnpj_cpf]
\t\t\t        VAR nomeFromJob = CALCULATE(
\t\t\t            MAX('vw_powerbi_job_repasse'[UNIDADE_NOME]),
\t\t\t            FILTER('vw_powerbi_job_repasse', 'vw_powerbi_job_repasse'[JOB] = curJob)
\t\t\t        )
\t\t\t        VAR nomeFromPU = CALCULATE(
\t\t\t            MAX('vw_participantes_unidades'[UNIDADE_NOME]),
\t\t\t            FILTER('vw_participantes_unidades', 
\t\t\t                (NOT ISBLANK('vw_participantes_unidades'[PARTICIPANTE_CPF]) && 'vw_participantes_unidades'[PARTICIPANTE_CPF] = curCnpj) || 
\t\t\t                (NOT ISBLANK('vw_participantes_unidades'[CNPJ_UNIDADE]) && 'vw_participantes_unidades'[CNPJ_UNIDADE] = curCnpj)
\t\t\t            )
\t\t\t        )
\t\t\t        RETURN
\t\t\t        COALESCE(nomeFromJob, nomeFromPU, ""),"""

new_nome_unidade = """\t\t\t        "NOME_UNIDADE_VAL", 
\t\t\t        VAR curJob = [numero_contrato]
\t\t\t        VAR nomeFromJob = CALCULATE(
\t\t\t            MAX('vw_powerbi_job_repasse'[UNIDADE_NOME]),
\t\t\t            FILTER('vw_powerbi_job_repasse', 'vw_powerbi_job_repasse'[JOB] = curJob)
\t\t\t        )
\t\t\t        RETURN
\t\t\t        COALESCE(nomeFromJob, ""),"""

# 3. Replace DATA_CADASTRO_VAL block
old_data_cadastro = """\t\t\t        "DATA_CADASTRO_VAL", 
\t\t\t        VAR curJob = [numero_contrato]
\t\t\t        VAR curCnpj = [cnpj_cpf]
\t\t\t        VAR dtFromJob = CALCULATE(
\t\t\t            MAX('vw_powerbi_job_repasse'[DATA_CADASTRO]),
\t\t\t            FILTER('vw_powerbi_job_repasse', 'vw_powerbi_job_repasse'[JOB] = curJob)
\t\t\t        )
\t\t\t        VAR dtFromPU = CALCULATE(
\t\t\t            MAX('vw_participantes_unidades'[VIGENCIA_INICIO]),
\t\t\t            FILTER('vw_participantes_unidades', 
\t\t\t                (NOT ISBLANK('vw_participantes_unidades'[PARTICIPANTE_CPF]) && 'vw_participantes_unidades'[PARTICIPANTE_CPF] = curCnpj) || 
\t\t\t                (NOT ISBLANK('vw_participantes_unidades'[CNPJ_UNIDADE]) && 'vw_participantes_unidades'[CNPJ_UNIDADE] = curCnpj)
\t\t\t            )
\t\t\t        )
\t\t\t        RETURN
\t\t\t        COALESCE(dtFromJob, dtFromPU, [data_lancamento]),"""

new_data_cadastro = """\t\t\t        "DATA_CADASTRO_VAL", 
\t\t\t        VAR curJob = [numero_contrato]
\t\t\t        VAR dtFromJob = CALCULATE(
\t\t\t            MAX('vw_powerbi_job_repasse'[DATA_CADASTRO]),
\t\t\t            FILTER('vw_powerbi_job_repasse', 'vw_powerbi_job_repasse'[JOB] = curJob)
\t\t\t        )
\t\t\t        RETURN
\t\t\t        COALESCE(dtFromJob, [data_lancamento]),"""

# 4. Replace curPercHonorario block
old_honorario = """\t\t\t        VAR percFromJob = CALCULATE(MAX('vw_powerbi_job_repasse'[PERC_HONORARIOS_JOB]), FILTER('vw_powerbi_job_repasse', 'vw_powerbi_job_repasse'[JOB] = [JOB_VAL]))
\t\t\tVAR percFromTable = CALCULATE(MAX('HonorariosPorJob'[honorario]), FILTER('HonorariosPorJob', 'HonorariosPorJob'[numero_contrato] = [JOB_VAL]))
\t\t\tVAR curUidNum = IF(ISBLANK(curUnidadeId) || curUnidadeId = "", BLANK(), VALUE(curUnidadeId))
\t\t\tVAR percFromPU = CALCULATE(MAX('vw_participantes_unidades'[PERC_FRANQUEADO]), FILTER('vw_participantes_unidades', 'vw_participantes_unidades'[UNIDADE_ID] = curUidNum))
\t\t\tVAR curPercHonorario = IF(
\t\t\t    isBloqueado, 
\t\t\t    0, 
\t\t\t    COALESCE(
\t\t\t        IF(percFromPU > 0, percFromPU, BLANK()),
\t\t\t        IF(percFromJob > 0, percFromJob, BLANK()), 
\t\t\t        IF(percFromTable > 0, percFromTable, BLANK()), 
\t\t\t        [HonorariosPorJob.honorario], 
\t\t\t        0
\t\t\t    )
\t\t\t)"""

new_honorario = """\t\t\t        VAR percFromJob = CALCULATE(MAX('vw_powerbi_job_repasse'[PERC_HONORARIOS_JOB]), FILTER('vw_powerbi_job_repasse', 'vw_powerbi_job_repasse'[JOB] = [JOB_VAL]))
\t\t\t        VAR percFromFranq = CALCULATE(MAX('vw_powerbi_job_repasse'[PERC_HONORARIOS_FRANQUEADO]), FILTER('vw_powerbi_job_repasse', 'vw_powerbi_job_repasse'[JOB] = [JOB_VAL]))
\t\t\t        VAR percFromFranq2 = CALCULATE(MAX('vw_powerbi_job_repasse'[PERC_FRANQUEADO]), FILTER('vw_powerbi_job_repasse', 'vw_powerbi_job_repasse'[JOB] = [JOB_VAL]))
\t\t\t        VAR percFromTable = CALCULATE(MAX('HonorariosPorJob'[honorario]), FILTER('HonorariosPorJob', 'HonorariosPorJob'[numero_contrato] = [JOB_VAL]))
\t\t\t        VAR curPercHonorario = IF(
\t\t\t            isBloqueado, 
\t\t\t            0, 
\t\t\t            COALESCE(
\t\t\t                IF(percFromFranq > 0, percFromFranq, BLANK()),
\t\t\t                IF(percFromFranq2 > 0, percFromFranq2, BLANK()),
\t\t\t                IF(percFromJob > 0, percFromJob, BLANK()), 
\t\t\t                IF(percFromTable > 0, percFromTable, BLANK()), 
\t\t\t                0
\t\t\t            )
\t\t\t        )"""

# Perform replacements
norm_painel = painel_def.replace('\r\n', '\n')
norm_painel = norm_painel.replace(old_unidade_id.replace('\r\n', '\n'), new_unidade_id.replace('\r\n', '\n'))
norm_painel = norm_painel.replace(old_nome_unidade.replace('\r\n', '\n'), new_nome_unidade.replace('\r\n', '\n'))
norm_painel = norm_painel.replace(old_data_cadastro.replace('\r\n', '\n'), new_data_cadastro.replace('\r\n', '\n'))
norm_painel = norm_painel.replace(old_honorario.replace('\r\n', '\n'), new_honorario.replace('\r\n', '\n'))

print('Occurrences of vw_participantes_unidades in new painel:', norm_painel.count('vw_participantes_unidades'))

# Update TMDL files
for p in [r'C:\Users\cristhofer.maciel.GRUPOSTUDIO\OneDrive\repasse.SemanticModel\definition\tables\medidas_html.tmdl', r'C:\Users\cristhofer.maciel.GRUPOSTUDIO\Downloads\repasse.SemanticModel\definition\tables\medidas_html.tmdl']:
    if os.path.exists(p):
        with open(p, 'r', encoding='utf-8') as f:
            c = f.read()
        c_norm = c.replace('\r\n', '\n')
        p_start = c_norm.find('measure Painel_Repasses =')
        p_end = c_norm.find('\n\tmeasure ', p_start + 1)
        if p_end == -1:
            p_end = len(c_norm)
        c_new = c_norm[:p_start] + norm_painel + c_norm[p_end:]
        with open(p, 'w', encoding='utf-8') as f:
            f.write(c_new)
        print('Updated TMDL:', p)

# Extract raw DAX expression for MCP
m = re.search(r'```([\s\S]*?)```', norm_painel)
raw_expr = ''
if m:
    lines = [l.replace('\t\t\t', '') for l in m.group(1).strip().splitlines()]
    raw_expr = '\n'.join(lines)

# Push live to Port 57503
p = subprocess.Popen([exe_path, '--start'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8')

msg_id = 1
def send(msg):
    global msg_id
    msg['id'] = msg_id
    msg_id += 1
    p.stdin.write(json.dumps(msg) + '\n')
    p.stdin.flush()
    res = p.stdout.readline()
    try:
        return json.loads(res)
    except:
        return res

# 1. Initialize
send({'jsonrpc': '2.0', 'method': 'initialize', 'params': {'protocolVersion': '2024-11-05', 'capabilities': {}, 'clientInfo': {'name': 'sync', 'version': '1.0'}}})

# 2. Connect to Port 57503
conn_resp = send({
    'jsonrpc': '2.0',
    'method': 'tools/call',
    'params': {
        'name': 'connection_operations',
        'arguments': {
            'request': {
                'operation': 'Connect',
                'connectionString': 'Data Source=localhost:57503;Application Name=MCP-Direct'
            }
        }
    }
})
print('Connect to 57503:', conn_resp.get('result', {}).get('content', [{}])[0].get('text', ''))

# 3. Update measure in medidas_html
upd_resp = send({
    'jsonrpc': '2.0',
    'method': 'tools/call',
    'params': {
        'name': 'measure_operations',
        'arguments': {
            'request': {
                'operation': 'Update',
                'Definitions': [
                    {
                        'Name': 'Painel_Repasses',
                        'TableName': 'medidas_html',
                        'Expression': raw_expr
                    }
                ]
            }
        }
    }
})
print('Update Painel_Repasses result:', upd_resp.get('result', {}).get('content', [{}])[0].get('text', ''))

# 4. Run DAX test query to verify Painel_Repasses evaluates
test_dax = send({
    'jsonrpc': '2.0',
    'method': 'tools/call',
    'params': {
        'name': 'dax_query_operations',
        'arguments': {
            'request': {
                'operation': 'Execute',
                'query': 'EVALUATE ROW("Len", LEN([Painel_Repasses]))'
            }
        }
    }
})
print('DAX Test Result (LEN):')
for c in test_dax.get('result', {}).get('content', []):
    if 'resource' in c:
        print(c['resource']['text'])

p.terminate()

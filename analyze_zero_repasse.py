import json
import subprocess

exe_path = r'C:\Users\cristhofer.maciel.GRUPOSTUDIO\.vscode\extensions\analysis-services.powerbi-modeling-mcp-0.4.0-win32-x64\server\powerbi-modeling-mcp.exe'
p = subprocess.Popen([exe_path, '--start'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8')
msg_id = 1
def send(msg):
    global msg_id
    msg['id'] = msg_id
    msg_id += 1
    p.stdin.write(json.dumps(msg) + '\n')
    p.stdin.flush()
    return json.loads(p.stdout.readline())

send({'jsonrpc': '2.0', 'method': 'initialize', 'params': {'protocolVersion': '2024-11-05', 'capabilities': {}, 'clientInfo': {'name': 'audit', 'version': '1.0'}}})
send({'jsonrpc': '2.0', 'method': 'tools/call', 'params': {'name': 'connection_operations', 'arguments': {'request': {'operation': 'Connect', 'connectionString': 'Data Source=localhost:52661;Application Name=MCP-Audit'}}}})

# Run DAX to see why some rows have 0 repasse
dax = '''
EVALUATE
VAR _DataCorte = DATE(2026, 8, 1)
VAR _BaseNovo = 
    CALCULATETABLE(
        SUMMARIZE(
            Metas,
            Metas[codigo_lancamento_omie],
            Metas[numero_contrato],
            Metas[cnpj_cpf],
            Metas[bandeira]
        ),
        Metas[data_emissao] >= _DataCorte,
        UPPER(Metas[categoria]) = "TAX",
        TREATAS(VALUES(Metas[codigo_lancamento_omie]), Metas[codigo_lancamento_omie]),
        Calendario[MesNome] = "Agosto",
        Calendario[Ano] = 2026
    )

VAR _BaseComCalculos = 
    ADDCOLUMNS(
        _BaseNovo,
        "@valor_conta", CALCULATE(SUM(Metas[valor_conta])),
        "@honorario_job", 
            VAR curJob = [numero_contrato]
            VAR percFromJob = CALCULATE(MAX('vw_powerbi_job_repasse'[PERC_HONORARIOS_JOB]), FILTER('vw_powerbi_job_repasse', 'vw_powerbi_job_repasse'[JOB] = curJob))
            VAR percFromFranq = CALCULATE(MAX('vw_powerbi_job_repasse'[PERC_HONORARIOS_FRANQUEADO]), FILTER('vw_powerbi_job_repasse', 'vw_powerbi_job_repasse'[JOB] = curJob))
            VAR percFromFranq2 = CALCULATE(MAX('vw_powerbi_job_repasse'[PERC_FRANQUEADO]), FILTER('vw_powerbi_job_repasse', 'vw_powerbi_job_repasse'[JOB] = curJob))
            VAR percFromTable = CALCULATE(MAX(HonorariosPorJob[honorario]), FILTER(HonorariosPorJob, HonorariosPorJob[numero_contrato] = curJob))
            RETURN COALESCE(
                IF(percFromFranq > 0, percFromFranq, BLANK()),
                IF(percFromFranq2 > 0, percFromFranq2, BLANK()),
                IF(percFromJob > 0, percFromJob, BLANK()),
                IF(percFromTable > 0, percFromTable, BLANK()),
                0
            ),
        "@data_cadastro", 
            VAR curJob = [numero_contrato]
            RETURN CALCULATE(MAX('vw_powerbi_job_repasse'[DATA_CADASTRO]), FILTER('vw_powerbi_job_repasse', 'vw_powerbi_job_repasse'[JOB] = curJob)),
        "@unidade_id",
            VAR curJob = [numero_contrato]
            RETURN CALCULATE(MAX('vw_powerbi_job_repasse'[UNIDADE_ID]), FILTER('vw_powerbi_job_repasse', 'vw_powerbi_job_repasse'[JOB] = curJob)),
        "@rede_distribuicao",
            VAR curJob = [numero_contrato]
            RETURN CALCULATE(MAX('vw_powerbi_job_repasse'[REDE_DISTRIBUICAO]), FILTER('vw_powerbi_job_repasse', 'vw_powerbi_job_repasse'[JOB] = curJob)),
        "@part_franqueado",
            VAR curJob = [numero_contrato]
            RETURN CALCULATE(MAX('vw_powerbi_job_repasse'[PARTICIPANTE_FRANQUEADO]), FILTER('vw_powerbi_job_repasse', 'vw_powerbi_job_repasse'[JOB] = curJob)),
        "@part_cliente",
            VAR curJob = [numero_contrato]
            RETURN CALCULATE(MAX('vw_powerbi_job_repasse'[PARTICIPANTE_CLIENTE]), FILTER('vw_powerbi_job_repasse', 'vw_powerbi_job_repasse'[JOB] = curJob))
    )

RETURN
ROW(
    "TotalRows", COUNTROWS(_BaseComCalculos),
    "TotalValorConta", SUMX(_BaseComCalculos, [@valor_conta]),
    "SemJob", COUNTROWS(FILTER(_BaseComCalculos, ISBLANK([numero_contrato]) || [numero_contrato] = "")),
    "ValorSemJob", SUMX(FILTER(_BaseComCalculos, ISBLANK([numero_contrato]) || [numero_contrato] = ""), [@valor_conta]),
    "JobNaoAchadoNaView", COUNTROWS(FILTER(_BaseComCalculos, NOT ISBLANK([numero_contrato]) && [numero_contrato] <> "" && ISBLANK([@unidade_id]))),
    "ValorJobNaoAchado", SUMX(FILTER(_BaseComCalculos, NOT ISBLANK([numero_contrato]) && [numero_contrato] <> "" && ISBLANK([@unidade_id])), [@valor_conta]),
    "SemDataCadastro", COUNTROWS(FILTER(_BaseComCalculos, NOT ISBLANK([@unidade_id]) && ISBLANK([@data_cadastro]))),
    "ValorSemDataCadastro", SUMX(FILTER(_BaseComCalculos, NOT ISBLANK([@unidade_id]) && ISBLANK([@data_cadastro])), [@valor_conta]),
    "HonorarioZero", COUNTROWS(FILTER(_BaseComCalculos, NOT ISBLANK([@unidade_id]) && [@honorario_job] = 0)),
    "ValorHonorarioZero", SUMX(FILTER(_BaseComCalculos, NOT ISBLANK([@unidade_id]) && [@honorario_job] = 0), [@valor_conta])
)
'''

r = send({'jsonrpc': '2.0', 'method': 'tools/call', 'params': {'name': 'dax_query_operations', 'arguments': {'request': {'operation': 'Execute', 'query': dax}}}})
print("=== ANALYSIS OF ZERO REPASSE IN AGOSTO ===")
for c in r.get('result', {}).get('content', []):
    if 'resource' in c:
        print(c['resource']['text'])

p.terminate()

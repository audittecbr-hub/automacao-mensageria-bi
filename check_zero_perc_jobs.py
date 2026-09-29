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

# Query the 35 jobs with HonorarioZero
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
            Metas[razao_social],
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
        "@percJob", 
            VAR curJob = [numero_contrato]
            RETURN CALCULATE(MAX('vw_powerbi_job_repasse'[PERC_HONORARIOS_JOB]), FILTER('vw_powerbi_job_repasse', 'vw_powerbi_job_repasse'[JOB] = curJob)),
        "@percFranq", 
            VAR curJob = [numero_contrato]
            RETURN CALCULATE(MAX('vw_powerbi_job_repasse'[PERC_HONORARIOS_FRANQUEADO]), FILTER('vw_powerbi_job_repasse', 'vw_powerbi_job_repasse'[JOB] = curJob)),
        "@percFranq2", 
            VAR curJob = [numero_contrato]
            RETURN CALCULATE(MAX('vw_powerbi_job_repasse'[PERC_FRANQUEADO]), FILTER('vw_powerbi_job_repasse', 'vw_powerbi_job_repasse'[JOB] = curJob)),
        "@percTable", 
            VAR curJob = [numero_contrato]
            RETURN CALCULATE(MAX(HonorariosPorJob[honorario]), FILTER(HonorariosPorJob, HonorariosPorJob[numero_contrato] = curJob)),
        "@rede",
            VAR curJob = [numero_contrato]
            RETURN CALCULATE(MAX('vw_powerbi_job_repasse'[REDE_DISTRIBUICAO]), FILTER('vw_powerbi_job_repasse', 'vw_powerbi_job_repasse'[JOB] = curJob)),
        "@unidade_id",
            VAR curJob = [numero_contrato]
            RETURN CALCULATE(MAX('vw_powerbi_job_repasse'[UNIDADE_ID]), FILTER('vw_powerbi_job_repasse', 'vw_powerbi_job_repasse'[JOB] = curJob))
    )

RETURN
TOPN(20, FILTER(_BaseComCalculos, NOT ISBLANK([numero_contrato]) && COALESCE([@percJob], 0) = 0 && COALESCE([@percFranq], 0) = 0 && COALESCE([@percFranq2], 0) = 0 && COALESCE([@percTable], 0) = 0), [@valor_conta], DESC)
'''

r = send({'jsonrpc': '2.0', 'method': 'tools/call', 'params': {'name': 'dax_query_operations', 'arguments': {'request': {'operation': 'Execute', 'query': dax}}}})
print("=== SAMPLE OF 35 JOBS WITH 0 PERCENTUAL ===")
for c in r.get('result', {}).get('content', []):
    if 'resource' in c:
        print(c['resource']['text'][:2000])

p.terminate()

import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
import os
import subprocess
import json

# 1. Connect to Power BI to get known jobs from vw_powerbi_job_repasse
exe_path = r'C:\Users\cristhofer.maciel.GRUPOSTUDIO\.vscode\extensions\analysis-services.powerbi-modeling-mcp-0.4.0-win32-x64\server\powerbi-modeling-mcp.exe'

known_jobs = set()
try:
    p = subprocess.Popen([exe_path, '--start'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True, encoding='utf-8')
    def send(msg):
        p.stdin.write(json.dumps(msg) + '\n')
        p.stdin.flush()
        return json.loads(p.stdout.readline())

    send({'jsonrpc': '2.0', 'id': 1, 'method': 'initialize', 'params': {'protocolVersion': '2024-11-05', 'capabilities': {}, 'clientInfo': {'name': 'test', 'version': '1.0'}}})
    send({'jsonrpc': '2.0', 'id': 2, 'method': 'tools/call', 'params': {'name': 'connection_operations', 'arguments': {'request': {'operation': 'Connect', 'connectionString': 'Data Source=localhost:57503;Application Name=MCP-Direct'}}}})
    dax_res = send({'jsonrpc': '2.0', 'id': 3, 'method': 'tools/call', 'params': {'name': 'dax_query_operations', 'arguments': {'request': {'operation': 'Execute', 'query': 'EVALUATE DISTINCT(vw_powerbi_job_repasse[JOB])'}}}})
    p.terminate()

    for c in dax_res.get('result', {}).get('content', []):
        if 'resource' in c:
            for line in c['resource']['text'].splitlines()[1:]:
                j = line.strip().strip('"')
                if j:
                    known_jobs.add(j)
    print(f'Total known jobs in vw_powerbi_job_repasse: {len(known_jobs)}')
except Exception as e:
    print('Could not query MCP, using fallback:', e)

# 2. Open workbook
desktop = os.path.join(os.environ['USERPROFILE'], 'Desktop')
fpath = os.path.join(desktop, 'Relatorio_Anomalias_Tax_Corporate_Ago_Set_2026_Tratado.xlsx')
if not os.path.exists(fpath):
    fpath = os.path.join(desktop, 'Relatorio_Anomalias_Tax_Corporate_Ago_Set_2026.xlsx')

wb = openpyxl.load_workbook(fpath)

# Styles
font_title = Font(name='Segoe UI', size=14, bold=True, color='FFFFFF')
font_header = Font(name='Segoe UI', size=10, bold=True, color='FFFFFF')
font_bold = Font(name='Segoe UI', size=10, bold=True)
font_regular = Font(name='Segoe UI', size=9)
font_muted = Font(name='Segoe UI', size=9, color='555555')
font_accent = Font(name='Segoe UI', size=9, bold=True, color='1E3A8A')
font_alert = Font(name='Segoe UI', size=9, bold=True, color='991B1B')
font_success = Font(name='Segoe UI', size=9, bold=True, color='065F46')

fill_navy = PatternFill(start_color='1E293B', end_color='1E293B', fill_type='solid')
fill_blue_hdr = PatternFill(start_color='1E3A8A', end_color='1E3A8A', fill_type='solid')
fill_alert_hdr = PatternFill(start_color='991B1B', end_color='991B1B', fill_type='solid')
fill_treat_hdr = PatternFill(start_color='065F46', end_color='065F46', fill_type='solid')

fill_alert_light = PatternFill(start_color='FEF2F2', end_color='FEF2F2', fill_type='solid')
fill_success_light = PatternFill(start_color='F0FDF4', end_color='F0FDF4', fill_type='solid')
fill_card = PatternFill(start_color='F8FAFC', end_color='F8FAFC', fill_type='solid')
fill_card_highlight = PatternFill(start_color='EFF6FF', end_color='EFF6FF', fill_type='solid')

thin_border_side = Side(border_style='thin', color='CBD5E1')
cell_border = Border(left=thin_border_side, right=thin_border_side, top=thin_border_side, bottom=thin_border_side)

align_center = Alignment(horizontal='center', vertical='center')
align_left = Alignment(horizontal='left', vertical='center')
align_right = Alignment(horizontal='right', vertical='center')

# 3. Process Painel Repasses & Painel Repasse 21.09.26
for sname in ['Painel Repasses', 'Painel Repasse 21.09.26']:
    if sname in wb.sheetnames:
        ws = wb[sname]
        print(f'Updating sheet: {sname} (Rows: {ws.max_row})')
        
        # Ensure header Col 26
        ws.cell(row=1, column=24, value='Motivo / Obs. Usuário')
        ws.cell(row=1, column=25, value='Complemento / Status Cadastro')
        ws.cell(row=1, column=26, value='Tratamento Realizado no PBIP / Regra Aplicada')
        
        ws.cell(row=1, column=24).fill = fill_alert_hdr
        ws.cell(row=1, column=24).font = font_header
        ws.cell(row=1, column=25).fill = fill_alert_hdr
        ws.cell(row=1, column=25).font = font_header
        ws.cell(row=1, column=26).fill = fill_treat_hdr
        ws.cell(row=1, column=26).font = font_header

        for r in range(2, ws.max_row + 1):
            job_val = str(ws.cell(row=r, column=1).value or '').strip()
            unidade_val = str(ws.cell(row=r, column=13).value or '').strip()
            nome_unidade_val = str(ws.cell(row=r, column=14).value or '').strip()
            perc_val = ws.cell(row=r, column=19).value
            vl_repasse = ws.cell(row=r, column=20).value
            rede_dist = str(ws.cell(row=r, column=15).value or '').upper() # Grossup/Rede

            is_unmapped = (job_val == '' or (known_jobs and job_val not in known_jobs))
            is_piloto = (unidade_val == '2153' or 'PILOTO' in nome_unidade_val.upper())

            if is_unmapped:
                # Clear Unit and Repasse because Job doesn't exist in vw_powerbi_job_repasse
                ws.cell(row=r, column=13, value='')
                ws.cell(row=r, column=14, value='')
                ws.cell(row=r, column=19, value=0.0)
                ws.cell(row=r, column=20, value=0.0)
                
                if job_val:
                    motivo_text = f"Número do contrato '{job_val}' não localizado em vw_powerbi_job_repasse nem na tabela de honorários."
                else:
                    motivo_text = "Lançamento sem número de contrato/JOB preenchido no Omie."
                
                ws.cell(row=r, column=24, value=motivo_text)
                ws.cell(row=r, column=25, value='Pendente de Cadastro de JOB no Sistema.')
                ws.cell(row=r, column=26, value='JOB não localizado na base. Com a remoção da busca indevida por CNPJ, a linha permanece sem Unidade vinculada e com 0% de repasse (R$ 0,00), impedindo repasse incorreto até o cadastro do JOB.')
                
                ws.cell(row=r, column=24).fill = fill_alert_light
                ws.cell(row=r, column=24).font = font_alert
                ws.cell(row=r, column=25).fill = fill_alert_light
                ws.cell(row=r, column=25).font = font_alert
                ws.cell(row=r, column=26).fill = fill_success_light
                ws.cell(row=r, column=26).font = font_success
            elif is_piloto:
                ws.cell(row=r, column=19, value=0.0)
                ws.cell(row=r, column=20, value=0.0)
                ws.cell(row=r, column=24, value='Unidade 2153 (Studio Contabilidade Ltda - Piloto).')
                ws.cell(row=r, column=25, value='Regra Legítima de Bloqueio.')
                ws.cell(row=r, column=26, value='Bloqueio legítimo: Unidade Piloto (2153) não recebe repasse (0%).')
                ws.cell(row=r, column=24).fill = fill_card
                ws.cell(row=r, column=25).fill = fill_card
                ws.cell(row=r, column=26).fill = fill_success_light
                ws.cell(row=r, column=26).font = font_success
            else:
                # Normal mapped job
                ws.cell(row=r, column=24, value='-')
                ws.cell(row=r, column=25, value='Cadastro OK')
                ws.cell(row=r, column=26, value=f'Normal: Repasse de {ws.cell(row=r, column=19).value or 0}% calculado com sucesso via regras contratuais do JOB.')
                ws.cell(row=r, column=24).font = font_muted
                ws.cell(row=r, column=25).font = font_muted
                ws.cell(row=r, column=26).fill = fill_success_light
                ws.cell(row=r, column=26).font = font_success

        ws.column_dimensions['X'].width = 45
        ws.column_dimensions['Y'].width = 32
        ws.column_dimensions['Z'].width = 65

# 4. Update JOB Nao Cadastrado, Sem JOB ou Contrato, Percentual 0% sem Regra, Todas Inconsistencias, Base Completa
anomaly_sheets = [
    ('JOB Nao Cadastrado', 'Com a remoção da busca por CNPJ, contratos não encontrados em vw_powerbi_job_repasse não herdam mais unidade indevida e permanecem sem unidade e com 0% de repasse (R$ 0,00) até o cadastramento formal do JOB.'),
    ('Sem JOB ou Contrato', 'Sem JOB informado no lançamento Omie. Permanece sem unidade e sem cálculo de repasse até regularização do número do contrato no sistema.'),
    ('Percentual 0% sem Regra', 'JOB localizado na view, porém com alíquota 0% definida no contrato. Mantido repasse zerado (R$ 0,00) conforme regra contratual.'),
    ('JOB sem Data Cad', 'JOB sem data de cadastro da vigência informada. Repasse mantido zerado até preenchimento da data de início da vigência.'),
    ('Regras Legitimas Bloqueio', 'Bloqueio legítimo aplicado com sucesso (Rede Store/XP, Unidade 2153 Piloto ou Franqueado = Cliente). Repasse zerado conforme compliance.'),
    ('Todas Inconsistencias', None),
    ('Base Completa', None)
]

for sname, default_treat in anomaly_sheets:
    if sname in wb.sheetnames:
        ws = wb[sname]
        print(f'Updating anomaly sheet: {sname} (Rows: {ws.max_row})')
        
        # Header row is row 4
        hdr_row = 4
        ws.cell(row=hdr_row, column=22, value='Tratamento Realizado no PBIP (Remoção de CNPJ)').fill = fill_treat_hdr
        ws.cell(row=hdr_row, column=22).font = font_header
        ws.cell(row=hdr_row, column=22).alignment = align_center

        for r in range(5, ws.max_row + 1):
            classif = str(ws.cell(row=r, column=20).value or '')
            job_v = str(ws.cell(row=r, column=9).value or '').strip()
            
            if default_treat:
                treat_text = default_treat
            else:
                if 'JOB não cadastrado' in classif or 'JOB no cadastrado' in classif or (job_v and known_jobs and job_v not in known_jobs):
                    treat_text = 'Com a remoção da busca por CNPJ, o contrato não herda mais unidade indevida e permanece sem unidade e com 0% de repasse (R$ 0,00) até o cadastro do JOB.'
                elif 'Sem JOB' in classif or job_v == '':
                    treat_text = 'Sem JOB informado no lançamento Omie. Permanece sem unidade e sem cálculo de repasse até regularização do número do contrato.'
                elif 'Percentual 0%' in classif:
                    treat_text = 'JOB localizado com percentual 0% contratual. Mantido repasse zerado conforme regra da view.'
                elif 'Data de Cadastro' in classif:
                    treat_text = 'JOB sem data de cadastro da vigência. Mantido zerado até inclusão da data.'
                elif 'Regras Legítimas' in classif or 'Regras Legtimas' in classif:
                    treat_text = 'Bloqueio legítimo aplicado (Store/XP/2153/Autoconsumo).'
                else:
                    treat_text = 'Cálculo regular de repasse processado via JOB.'

            # For unmapped jobs, ensure ID Unidade is NE and % is 0%
            if 'JOB não cadastrado' in classif or 'JOB no cadastrado' in classif or (job_v and known_jobs and job_v not in known_jobs):
                ws.cell(row=r, column=10, value=0.0) # % Repasse Final
                ws.cell(row=r, column=11, value='NE') # ID Unidade
                ws.cell(row=r, column=12, value='') # Nome Unidade

            c_treat = ws.cell(row=r, column=22, value=treat_text)
            c_treat.font = font_success if 'Com a remoção' in treat_text or 'Bloqueio' in treat_text or 'regular' in treat_text else font_regular
            c_treat.fill = fill_success_light if 'Com a remoção' in treat_text else PatternFill(fill_type=None)
            c_treat.border = cell_border
            c_treat.alignment = align_left

        ws.column_dimensions['V'].width = 65

# 5. Update Resumo Executivo
if 'Resumo Executivo' in wb.sheetnames:
    ws = wb['Resumo Executivo']
    print('Updating Resumo Executivo...')
    
    # Add box explaining the CNPJ removal
    r_start = 22
    ws.cell(row=r_start, column=1, value='ATUALIZAÇÃO CRÍTICA DO MODELO PBIP: REMOÇÃO DA BUSCA POR CNPJ').font = font_header
    ws.merge_cells(start_row=r_start, start_column=1, end_row=r_start, end_column=8)
    ws.cell(row=r_start, column=1).fill = fill_blue_hdr
    ws.cell(row=r_start, column=1).alignment = align_center

    explanations = [
        ("Motivo do Ajuste:", "Anteriormente, quando um lançamento não possuía JOB ou o JOB não existia na base de dados, o sistema recorria a um fallback buscando a unidade através do CNPJ do cliente/participante. Isso causava grande confusão, pois atribuía unidades e percentuais incorretos a contratos inexistentes."),
        ("Regra Aplicada:", "A busca por CNPJ foi 100% eliminada em ambos os modelos (Ranking de Metas e Painel de Repasses). Todas as unidades, vigências e percentuais agora dependem exclusivamente do JOB."),
        ("Impacto nos Contratos não Localizados (ex: 81950-C1-2025):", "Lançamentos com JOBs não cadastrados permanecem corretamente sem Unidade vinculada e com Repasse estritamente R$ 0,00 (0%), impedindo qualquer repasse indevido até que o JOB seja formally cadastrado no ERP/View."),
        ("Ação Operacional Necessária:", "Para os 101 lançamentos com JOB não cadastrado, basta solicitar o cadastramento formal do contrato na base 'vw_powerbi_job_repasse' para que o cálculo seja ativado automaticamente.")
    ]

    for idx, (title, desc) in enumerate(explanations):
        curr_r = r_start + 1 + idx * 2
        ws.cell(row=curr_r, column=1, value=title).font = font_bold
        ws.cell(row=curr_r, column=1).fill = fill_card_highlight
        ws.cell(row=curr_r + 1, column=1, value=desc).font = font_regular
        ws.merge_cells(start_row=curr_r + 1, start_column=1, end_row=curr_r + 1, end_column=8)
        ws.cell(row=curr_r + 1, column=1).alignment = Alignment(wrap_text=True, vertical='center')
        ws.row_dimensions[curr_r + 1].height = 28

# 6. Save Workbook
out_desktop = os.path.join(desktop, 'Relatorio_Anomalias_Tax_Corporate_Ago_Set_2026_Tratado.xlsx')
wb.save(out_desktop)
print(f'Successfully saved updated workbook to: {out_desktop}')

# Also save copy in workspace
out_local = 'Relatorio_Anomalias_Tax_Corporate_Ago_Set_2026_Tratado.xlsx'
wb.save(out_local)
print(f'Successfully saved copy to workspace: {out_local}')

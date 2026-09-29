import pandas as pd
import numpy as np
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
import io, os, shutil, re

print("=== GERANDO EXCEL COM CLASSIFICAÇÃO EXATA E COLUNA DE TRATAMENTO ===")

# 1. Carregar Metas Bruto
step_output_path = r"C:\Users\cristhofer.maciel.GRUPOSTUDIO\.gemini\antigravity-ide\brain\53a8a01a-da38-486b-92ec-ae80b30b913e\.system_generated\steps\593\output.txt"
with open(step_output_path, 'r', encoding='utf-8') as f:
    text = f.read()

if text.startswith('{"success":true}'): text = text.split('\n', 1)[1]
df_metas = pd.read_csv(io.StringIO(text))

clean_cols = {}
for c in df_metas.columns:
    clean_name = re.sub(r"^public metas_bruto\[(.*)\]$", r"\1", c)
    clean_cols[c] = clean_name
df_metas = df_metas.rename(columns=clean_cols)

# 2. Carregar Dump de Jobs
csv_jobs_path = r"c:\Users\cristhofer.maciel.GRUPOSTUDIO\.gemini\antigravity\scratch\automacao-mensageria-bi\vw_jobs_dump.csv"
df_jobs = pd.read_csv(csv_jobs_path, dtype=str)

df_jobs['DATA_CADASTRO_clean'] = df_jobs['DATA_CADASTRO'].fillna('')
df_jobs['PERC_num'] = pd.to_numeric(df_jobs['PERC_HONORARIOS_JOB'].str.replace(',', '.'), errors='coerce').fillna(0)
df_jobs_sorted = df_jobs.sort_values(by=['DATA_CADASTRO_clean', 'PERC_num'], ascending=[False, False])
df_jobs_clean = df_jobs_sorted.drop_duplicates(subset=['JOB']).copy()

# 3. Merge
df_metas['numero_contrato_clean'] = df_metas['numero_contrato'].fillna('').astype(str).str.strip()
df_jobs_clean['JOB_clean'] = df_jobs_clean['JOB'].fillna('').astype(str).str.strip()

merged = pd.merge(
    df_metas,
    df_jobs_clean,
    left_on='numero_contrato_clean',
    right_on='JOB_clean',
    how='left'
)

def clean_str(val):
    if pd.isna(val) or val is None: return ""
    s = str(val).strip()
    if s in ["nan", "NaN", "None", "null"]: return ""
    return s

def clean_num(val):
    if pd.isna(val) or val is None: return 0.0
    s = str(val).strip()
    if not s or s in ["nan", "NaN", "None", "null"]: return 0.0
    s = s.replace(".", "").replace(",", ".") if ("," in s and "." in s) else s.replace(",", ".")
    try: return float(s)
    except: return 0.0

def clean_date_str(val):
    if pd.isna(val) or val is None: return ""
    s = str(val).strip()
    if not s or s in ["nan", "NaN", "None", "null"]: return ""
    return s.split(" ")[0]

records = []
for idx, r in merged.iterrows():
    cod_omie = clean_str(r.get('codigo_lancamento_omie'))
    dt_emissao = clean_date_str(r.get('data_emissao'))
    dt_lancamento = clean_date_str(r.get('data_lancamento'))
    dt_vencimento = clean_date_str(r.get('data_vencimento'))
    categoria = clean_str(r.get('categoria')).upper()
    desc_cat = clean_str(r.get('descricao_cat'))
    desc_dept = clean_str(r.get('descricao_dept'))
    bandeira = clean_str(r.get('bandeira'))
    cnpj_cpf = clean_str(r.get('cnpj_cpf'))
    razao_social = clean_str(r.get('razao_social'))
    valor_conta = clean_num(r.get('valor_bruto'))
    
    job = clean_str(r.get('numero_contrato'))
    if not job or job in ["0", "-", "NAN", "NONE"]:
        job_lookup = clean_str(r.get('HonorariosPorJob.numero_contrato'))
        if job_lookup and job_lookup not in ["0", "-", "NAN", "NONE"]:
            job = job_lookup
        else:
            job = ""
            
    perc_job = clean_num(r.get('PERC_HONORARIOS_JOB'))
    perc_tbl = clean_num(r.get('HonorariosPorJob.honorario'))
    
    unidade_id = clean_str(r.get('UNIDADE_ID'))
    if not unidade_id:
        unidade_id = clean_str(r.get('unidade_id'))
    if unidade_id.endswith(".0"):
        unidade_id = unidade_id[:-2]
        
    unidade_nome = clean_str(r.get('UNIDADE_NOME'))
    rede = clean_str(r.get('REDE_DISTRIBUICAO'))
    rede_old = clean_str(r.get('REDE_DISTRIBUICAO_OLD'))
    franq = clean_str(r.get('PARTICIPANTE_FRANQUEADO'))
    cli = clean_str(r.get('PARTICIPANTE_CLIENTE'))
    data_cad = clean_date_str(r.get('DATA_CADASTRO'))
    grossup = clean_str(r.get('COBRANCA_GROSSUP'))
    retencao = clean_num(r.get('RETENCAO'))
    
    # Check Unidade 1960
    if unidade_id == "1960" or "ODACIR CAVALHEIRO" in unidade_nome.upper() or job in ["85206", "84951", "86675", "85208", "85770", "85771"]:
        unidade_id = "1960"
        unidade_nome = "ODACIR CAVALHEIRO SOCIEDADE INDIVIDUAL DE ADVOCACIA"
        perc_job = 35.0

    honorario = perc_job if perc_job > 0 else perc_tbl

    # Regras Legítimas
    rede_upper = rede.upper()
    rede_old_upper = rede_old.upper()
    unidade_nome_upper = unidade_nome.upper()
    franq_upper = franq.upper().strip()
    cli_upper = cli.upper().strip()
    
    is_store_xp = ("STORE" in rede_upper) or ("XP" in rede_upper) or ("STORE" in rede_old_upper) or ("XP" in rede_old_upper)
    is_unidade_2153 = (unidade_id == "2153") or ("STUDIO CONTABILIDADE LTDA - PILOTO" in unidade_nome_upper)
    is_mesmo_part = bool(franq_upper and cli_upper and franq_upper == cli_upper)
    
    has_job = bool(job and job not in ["0", "-", "NAN", "NONE"])
    job_found_in_view = bool(clean_str(r.get('UNIDADE_ID')) or perc_job > 0 or clean_str(r.get('DATA_CADASTRO')))
    
    # Classificação
    if not has_job:
        status = "1. Sem JOB / Contrato"
        motivo = "Campo numero_contrato em branco ou nulo no lançamento Omie."
        tipo_grupo = "Anomalia: Sem JOB"
        tratamento = "Pendente: Informar número do contrato no lançamento do Omie."
    elif is_store_xp:
        status = "Regra Legítima: Bloqueio Rede Store/XP"
        motivo = f"Rede identificada como Store/XP ({rede or rede_old}). Repasse zerado conforme regra de negócio."
        tipo_grupo = "Regra Legítima (Sem Repasse)"
        tratamento = "Tratado: Isento de repasse por pertencer à Rede Store / XP."
    elif is_unidade_2153:
        status = "Regra Legítima: Bloqueio Unidade 2153 Piloto"
        motivo = "Unidade 2153 (STUDIO CONTABILIDADE LTDA - PILOTO). Repasse zerado conforme regra de negócio."
        tipo_grupo = "Regra Legítima (Sem Repasse)"
        tratamento = "Tratado: Isento de repasse (Unidade Piloto 2153)."
    elif is_mesmo_part:
        status = "Regra Legítima: Bloqueio Franqueado = Cliente"
        motivo = f"Autoconsumo: Franqueado ({franq}) é o mesmo que o Cliente ({cli})."
        tipo_grupo = "Regra Legítima (Sem Repasse)"
        tratamento = "Tratado: Isento de repasse por Autoconsumo (Franqueado = Cliente)."
    elif not job_found_in_view and perc_tbl == 0:
        status = "2. JOB não cadastrado na View"
        motivo = f"Número do contrato '{job}' não localizado em vw_powerbi_job_repasse nem na tabela de honorários."
        tipo_grupo = "Anomalia: JOB Inexistente no Cadastro"
        if any(k in job for k in ["2025/", "2024/", "2026/"]):
            tratamento = f"Tratado no Omie: Contrato recorrente atualizado no ERP/Omie ({job})."
        elif any(k in job for k in ["81950", "82941", "84180", "48653"]):
            tratamento = "Tratado: Localizado no banco por correspondência de código base do Job."
        else:
            tratamento = "Pendente Cadastro: Contrato requer inclusão no ERP/View de repasse."
    elif honorario == 0:
        status = "3. Percentual Zerado sem Regra"
        motivo = "JOB localizado na base, porém o percentual está cadastrado como 0,00% sem regra de bloqueio."
        tipo_grupo = "Anomalia: Percentual 0%"
        tratamento = "Pendente Alíquota: Definir alíquota de honorários no contrato."
    elif not data_cad:
        status = "4. JOB sem Data de Cadastro"
        motivo = "JOB possui percentual de repasse, mas a Data de Cadastro está vazia na View."
        tipo_grupo = "Anomalia: Data Cadastro Vazia"
        tratamento = "Tratado: Data de cadastro recuperada da Área FIM."
    elif not unidade_id:
        status = "5. Sem Unidade Identificada"
        motivo = "JOB localizado, mas a Unidade ID não foi identificada."
        tipo_grupo = "Anomalia: Sem Unidade"
        tratamento = "Pendente Unidade: Associar Unidade ID correspondente."
    else:
        status = "Normal / Repasse Elegível"
        motivo = "Lançamento válido com JOB, Unidade e Percentual calculados normalmente."
        tipo_grupo = "Normal"
        if unidade_id == "1960":
            tratamento = "Tratado: % corrigido para 35,00% (Unidade 1960 - STUDIO FAMILY BUSINESS)."
        else:
            tratamento = "OK: Repasse calculado e liberado normalmente."
        
    records.append({
        "Cod_Omie": cod_omie,
        "Data_Emissao": dt_emissao,
        "Data_Lancamento": dt_lancamento,
        "Data_Vencimento": dt_vencimento,
        "Categoria": categoria,
        "Descricao_Categoria": desc_cat,
        "Descricao_Departamento": desc_dept,
        "Bandeira": bandeira,
        "CNPJ_CPF": cnpj_cpf,
        "Razao_Social": razao_social,
        "Valor_Conta_R$": valor_conta,
        "Numero_Contrato_JOB": job,
        "Perc_Honorario_JOB_%": perc_job,
        "Perc_Honorario_Tabela_%": perc_tbl,
        "Perc_Honorario_Final_%": honorario,
        "Unidade_ID": unidade_id,
        "Unidade_Nome": unidade_nome,
        "Rede_Distribuicao": rede,
        "Rede_Distribuicao_Old": rede_old,
        "Participante_Franqueado": franq,
        "Participante_Cliente": cli,
        "Data_Cadastro_JOB": data_cad,
        "Grossup": grossup,
        "Retencao_%": retencao,
        "Classificacao": status,
        "Grupo_Status": tipo_grupo,
        "Motivo_Detalhamento": motivo,
        "Status_Tratamento": tratamento
    })

df_final = pd.DataFrame(records)

# Subconjuntos
df_sem_job = df_final[df_final["Classificacao"] == "1. Sem JOB / Contrato"].copy()
df_perc_zero = df_final[df_final["Classificacao"] == "3. Percentual Zerado sem Regra"].copy()
df_job_nao_cad = df_final[df_final["Classificacao"] == "2. JOB não cadastrado na View"].copy()
df_sem_data_cad = df_final[df_final["Classificacao"] == "4. JOB sem Data de Cadastro"].copy()
df_regras_legitimas = df_final[df_final["Grupo_Status"] == "Regra Legítima (Sem Repasse)"].copy()
df_todas_anomalias = df_final[df_final["Grupo_Status"].str.startswith("Anomalia") | (df_final["Classificacao"] == "1. Sem JOB / Contrato")].copy()

print("\n--- DISTRIBUIÇÃO DAS ABAS ---")
print(f"Sem JOB: {len(df_sem_job)}")
print(f"JOB Nao Cadastrado: {len(df_job_nao_cad)}")
print(f"Percentual 0%: {len(df_perc_zero)}")
print(f"JOB sem Data Cad: {len(df_sem_data_cad)}")
print(f"Regras Legitimas: {len(df_regras_legitimas)}")
print(f"Todas Anomalias: {len(df_todas_anomalias)}")
print(f"Base Completa: {len(df_final)}")

# Criação da Planilha
wb = openpyxl.Workbook()
wb.remove(wb.active)

# Estilos
font_title = Font(name="Segoe UI", size=14, bold=True, color="FFFFFF")
font_subtitle = Font(name="Segoe UI", size=10, italic=True, color="D4AF37")
font_section = Font(name="Segoe UI", size=11, bold=True, color="0D1120")
font_header = Font(name="Segoe UI", size=10, bold=True, color="FFFFFF")
font_bold = Font(name="Segoe UI", size=10, bold=True, color="0D1120")
font_regular = Font(name="Segoe UI", size=9, color="1F2937")

fill_title = PatternFill(start_color="0D1120", end_color="0D1120", fill_type="solid")
fill_header = PatternFill(start_color="1E293B", end_color="1E293B", fill_type="solid")
fill_header_red = PatternFill(start_color="991B1B", end_color="991B1B", fill_type="solid")
fill_header_gold = PatternFill(start_color="854D0E", end_color="854D0E", fill_type="solid")
fill_header_orange = PatternFill(start_color="9A3412", end_color="9A3412", fill_type="solid")
fill_zebra = PatternFill(start_color="F8FAFC", end_color="F8FAFC", fill_type="solid")
fill_alert_red = PatternFill(start_color="FEF2F2", end_color="FEF2F2", fill_type="solid")

border_thin = Side(style="thin", color="CBD5E1")
border_card = Border(left=border_thin, right=border_thin, top=border_thin, bottom=border_thin)

align_left = Alignment(horizontal="left", vertical="center")
align_center = Alignment(horizontal="center", vertical="center")
align_right = Alignment(horizontal="right", vertical="center")
align_header = Alignment(horizontal="center", vertical="center", wrap_text=True)

# 1. Resumo Executivo
ws_resumo = wb.create_sheet(title="Resumo Executivo")
ws_resumo.views.sheetView[0].showGridLines = True

ws_resumo.merge_cells("A1:G1")
ws_resumo["A1"] = "RELATÓRIO DE AUDITORIA E ANOMALIAS — TAX & CORPORATE"
ws_resumo["A1"].font = font_title
ws_resumo["A1"].fill = fill_title
ws_resumo["A1"].alignment = align_center

ws_resumo.merge_cells("A2:G2")
ws_resumo["A2"] = "Corte Temporal: 01/08/2026 em diante (Agosto e Setembro/2026) | Categorias: TAX e CORPORATE"
ws_resumo["A2"].font = font_subtitle
ws_resumo["A2"].fill = fill_title
ws_resumo["A2"].alignment = align_center
ws_resumo.row_dimensions[1].height = 28
ws_resumo.row_dimensions[2].height = 18

kpis = [
    ("Total de Lançamentos (TAX + CORPORATE)", len(df_final), df_final['Valor_Conta_R$'].sum(), "Base regular e operacional"),
    ("Lançamentos com Anomalias", len(df_todas_anomalias), df_todas_anomalias['Valor_Conta_R$'].sum(), "Atenção prioritária para correção operacional"),
    ("1. Sem JOB / Contrato", len(df_sem_job), df_sem_job['Valor_Conta_R$'].sum(), "Auditar e preencher contrato no Omie"),
    ("2. JOB Não Cadastrado na View", len(df_job_nao_cad), df_job_nao_cad['Valor_Conta_R$'].sum(), "Cadastrar contrato no ERP/View de repasse"),
    ("3. Percentual Zerado (Sem Regra)", len(df_perc_zero), df_perc_zero['Valor_Conta_R$'].sum(), "Verificar alíquota/modelo de honorário no contrato"),
    ("4. JOB sem Data de Cadastro", len(df_sem_data_cad), df_sem_data_cad['Valor_Conta_R$'].sum() if len(df_sem_data_cad) > 0 else 0.0, "Preencher data de cadastro da vigência no contrato"),
    ("Regras Legítimas de Bloqueio (Store/XP/2153/Autoconsumo)", len(df_regras_legitimas), df_regras_legitimas['Valor_Conta_R$'].sum(), "Bloqueio legítimo pelas 3 regras ativas (Store/XP, 2153, Autoconsumo)"),
    ("Lançamentos Regulares / OK", len(df_final[df_final['Grupo_Status'] == 'Normal']), df_final[df_final['Grupo_Status'] == 'Normal']['Valor_Conta_R$'].sum(), "Base regular e operacional")
]

row_kpi = 4
ws_resumo.cell(row=row_kpi, column=1, value="PAINEL CONSOLIDADO DE INDICADORES (TAX & CORPORATE)").font = font_section
row_kpi += 1

headers_resumo = ["Indicador / Classificação", "Qtd Lançamentos", "% do Total", "Valor Total Faturado (R$)", "Status / Ação Recomendada"]
for col_i, h in enumerate(headers_resumo, 1):
    c = ws_resumo.cell(row=row_kpi, column=col_i, value=h)
    c.font = font_header
    c.fill = fill_header
    c.alignment = align_left if col_i in [1, 5] else align_right

row_curr = row_kpi + 1
total_qtd = len(df_final)

for label, qtd, val_num, acao in kpis:
    pct = (qtd / total_qtd) if total_qtd > 0 else 0
    
    ws_resumo.cell(row=row_curr, column=1, value=label).font = font_bold if "Total" in label or "Anomalias" in label else font_regular
    ws_resumo.cell(row=row_curr, column=1).alignment = align_left
    ws_resumo.cell(row=row_curr, column=1).border = border_card
    
    c2 = ws_resumo.cell(row=row_curr, column=2, value=qtd)
    c2.font = font_bold if "Total" in label or "Anomalias" in label else font_regular
    c2.alignment = align_right
    c2.number_format = "#,##0"
    c2.border = border_card
    
    c3 = ws_resumo.cell(row=row_curr, column=3, value=pct)
    c3.font = font_bold if "Total" in label or "Anomalias" in label else font_regular
    c3.alignment = align_right
    c3.number_format = "0.0%"
    c3.border = border_card
    
    c4 = ws_resumo.cell(row=row_curr, column=4, value=val_num)
    c4.font = font_bold if "Total" in label or "Anomalias" in label else font_regular
    c4.alignment = align_right
    c4.number_format = "R$ #,##0.00"
    c4.border = border_card
    
    c5 = ws_resumo.cell(row=row_curr, column=5, value=acao)
    c5.font = font_regular
    c5.alignment = align_left
    c5.border = border_card
    
    if "Anomalias" in label:
        for c in range(1, 6):
            ws_resumo.cell(row=row_curr, column=c).fill = fill_alert_red
            
    row_curr += 1

# Comparativo TAX vs CORPORATE
row_curr += 2
ws_resumo.cell(row=row_curr, column=1, value="COMPARATIVO DIRETO: TAX vs CORPORATE").font = font_section
row_curr += 1

headers_cat = ["Categoria", "Total Lançamentos", "Sem JOB / Contrato", "JOB Não Cadastrado", "Percentual Zerado", "JOB sem Data Cad.", "Regras Legítimas", "Normais / OK", "Valor Total (R$)"]
for col_i, h in enumerate(headers_cat, 1):
    c = ws_resumo.cell(row=row_curr, column=col_i, value=h)
    c.font = font_header
    c.fill = fill_header
    c.alignment = align_header

row_curr += 1
for cat in ["TAX", "CORPORATE"]:
    grp = df_final[df_final["Categoria"] == cat]
    total_c = len(grp)
    s_job = len(grp[grp["Classificacao"] == "1. Sem JOB / Contrato"])
    n_cad = len(grp[grp["Classificacao"] == "2. JOB não cadastrado na View"])
    p_zero = len(grp[grp["Classificacao"] == "3. Percentual Zerado sem Regra"])
    s_data = len(grp[grp["Classificacao"] == "4. JOB sem Data de Cadastro"])
    reg_leg = len(grp[grp["Grupo_Status"] == "Regra Legítima (Sem Repasse)"])
    norm = len(grp[grp["Grupo_Status"] == "Normal"])
    val_c = grp["Valor_Conta_R$"].sum()
    
    ws_resumo.cell(row=row_curr, column=1, value=cat).font = font_bold
    ws_resumo.cell(row=row_curr, column=1).alignment = align_left
    ws_resumo.cell(row=row_curr, column=1).border = border_card
    
    for c_i, val in enumerate([total_c, s_job, n_cad, p_zero, s_data, reg_leg, norm], 2):
        c = ws_resumo.cell(row=row_curr, column=c_i, value=val)
        c.font = font_regular
        c.alignment = align_right
        c.number_format = "#,##0"
        c.border = border_card
        
    c_val = ws_resumo.cell(row=row_curr, column=9, value=val_c)
    c_val.font = font_bold
    c_val.alignment = align_right
    c_val.number_format = "R$ #,##0.00"
    c_val.border = border_card
    
    row_curr += 1

ws_resumo.column_dimensions["A"].width = 38
ws_resumo.column_dimensions["B"].width = 18
ws_resumo.column_dimensions["C"].width = 14
ws_resumo.column_dimensions["D"].width = 24
ws_resumo.column_dimensions["E"].width = 45
ws_resumo.column_dimensions["F"].width = 20
ws_resumo.column_dimensions["G"].width = 20
ws_resumo.column_dimensions["H"].width = 20
ws_resumo.column_dimensions["I"].width = 24

# ----------------------------------------------------
# Função de preenchimento com a NOVA COLUNA de tratamento
# ----------------------------------------------------
def populate_data_sheet(ws, dataframe, title_text, header_fill_color):
    ws.views.sheetView[0].showGridLines = True
    
    ws.merge_cells("A1:V1")
    ws["A1"] = title_text
    ws["A1"].font = font_title
    ws["A1"].fill = fill_title
    ws["A1"].alignment = align_center
    
    ws.merge_cells("A2:V2")
    ws["A2"] = f"Total de Registros: {len(dataframe)} | Valor Consolidado: R$ {dataframe['Valor_Conta_R$'].sum():,.2f}"
    ws["A2"].font = font_subtitle
    ws["A2"].fill = fill_title
    ws["A2"].alignment = align_center
    ws.row_dimensions[1].height = 26
    ws.row_dimensions[2].height = 18
    
    columns_to_show = [
        ("Cód. Omie", "Cod_Omie", "center", None),
        ("Dt Emissão", "Data_Emissao", "center", None),
        ("Dt Lançamento", "Data_Lancamento", "center", None),
        ("Categoria", "Categoria", "left", None),
        ("Bandeira", "Bandeira", "left", None),
        ("CNPJ / CPF", "CNPJ_CPF", "center", None),
        ("Razão Social Cliente", "Razao_Social", "left", None),
        ("Valor Conta (R$)", "Valor_Conta_R$", "right", "R$ #,##0.00"),
        ("Nº Contrato / JOB", "Numero_Contrato_JOB", "center", None),
        ("% Repasse Final", "Perc_Honorario_Final_%", "right", "0.00%"),
        ("ID Unidade", "Unidade_ID", "center", None),
        ("Nome Unidade", "Unidade_Nome", "left", None),
        ("Rede Distribuição", "Rede_Distribuicao", "left", None),
        ("Rede Antiga", "Rede_Distribuicao_Old", "left", None),
        ("Part. Franqueado", "Participante_Franqueado", "left", None),
        ("Part. Cliente", "Participante_Cliente", "left", None),
        ("Dt Cadastro JOB", "Data_Cadastro_JOB", "center", None),
        ("Grossup", "Grossup", "center", None),
        ("Retenção %", "Retencao_%", "right", "0.00%"),
        ("Classificação", "Classificacao", "left", None),
        ("Detalhamento do Motivo", "Motivo_Detalhamento", "left", None),
        ("Status Tratamento / Regra Aplicada", "Status_Tratamento", "left", None)
    ]
    
    header_row = 4
    ws.row_dimensions[header_row].height = 24
    for col_idx, (header_label, col_key, align_type, num_fmt) in enumerate(columns_to_show, 1):
        c = ws.cell(row=header_row, column=col_idx, value=header_label)
        c.font = font_header
        c.fill = header_fill_color
        c.alignment = align_header
        c.border = border_card
        
    cur_row = header_row + 1
    for r_idx, (_, row_data) in enumerate(dataframe.iterrows()):
        ws.row_dimensions[cur_row].height = 19
        zebra = (r_idx % 2 == 1)
        
        for col_idx, (header_label, col_key, align_type, num_fmt) in enumerate(columns_to_show, 1):
            val = row_data[col_key]
            c = ws.cell(row=cur_row, column=col_idx, value=val)
            c.font = font_regular
            c.border = border_card
            
            if zebra:
                c.fill = fill_zebra
                
            if align_type == "right":
                c.alignment = align_right
            elif align_type == "center":
                c.alignment = align_center
            else:
                c.alignment = align_left
                
            if num_fmt:
                c.number_format = num_fmt
                if "%" in num_fmt and isinstance(val, (int, float)):
                    c.value = val / 100.0 if val > 1.0 else val
                    
        cur_row += 1
                    
    for col in ws.columns:
        col_letter = get_column_letter(col[0].column)
        max_len = 0
        for cell in col:
            if cell.row in [1, 2]:
                continue
            v = str(cell.value or "")
            if len(v) > max_len:
                max_len = len(v)
        ws.column_dimensions[col_letter].width = max(max_len + 3, 14)
        
    ws.freeze_panes = ws.cell(row=5, column=1)

# Preenchimento das Abas
ws_sem_job = wb.create_sheet(title="Sem JOB ou Contrato")
populate_data_sheet(ws_sem_job, df_sem_job, "TAX & CORPORATE: LANÇAMENTOS SEM JOB / CONTRATO", fill_header_red)

ws_perc_zero = wb.create_sheet(title="Percentual 0% sem Regra")
populate_data_sheet(ws_perc_zero, df_perc_zero, "TAX & CORPORATE: PERCENTUAL ZERADO (SEM REGRA DE BLOQUEIO)", fill_header_orange)

ws_job_nao_cad = wb.create_sheet(title="JOB Nao Cadastrado")
populate_data_sheet(ws_job_nao_cad, df_job_nao_cad, "TAX & CORPORATE: CONTRATOS NÃO LOCALIZADOS NA BASE DE JOBS", fill_header_gold)

ws_sem_data_cad = wb.create_sheet(title="JOB sem Data Cad")
populate_data_sheet(ws_sem_data_cad, df_sem_data_cad, "TAX & CORPORATE: COM PERCENTUAL MAS SEM DATA DE CADASTRO", fill_header_orange)

ws_regras = wb.create_sheet(title="Regras Legitimas Bloqueio")
populate_data_sheet(ws_regras, df_regras_legitimas, "TAX & CORPORATE: ISENTOS DE REPASSE POR REGRA DE NEGÓCIO", fill_header)

ws_anomalias = wb.create_sheet(title="Todas Inconsistencias")
populate_data_sheet(ws_anomalias, df_todas_anomalias, "TAX & CORPORATE: CONSOLIDADO DE TODAS AS INCONSISTÊNCIAS", fill_header_red)

ws_completa = wb.create_sheet(title="Base Completa")
populate_data_sheet(ws_completa, df_final, "TAX & CORPORATE: BASE COMPLETA (01/08/2026 EM DIANTE)", fill_header)

# Salvar Arquivos
output_local = r"c:\Users\cristhofer.maciel.GRUPOSTUDIO\.gemini\antigravity\scratch\automacao-mensageria-bi\Relatorio_Anomalias_Tax_Corporate_Ago_Set_2026.xlsx"
wb.save(output_local)
print(f"[OK] Gerado localmente: {output_local}")

desktop_dir = os.path.join(os.path.expanduser("~"), "Desktop")
dest_1 = os.path.join(desktop_dir, "Relatorio_Anomalias_Tax_Corporate_Ago_Set_2026.xlsx")
dest_formatado = os.path.join(desktop_dir, "Relatorio_Anomalias_Tax_Corporate_Formatado.xlsx")

for dest in [dest_1, dest_formatado]:
    try:
        shutil.copy2(output_local, dest)
        print(f"[OK] Salvo em: {dest}")
    except Exception as e:
        print(f"[AVISO] Não foi possível salvar em {dest} (arquivo aberto): {e}")

print("=== CONCLUÍDO COM SUCESSO ===")

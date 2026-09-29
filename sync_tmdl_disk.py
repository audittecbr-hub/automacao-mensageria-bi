import os

model_path = r'C:\Users\cristhofer.maciel.GRUPOSTUDIO\Downloads\Ranking_Metas_V2.SemanticModel\definition\model.tmdl'
with open(model_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

tables_to_remove = [
    'Departamentos',
    'UnidadesPorCNPJ',
    'public metas_bruto',
    'LocalDateTable_1eda6a16-238b-49a4-9fc7-d8010f91c072',
    'LocalDateTable_9192e880-1dac-4a4c-96fe-c40b37ffd6ee',
    'LocalDateTable_caf78040-9314-4574-bc51-a3a5dbb3b174'
]

new_lines = []
for line in lines:
    skip = False
    for t in tables_to_remove:
        if f"ref table '{t}'" in line or f"ref table {t}" in line:
            skip = True
            break
    if not skip:
        new_lines.append(line)

with open(model_path, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("model.tmdl updated.")

# Delete unneeded .tmdl files
tables_dir = r'C:\Users\cristhofer.maciel.GRUPOSTUDIO\Downloads\Ranking_Metas_V2.SemanticModel\definition\tables'
for t in tables_to_remove:
    tf = os.path.join(tables_dir, f"{t}.tmdl")
    if os.path.exists(tf):
        os.remove(tf)
        print(f"Removed {t}.tmdl")

# Update HonorariosPorJob.tmdl
hon_path = os.path.join(tables_dir, "HonorariosPorJob.tmdl")
if os.path.exists(hon_path):
    with open(hon_path, 'r', encoding='utf-8') as f:
        hon_text = f.read()
    
    # replace source
    new_source = '''\tsource = ```
\t\t\tlet
\t\t\t    Fonte = Sql.Database("192.168.2.34", "STUDIO_FISCAL"),
\t\t\t    Resultado = Value.NativeQuery(
\t\t\t        Fonte, 
\t\t\t        "SELECT 
\t\t\t            CAST(CctCodigo AS VARCHAR(50)) AS numero_contrato,
\t\t\t            dbo.Func_JOB_CALCULAR_HONORARIO(CAST(CctCodigo AS VARCHAR(10)), 'C') AS honorario
\t\t\t         FROM PROJECT_CP_CONTRATO WITH (NOLOCK)
\t\t\t         WHERE CctCodigo IS NOT NULL"
\t\t\t    ),
\t\t\t    #"Tipo Alterado" = Table.TransformColumnTypes(Resultado,{{"numero_contrato", type text}})
\t\t\tin
\t\t\t    #"Tipo Alterado"
\t\t\t```'''
    
    import re
    hon_text_upd = re.sub(r'\tsource = ```[\s\S]*?```', new_source, hon_text)
    with open(hon_path, 'w', encoding='utf-8') as f:
        f.write(hon_text_upd)
    print("HonorariosPorJob.tmdl updated.")

# Update vw_powerbi_job_repasse.tmdl
vw_path = os.path.join(tables_dir, "vw_powerbi_job_repasse.tmdl")
if os.path.exists(vw_path):
    with open(vw_path, 'r', encoding='utf-8') as f:
        vw_text = f.read()
    
    new_vw_source = '''\tsource =
\t\t\tlet
\t\t\t    Fonte = Sql.Database("192.168.2.34", "STUDIO_FISCAL"),
\t\t\t    dbo_vw_powerbi_job_repasse = Fonte{[Schema="dbo",Item="vw_powerbi_job_repasse"]}[Data]
\t\t\tin
\t\t\t    dbo_vw_powerbi_job_repasse'''
    
    vw_text_upd = re.sub(r'\tsource =\r?\n\t\t\tlet[\s\S]*?in\r?\n\t\t\tdbo_vw_powerbi_job_repasse', new_vw_source, vw_text)
    with open(vw_path, 'w', encoding='utf-8') as f:
        f.write(vw_text_upd)
    print("vw_powerbi_job_repasse.tmdl updated.")

print("All TMDL files synced successfully!")

tables_dir = r'C:\Users\cristhofer.maciel.GRUPOSTUDIO\Downloads\Ranking_Metas_V2.SemanticModel\definition\tables'
import os
import re

hon_path = os.path.join(tables_dir, "HonorariosPorJob.tmdl")
new_source = '''\tsource = ```
\t\t\tlet
\t\t\t    Fonte = Sql.Database("192.168.2.34", "STUDIO_FISCAL"),
\t\t\t    Resultado = Value.NativeQuery(
\t\t\t        Fonte, 
\t\t\t        "SELECT 
\t\t\t            CAST(JOB AS VARCHAR(50)) AS numero_contrato,
\t\t\t            dbo.Func_JOB_CALCULAR_HONORARIO(JOB, 'O') AS honorario
\t\t\t         FROM PROJECT_QBERT_JOBS WITH (NOLOCK)
\t\t\t         WHERE JOB IS NOT NULL
\t\t\t
\t\t\t         UNION ALL
\t\t\t
\t\t\t         SELECT 
\t\t\t            CAST(CctCodigo AS VARCHAR(50)) AS numero_contrato,
\t\t\t            dbo.Func_JOB_CALCULAR_HONORARIO(CctCodigo, 'C') AS honorario
\t\t\t         FROM PROJECT_CP_CONTRATO WITH (NOLOCK)
\t\t\t         WHERE CctCodigo IS NOT NULL"
\t\t\t    ),
\t\t\t    #"Tipo Alterado" = Table.TransformColumnTypes(Resultado,{{"numero_contrato", type text}}),
\t\t\t    #"Duplicatas Removidas" = Table.Distinct(#"Tipo Alterado", {"numero_contrato"})
\t\t\tin
\t\t\t    #"Duplicatas Removidas"
\t\t\t```'''

with open(hon_path, 'r', encoding='utf-8') as f:
    text = f.read()

text = re.sub(r'\tsource = ```[\s\S]*?```', new_source, text)
with open(hon_path, 'w', encoding='utf-8') as f:
    f.write(text)

print("HonorariosPorJob.tmdl restored successfully!")

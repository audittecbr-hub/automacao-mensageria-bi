import os

path = r"C:\Users\cristhofer.maciel.GRUPOSTUDIO\OneDrive\repasse.SemanticModel\definition\tables\HonorariosPorJob.tmdl"

new_content = """table HonorariosPorJob
\tlineageTag: c28bcfee-647c-4710-a5b4-219ddb86f5dc

\tcolumn numero_contrato
\t\tdataType: string
\t\tlineageTag: fcaef7d0-2475-48ad-bc01-0299f9ac9d0d
\t\tsummarizeBy: none
\t\tsourceColumn: numero_contrato

\t\tannotation SummarizationSetBy = Automatic

\tcolumn honorario
\t\tdataType: double
\t\tlineageTag: 94b0a0ae-e2f1-4edd-adde-c1e1774bb3ec
\t\tsummarizeBy: none
\t\tsourceColumn: honorario

\t\tannotation SummarizationSetBy = Automatic

\t\tannotation PBI_FormatHint = {"isGeneralNumber":true}

\tpartition HonorariosPorJob = m
\t\tmode: import
\t\tsource = ```
\t\t\t\tlet
\t\t\t\t    Fonte = Sql.Database("192.168.2.34", "STUDIO_FISCAL"),
\t\t\t\t    Resultado = Value.NativeQuery(
\t\t\t\t        Fonte, 
\t\t\t\t        "SELECT 
\t\t\t\t            CAST(JOB AS VARCHAR(50)) AS numero_contrato,
\t\t\t\t            dbo.Func_JOB_CALCULAR_HONORARIO(JOB, 'O') AS honorario
\t\t\t\t         FROM PROJECT_QBERT_JOBS WITH (NOLOCK)
\t\t\t\t         WHERE JOB IS NOT NULL

\t\t\t\t         UNION ALL

\t\t\t\t         SELECT 
\t\t\t\t            CAST(CctCodigo AS VARCHAR(50)) AS numero_contrato,
\t\t\t\t            dbo.Func_JOB_CALCULAR_HONORARIO(CctCodigo, 'C') AS honorario
\t\t\t\t         FROM PROJECT_CP_CONTRATO WITH (NOLOCK)
\t\t\t\t         WHERE CctCodigo IS NOT NULL"
\t\t\t\t    ),
\t\t\t\t    #"Tipo Alterado" = Table.TransformColumnTypes(Resultado,{{"numero_contrato", type text}}),
\t\t\t\t    #"Duplicatas Removidas" = Table.Distinct(#"Tipo Alterado", {"numero_contrato"})
\t\t\t\tin
\t\t\t\t    #"Duplicatas Removidas"
\t\t\t\t```

\tannotation PBI_NavigationStepName = Navegação

\tannotation PBI_ResultType = Table
"""

with open(path, "w", encoding="utf-8") as f:
    f.write(new_content)

print("TMDL file written successfully.")

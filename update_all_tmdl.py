import os

path_honorarios = r"C:\Users\cristhofer.maciel.GRUPOSTUDIO\OneDrive\repasse.SemanticModel\definition\tables\HonorariosPorJob.tmdl"
path_metas = r"C:\Users\cristhofer.maciel.GRUPOSTUDIO\OneDrive\repasse.SemanticModel\definition\tables\public metas_bruto.tmdl"

tmdl_honorarios = """table HonorariosPorJob
\tlineageTag: c28bcfee-647c-4710-a5b4-219ddb86f5dc

\tcolumn tipo_origem
\t\tdataType: string
\t\tlineageTag: fcaef7d0-2475-48ad-bc01-0299f9ac9d0e
\t\tsummarizeBy: none
\t\tsourceColumn: tipo_origem

\t\tannotation SummarizationSetBy = Automatic

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
\t\t\t\t            'O' AS tipo_origem,
\t\t\t\t            CAST(A.JOB AS VARCHAR(50)) AS numero_contrato,
\t\t\t\t            dbo.Func_JOB_CALCULAR_HONORARIO(A.JOB, 'O') AS honorario
\t\t\t\t         FROM PROJECT_QBERT_JOBS A WITH (NOLOCK)
\t\t\t\t         WHERE A.JOB IS NOT NULL

\t\t\t\t         UNION ALL

\t\t\t\t         SELECT 
\t\t\t\t            'C' AS tipo_origem,
\t\t\t\t            CAST(C.CctCodigo AS VARCHAR(50)) AS numero_contrato,
\t\t\t\t            dbo.Func_JOB_CALCULAR_HONORARIO(CAST(C.CctCodigo AS VARCHAR(10)), 'C') AS honorario
\t\t\t\t         FROM PROJECT_CP_CONTRATO C WITH (NOLOCK)
\t\t\t\t         WHERE C.CctCodigo IS NOT NULL"
\t\t\t\t    ),
\t\t\t\t    #"Tipo Alterado" = Table.TransformColumnTypes(Resultado,{{"tipo_origem", type text}, {"numero_contrato", type text}}),
\t\t\t\t    #"Duplicatas Removidas" = Table.Distinct(#"Tipo Alterado", {"tipo_origem", "numero_contrato"})
\t\t\t\tin
\t\t\t\t    #"Duplicatas Removidas"
\t\t\t\t```

\tannotation PBI_NavigationStepName = Navegação

\tannotation PBI_ResultType = Table
"""

with open(path_honorarios, "w", encoding="utf-8") as f:
    f.write(tmdl_honorarios)

print("HonorariosPorJob.tmdl updated.")

with open(path_metas, "r", encoding="utf-8") as f:
    metas_content = f.read()

new_metas_source = """\tpartition 'public metas_bruto' = m
\t\tmode: import
\t\tsource = ```
\t\t\t\tlet
\t\t\t\t    Fonte = PostgreSQL.Database("aws-1-sa-east-1.pooler.supabase.com:5432", "postgres"),
\t\t\t\t    public_metas_bruto = Fonte{[Schema="public",Item="metas_bruto"]}[Data],
\t\t\t\t    #"Valor Substituído" = Table.ReplaceValue(public_metas_bruto,".","",Replacer.ReplaceText,{"cnpj_cpf"}),
\t\t\t\t    #"Valor Substituído1" = Table.ReplaceValue(#"Valor Substituído","/","",Replacer.ReplaceText,{"cnpj_cpf"}),
\t\t\t\t    #"Valor Substituído2" = Table.ReplaceValue(#"Valor Substituído1","-","",Replacer.ReplaceText,{"cnpj_cpf"}),
\t\t\t\t    #"Coluna Tipo Origem Adicionada" = Table.AddColumn(#"Valor Substituído2", "tipo_origem", each if Text.Upper(Text.From([descricao_cat])) = "RECEITA DE CONTABILIDADE RECORRENTE" or Text.Upper(Text.From([categoria])) = "RECEITA DE CONTABILIDADE RECORRENTE" then "C" else "O", type text),
\t\t\t\t    #"Mesclado" = Table.NestedJoin(#"Coluna Tipo Origem Adicionada", {"cnpj_cpf"}, UnidadesPorCNPJ, {"cnpj_cpf"}, "Unidade", JoinKind.LeftOuter),
\t\t\t\t    #"Expandido" = Table.ExpandTableColumn(#"Mesclado", "Unidade", {"unidade_id"}, {"unidade_id"}),
\t\t\t\t    #"Valor Substituído3" = Table.ReplaceValue(#"Expandido",null,"NE",Replacer.ReplaceValue,{"unidade_id"}),
\t\t\t\t    #"Consultas Mescladas" = Table.NestedJoin(#"Valor Substituído3", {"tipo_origem", "numero_contrato"}, HonorariosPorJob, {"tipo_origem", "numero_contrato"}, "HonorariosPorJob", JoinKind.LeftOuter),
\t\t\t\t    #"HonorariosPorJob Expandido" = Table.ExpandTableColumn(#"Consultas Mescladas", "HonorariosPorJob", {"numero_contrato", "honorario"}, {"HonorariosPorJob.numero_contrato", "HonorariosPorJob.honorario"}),
\t\t\t\t    #"Coluna Removida" = Table.RemoveColumns(#"HonorariosPorJob Expandido",{"tipo_origem"})
\t\t\t\tin
\t\t\t\t    #"Coluna Removida"
\t\t\t\t```"""

import re
metas_updated = re.sub(r"\tpartition 'public metas_bruto' = m\s+mode: import\s+source =.*?```", new_metas_source, metas_content, flags=re.DOTALL)

with open(path_metas, "w", encoding="utf-8") as f:
    f.write(metas_updated)

print("public metas_bruto.tmdl updated.")

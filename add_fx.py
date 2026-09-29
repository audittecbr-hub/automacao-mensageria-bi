import uuid

file_path = r'C:\Users\cristhofer.maciel.GRUPOSTUDIO\OneDrive\repasse.SemanticModel\definition\expressions.tmdl'

new_guid = str(uuid.uuid4())

new_expr = f'''

expression fxCalcularHonorario = `
		(codigo_job as number) =>
		let
		    Resultado = Sql.Database("192.168.2.34", "STUDIO_FISCAL", 
		        [Query = "SELECT dbo.Func_JOB_CALCULAR_HONORARIO(" & Text.From(codigo_job) & ") as Honorario"]
		    )
		in
		    Resultado
		`
	lineageTag: {new_guid}

	annotation PBI_NavigationStepName = Navegação

	annotation PBI_ResultType = Function
'''

with open(file_path, 'a', encoding='utf8') as f:
    f.write(new_expr)

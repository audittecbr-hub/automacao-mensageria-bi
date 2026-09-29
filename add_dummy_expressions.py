import re

exp_path = r'C:\Users\cristhofer.maciel.GRUPOSTUDIO\Downloads\Ranking_Metas_V2.SemanticModel\definition\expressions.tmdl'
with open(exp_path, 'r', encoding='utf-8') as f:
    text = f.read()

dummy_expressions = '''

expression UnidadesPorCNPJ = ```
		let
		    Fonte = #table(type table [cnpj_limpo = text, unidade_id = text], {})
		in
		    Fonte
	```
	lineageTag: a1b2c3d4-e5f6-7890-abcd-ef1234567890

expression 'public metas_bruto' = ```
		let
		    Fonte = #table(type table [cnpj_cpf = text], {})
		in
		    Fonte
	```
	lineageTag: b2c3d4e5-f6a7-8901-bcde-f12345678901
'''

if 'expression UnidadesPorCNPJ' not in text:
    text = text.rstrip() + dummy_expressions
    with open(exp_path, 'w', encoding='utf-8') as f:
        f.write(text)
    print("Dummy expressions added to expressions.tmdl successfully!")
else:
    print("Expressions already present.")

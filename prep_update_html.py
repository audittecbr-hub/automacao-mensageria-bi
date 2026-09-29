import json
import requests

# Load original expressions
with open(r'C:\Users\cristhofer.maciel.GRUPOSTUDIO\.gemini\antigravity-ide\brain\86a55459-41f9-4a50-8a31-1a8a8f9a51d5\.system_generated\steps\2269\output.txt', 'r', encoding='utf-8') as f:
    tax_data = json.load(f)['results'][0]['data']

with open(r'C:\Users\cristhofer.maciel.GRUPOSTUDIO\.gemini\antigravity-ide\brain\86a55459-41f9-4a50-8a31-1a8a8f9a51d5\.system_generated\steps\2279\output.txt', 'r', encoding='utf-8') as f:
    other_data = json.load(f)['results']

measures_dict = {
    'HTML_Detalhamento_Metas_Tax': tax_data['expression']
}
for item in other_data:
    measures_dict[item['data']['name']] = item['data']['expression']

# 1. TAX
old_tax_block = """VAR _tabelaRaw = 
    ADDCOLUMNS(
        SUMMARIZE(
            Metas,
            Metas[bandeira],
            Metas[descricao_cat],
            Metas[razao_social],
            Metas[data_emissao],
            Calendario[Date]
        ),
        "V_Tax", [valor_Tax],
        "V_Repasse", [valor_Tax_Repasse]
    )

VAR _tabelaCalc = 
    ADDCOLUMNS(
        FILTER(_tabelaRaw, NOT ISBLANK([V_Tax]) || NOT ISBLANK([V_Repasse])),
        "Tax_Liquido", COALESCE([V_Tax], 0) - COALESCE([V_Repasse], 0)
    )"""

new_tax_block = """VAR _tabelaRaw = 
    ADDCOLUMNS(
        CALCULATETABLE(
            SUMMARIZE(
                Metas,
                Metas[bandeira],
                Metas[descricao_cat],
                Metas[razao_social],
                Metas[data_emissao],
                Calendario[Date]
            ),
            Metas[categoria] = "TAX"
        ),
        "V_Tax", [valor_Tax],
        "V_Repasse", [valor_Tax_Repasse]
    )

VAR _tabelaCalc = 
    ADDCOLUMNS(
        FILTER(_tabelaRaw, COALESCE([V_Tax], 0) > 0),
        "Tax_Liquido", COALESCE([V_Tax], 0) - COALESCE([V_Repasse], 0)
    )"""

# 2. Corporate
old_corp_block = """VAR _tabelaRaw = 
    ADDCOLUMNS(
        SUMMARIZE(
            Metas,
            Metas[bandeira],
            Metas[descricao_cat],
            Metas[razao_social],
            Metas[data_emissao],
            Calendario[Date]
        ),
        "V_Total", [Valor_Corporate],
        "V_Repasse", [Valor_Corporate_Repasse]
    )

VAR _tabelaCalc = 
    ADDCOLUMNS(
        FILTER(_tabelaRaw, NOT ISBLANK([V_Total]) || NOT ISBLANK([V_Repasse])),
        "V_Liquido", COALESCE([V_Total], 0) - COALESCE([V_Repasse], 0)
    )"""

new_corp_block = """VAR _tabelaRaw = 
    ADDCOLUMNS(
        CALCULATETABLE(
            SUMMARIZE(
                Metas,
                Metas[bandeira],
                Metas[descricao_cat],
                Metas[razao_social],
                Metas[data_emissao],
                Calendario[Date]
            ),
            Metas[categoria] = "CORPORATE"
        ),
        "V_Total", [Valor_Corporate],
        "V_Repasse", [Valor_Corporate_Repasse]
    )

VAR _tabelaCalc = 
    ADDCOLUMNS(
        FILTER(_tabelaRaw, COALESCE([V_Total], 0) > 0),
        "V_Liquido", COALESCE([V_Total], 0) - COALESCE([V_Repasse], 0)
    )"""

# 3. Tecnologia
old_tec_block = """VAR _tabelaRaw = 
    ADDCOLUMNS(
        SUMMARIZE(
            Metas,
            Metas[bandeira],
            Metas[descricao_cat],
            Metas[razao_social],
            Metas[data_emissao],
            Calendario[Date]
        ),
        "V_Total", [Valor_PJ],
        "V_Repasse", [Valor_PJ_Repasse],
        "V_Liquido", [tecnlogia_liquido]
    )

VAR _tabelaCalc = 
    FILTER(_tabelaRaw, NOT ISBLANK([V_Total]) || NOT ISBLANK([V_Repasse]) || NOT ISBLANK([V_Liquido]))"""

new_tec_block = """VAR _tabelaRaw = 
    ADDCOLUMNS(
        CALCULATETABLE(
            SUMMARIZE(
                Metas,
                Metas[bandeira],
                Metas[descricao_cat],
                Metas[razao_social],
                Metas[data_emissao],
                Calendario[Date]
            ),
            Metas[categoria] IN { "PJ 360", "PJ", "TECNOLOGIA" }
        ),
        "V_Total", [Valor_PJ],
        "V_Repasse", [Valor_PJ_Repasse],
        "V_Liquido", [tecnlogia_liquido]
    )

VAR _tabelaCalc = 
    FILTER(_tabelaRaw, COALESCE([V_Total], 0) > 0)"""

# 4. Educacao
old_educ_block = """VAR _tabelaRaw = 
    ADDCOLUMNS(
        SUMMARIZE(
            Metas,
            Metas[bandeira],
            Metas[descricao_cat],
            Metas[razao_social],
            Metas[data_emissao],
            Calendario[Date]
        ),
        "V_Total", [Valor_Educacao],
        "V_Repasse", [Valor_Educacao_Repasse]
    )

VAR _tabelaCalc = 
    ADDCOLUMNS(
        FILTER(_tabelaRaw, NOT ISBLANK([V_Total]) || NOT ISBLANK([V_Repasse])),
        "V_Liquido", COALESCE([V_Total], 0) - COALESCE([V_Repasse], 0)
    )"""

new_educ_block = """VAR _tabelaRaw = 
    ADDCOLUMNS(
        CALCULATETABLE(
            SUMMARIZE(
                Metas,
                Metas[bandeira],
                Metas[descricao_cat],
                Metas[razao_social],
                Metas[data_emissao],
                Calendario[Date]
            ),
            Metas[categoria] IN { "EDUCAÇÃO", "EDUCACAO", "EDUCAO" }
        ),
        "V_Total", [Valor_Educacao],
        "V_Repasse", [Valor_Educacao_Repasse]
    )

VAR _tabelaCalc = 
    ADDCOLUMNS(
        FILTER(_tabelaRaw, COALESCE([V_Total], 0) > 0),
        "V_Liquido", COALESCE([V_Total], 0) - COALESCE([V_Repasse], 0)
    )"""

# 5. Franchising
old_fran_block = """VAR _tabelaRaw = 
    ADDCOLUMNS(
        SUMMARIZE(
            Metas,
            Metas[bandeira],
            Metas[descricao_cat],
            Metas[razao_social],
            Metas[data_emissao],
            Calendario[Date]
        ),
        "V_Total", [Valor_Franchising],
        "V_Repasse", [Valor_Franchising_Repasse]
    )

VAR _tabelaCalc = 
    ADDCOLUMNS(
        FILTER(_tabelaRaw, NOT ISBLANK([V_Total]) || NOT ISBLANK([V_Repasse])),
        "V_Liquido", COALESCE([V_Total], 0) - COALESCE([V_Repasse], 0)
    )"""

new_fran_block = """VAR _tabelaRaw = 
    ADDCOLUMNS(
        CALCULATETABLE(
            SUMMARIZE(
                Metas,
                Metas[bandeira],
                Metas[descricao_cat],
                Metas[razao_social],
                Metas[data_emissao],
                Calendario[Date]
            ),
            Metas[categoria] = "FRANCHISING"
        ),
        "V_Total", [Valor_Franchising],
        "V_Repasse", [Valor_Franchising_Repasse]
    )

VAR _tabelaCalc = 
    ADDCOLUMNS(
        FILTER(_tabelaRaw, COALESCE([V_Total], 0) > 0),
        "V_Liquido", COALESCE([V_Total], 0) - COALESCE([V_Repasse], 0)
    )"""

# 6. Expansao
old_exp_block = """VAR _tabelaRaw = 
    ADDCOLUMNS(
        SUMMARIZE(
            Metas,
            Metas[bandeira],
            Metas[descricao_cat],
            Metas[descricao_dept],
            Metas[razao_social],
            Metas[data_emissao],
            Calendario[Date]
        ),
        "V_Total", [Valor_Expansao],
        "V_Repasse", [Valor_Expansao_Repasse]
    )

VAR _tabelaCalc = 
    ADDCOLUMNS(
        FILTER(_tabelaRaw, NOT ISBLANK([V_Total]) || NOT ISBLANK([V_Repasse])),
        "V_Liquido", COALESCE([V_Total], 0) - COALESCE([V_Repasse], 0)
    )"""

new_exp_block = """VAR _tabelaRaw = 
    ADDCOLUMNS(
        CALCULATETABLE(
            SUMMARIZE(
                Metas,
                Metas[bandeira],
                Metas[descricao_cat],
                Metas[descricao_dept],
                Metas[razao_social],
                Metas[data_emissao],
                Calendario[Date]
            ),
            Metas[categoria] = "EXPANSÃO"
        ),
        "V_Total", [Valor_Expansao],
        "V_Repasse", [Valor_Expansao_Repasse]
    )

VAR _tabelaCalc = 
    ADDCOLUMNS(
        FILTER(_tabelaRaw, COALESCE([V_Total], 0) > 0),
        "V_Liquido", COALESCE([V_Total], 0) - COALESCE([V_Repasse], 0)
    )"""

def replace_block(text, old_b, new_b, name):
    # Normalize newlines
    norm_text = text.replace('\r\n', '\n')
    norm_old = old_b.replace('\r\n', '\n')
    if norm_old in norm_text:
        print(f"Match found for {name}")
        return norm_text.replace(norm_old, new_b)
    else:
        print(f"ERROR: match NOT found for {name}")
        return norm_text

updated_measures = []

tax_expr = replace_block(measures_dict['HTML_Detalhamento_Metas_Tax'], old_tax_block, new_tax_block, 'HTML_Detalhamento_Metas_Tax')
updated_measures.append({'name': 'HTML_Detalhamento_Metas_Tax', 'tableName': 'Medidas_HTML', 'expression': tax_expr})

corp_expr = replace_block(measures_dict['HTML_Detalhamento_Metas_Corporate'], old_corp_block, new_corp_block, 'HTML_Detalhamento_Metas_Corporate')
updated_measures.append({'name': 'HTML_Detalhamento_Metas_Corporate', 'tableName': 'Medidas_HTML', 'expression': corp_expr})

tec_expr = replace_block(measures_dict['HTML_Detalhamento_Metas_Tecnologia'], old_tec_block, new_tec_block, 'HTML_Detalhamento_Metas_Tecnologia')
updated_measures.append({'name': 'HTML_Detalhamento_Metas_Tecnologia', 'tableName': 'Medidas_HTML', 'expression': tec_expr})

educ_expr = replace_block(measures_dict['HTML_Detalhamento_Metas_Educacao'], old_educ_block, new_educ_block, 'HTML_Detalhamento_Metas_Educacao')
updated_measures.append({'name': 'HTML_Detalhamento_Metas_Educacao', 'tableName': 'Medidas_HTML', 'expression': educ_expr})

fran_expr = replace_block(measures_dict['HTML_Detalhamento_Metas_Franchising'], old_fran_block, new_fran_block, 'HTML_Detalhamento_Metas_Franchising')
updated_measures.append({'name': 'HTML_Detalhamento_Metas_Franchising', 'tableName': 'Medidas_HTML', 'expression': fran_expr})

exp_expr = replace_block(measures_dict['HTML_Detalhamento_Metas_Expansao'], old_exp_block, new_exp_block, 'HTML_Detalhamento_Metas_Expansao')
updated_measures.append({'name': 'HTML_Detalhamento_Metas_Expansao', 'tableName': 'Medidas_HTML', 'expression': exp_expr})

with open('updated_html_measures.json', 'w', encoding='utf-8') as f:
    json.dump(updated_measures, f, ensure_ascii=False, indent=2)

print("Saved updated_html_measures.json")

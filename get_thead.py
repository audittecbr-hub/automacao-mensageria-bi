import re
with open(r'C:\Users\cristhofer.maciel.GRUPOSTUDIO\OneDrive\repasse.SemanticModel\definition\tables\medidas_html.tmdl', 'r', encoding='utf8') as f:
    text = f.read()

painel = text[text.find('measure Painel_Repasses = '):]
thead_start = painel.find('<thead>')
thead_end = painel.find('</thead>')
print(painel[thead_start:thead_end])

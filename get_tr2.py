import re

with open(r'C:\Users\cristhofer.maciel.GRUPOSTUDIO\OneDrive\repasse.SemanticModel\definition\tables\medidas_html.tmdl', 'r', encoding='utf8') as f:
    text = f.read()

painel = text[text.find('measure Painel_Repasses = '):]
tr_start = painel.find('html+=\'<tr')
tr_end = painel.find('html+=\'</tr>\';', tr_start)

# Let's save the snippet to a file so we don't have unicode console errors
with open('snippet.txt', 'w', encoding='utf8') as f:
    f.write(painel[tr_start:tr_end+14])

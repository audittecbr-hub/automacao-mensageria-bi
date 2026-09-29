import re

with open(r'C:\Users\cristhofer.maciel.GRUPOSTUDIO\OneDrive\repasse.SemanticModel\definition\tables\medidas_html.tmdl', 'r', encoding='utf8') as f:
    text = f.read()

painel_start = text.find('measure Painel_Repasses = ')
# find the next measure to know where Painel_Repasses ends
# if it's the last measure, just take till the end of the file
next_measure = text.find('measure ', painel_start + 10)
if next_measure == -1:
    painel_text = text[painel_start:]
else:
    painel_text = text[painel_start:next_measure]

with open('painel_full.txt', 'w', encoding='utf8') as f:
    f.write(painel_text)

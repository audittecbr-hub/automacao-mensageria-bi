import re

file_path = r'C:\Users\cristhofer.maciel.GRUPOSTUDIO\Desktop\HTML_Detalhamento_Aprovados_Corrigido.dax'
with open(file_path, 'r', encoding='utf8') as f:
    dax = f.read()

# Fix the escape character used for double quotes in DAX
# Replace \" with ""
dax = dax.replace('\\"', '""')

with open(file_path, 'w', encoding='utf8') as f:
    f.write(dax)

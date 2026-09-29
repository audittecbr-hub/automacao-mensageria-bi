import re

file_path = r'C:\Users\cristhofer.maciel.GRUPOSTUDIO\Desktop\HTML_Detalhamento_Aprovados_Corrigido.dax'
with open(file_path, 'r', encoding='utf8') as f:
    dax = f.read()

# Fix the double quotes that I accidentally injected
dax = dax.replace('""<th><span>Data_RT</span><br>"', '"<th><span>Data_RT</span><br>"')
dax = dax.replace('</div></th>"" &', '</div></th>" &')
dax = dax.replace('""<th><span>Data_Mov</span><br>"', '"<th><span>Data_Mov</span><br>"')

with open(file_path, 'w', encoding='utf8') as f:
    f.write(dax)

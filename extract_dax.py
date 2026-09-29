import re
with open('painel_full.txt', 'r', encoding='utf8') as f:
    text = f.read()
start_idx = text.find('measure Painel_Repasses = `') + len('measure Painel_Repasses = `')
end_idx = text.rfind('`')
dax_code = text[start_idx:end_idx].strip()
with open('Painel_Repasses_Codigo.txt', 'w', encoding='utf8') as f:
    f.write(dax_code)

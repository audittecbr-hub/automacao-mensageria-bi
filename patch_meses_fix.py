import re

file_path = r'C:\Users\cristhofer.maciel.GRUPOSTUDIO\Desktop\Mockup_Honorarios_Matriz_Corrigido.dax'
with open(file_path, 'r', encoding='utf8') as f:
    dax = f.read()

# 1. Update _datas_meses to filter dates >= 2026-06-01 AND <= 2026-12-31
old_filter = 'FILTER(Calendario, Calendario[Date] >= DATE(2026, 6, 1))'
new_filter = 'FILTER(Calendario, Calendario[Date] >= DATE(2026, 6, 1) && Calendario[Date] <= DATE(2026, 12, 31))'

if old_filter in dax:
    dax = dax.replace(old_filter, new_filter)

# 2. Update CONCATENATEX to sort by [AnoMes] ASC
old_concat = 'DESC'
# Be careful replacing DESC, only the one in _opcoes_meses
# Let's find _opcoes_meses block
match = re.search(r'VAR _opcoes_meses =.*?CONCATENATEX\([^,]+,[^,]+,[^,]+,\s*\[AnoMes\],\s*DESC\s*\)', dax, flags=re.DOTALL)
if match:
    block = match.group(0)
    new_block = block.replace('DESC', 'ASC')
    dax = dax.replace(block, new_block)

# 3. Add max-height and overflow to the dropdown list
old_dropdown_list = '"<div class=\'dropdown-list\' style=\'padding:10px;\'>" &'
new_dropdown_list = '"<div class=\'dropdown-list\' style=\'padding:10px; max-height: 250px; overflow-y: auto;\'>" &'

if old_dropdown_list in dax:
    dax = dax.replace(old_dropdown_list, new_dropdown_list)

with open(file_path, 'w', encoding='utf8') as f:
    f.write(dax)

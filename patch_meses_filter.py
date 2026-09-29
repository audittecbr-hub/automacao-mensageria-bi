import re

file_path = r'C:\Users\cristhofer.maciel.GRUPOSTUDIO\Desktop\Mockup_Honorarios_Matriz_Corrigido.dax'
with open(file_path, 'r', encoding='utf8') as f:
    dax = f.read()

# 1. Update _datas_meses to filter dates >= DATE(2026, 6, 1)
old_datas_meses = 'VAR _datas_meses = DISTINCT(SELECTCOLUMNS(Calendario, "AnoMes", FORMAT(Calendario[Date], "yyyy-MM")))'
new_datas_meses = 'VAR _datas_meses = DISTINCT(SELECTCOLUMNS(FILTER(Calendario, Calendario[Date] >= DATE(2026, 6, 1)), "AnoMes", FORMAT(Calendario[Date], "yyyy-MM")))'

if old_datas_meses in dax:
    dax = dax.replace(old_datas_meses, new_datas_meses)
else:
    # Use regex in case spacing is different
    dax = re.sub(
        r'VAR _datas_meses = DISTINCT\(SELECTCOLUMNS\(Calendario,\s*"AnoMes",\s*FORMAT\(Calendario\[Date\],\s*"yyyy-MM"\)\)\)',
        new_datas_meses,
        dax
    )

# 2. Update CONCATENATEX to sort by [AnoMes] DESC
old_concat = '''VAR _opcoes_meses = 
    CONCATENATEX(
        _datas_meses, 
        "<label class='dropdown-item' style='display:flex; align-items:center; gap:8px; cursor:pointer;'><input type='checkbox' class='mes-checkbox' value='" & [AnoMes] & "' onchange='atualizarMesBtnText(); filtrarTudo();' checked> " & [AnoMes] & "</label>", 
        ""
    )'''

new_concat = '''VAR _opcoes_meses = 
    CONCATENATEX(
        _datas_meses, 
        "<label class='dropdown-item' style='display:flex; align-items:center; gap:8px; cursor:pointer;'><input type='checkbox' class='mes-checkbox' value='" & [AnoMes] & "' onchange='atualizarMesBtnText(); filtrarTudo();' checked> " & [AnoMes] & "</label>", 
        "",
        [AnoMes], DESC
    )'''

if old_concat in dax:
    dax = dax.replace(old_concat, new_concat)

with open(file_path, 'w', encoding='utf8') as f:
    f.write(dax)

with open('HTML_Detalhamento_Aprovados.dax', 'r', encoding='utf8') as f:
    dax = f.read()

# 1. Update DAX filter and tr attributes
dax = dax.replace(
    'FILTER(vw_powerbi_relatorio_aprovacao, [Honorários aprovados] > 0),',
    'FILTER(vw_powerbi_relatorio_aprovacao, [Honorários aprovados] > 0 && vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026, 6, 12)),'
)

dax = dax.replace(
    '\"<tr class=\'linha-detalhe\' data-rt=\'\" & FORMAT(vw_powerbi_relatorio_aprovacao[DATA_RT], \"yyyy-MM-dd\") & \"\'>\" &',
    '\"<tr class=\'linha-detalhe\' data-rt=\'\" & FORMAT(vw_powerbi_relatorio_aprovacao[DATA_RT], \"yyyy-MM-dd\") & \"\' data-mov=\'\" & FORMAT(vw_powerbi_relatorio_aprovacao[data_mov_anterior], \"yyyy-MM-dd\") & \"\'>\" &'
)

# 2. Update JS filtering logic
import re

# Remove the complex date parsing logic
dax = re.sub(
    r'var dataInicial = null;.*?var dF_trunc = new Date\(dataFinal\.getFullYear\(\), dataFinal\.getMonth\(\), dataFinal\.getDate\(\)\);\s*\}',
    '',
    dax,
    flags=re.DOTALL
)

# Replace the inner loop logic for dates
inner_loop_old = r'var dtRtStr = rows\[i\]\.getAttribute\(\'data-rt\'\);.*?if \(qD !== \'\'\) \{\s*matchD = false;\s*\}'
inner_loop_new = '''var dtRtStr = rows[i].getAttribute('data-rt');
        var dtMovStr = rows[i].getAttribute('data-mov');
        var matchD = (qD === '' || dtRtStr === qD);
        var matchDM = (qDM === '' || dtMovStr === qDM);'''
dax = re.sub(inner_loop_old, inner_loop_new, dax, flags=re.DOTALL)

# Remove the old DM from matchG and instead just use matchDM properly (which we do)
# Wait, let's keep matchG as is, but we need to ensure matchDM is checked. The original had matchDM logic.
# Original: var matchDM=(qDM==='' || tDM.indexOf(qDM)>-1);
# We will replace that line:
dax = dax.replace(
    'var matchDM=(qDM===\'\' || tDM.indexOf(qDM)>-1);',
    '' # We already defined matchDM above
)

# 3. Update the HTML inputs
# <th><span>Data_RT</span><br><input type='month' id='buscaColData' class='col-filter' onchange='filtrarTabela()' value='" & _mesAtual & "'></th>
# <th><span>Data</span><br><input type='text' id='buscaColDataMov' class='col-filter' placeholder='Filtrar Data...' onkeyup='filtrarTabela()'></th>
html_rt_old = '<th><span>Data_RT</span><br><input type=\'month\' id=\'buscaColData\' class=\'col-filter\' onchange=\'filtrarTabela()\' value=\'\" & _mesAtual & \"\'></th>'
html_rt_new = '<th><span>Data_RT</span><br><input type=\'date\' id=\'buscaColData\' class=\'col-filter\' onchange=\'filtrarTabela()\'></th>'
dax = dax.replace(html_rt_old, html_rt_new)

html_dm_old = '<th><span>Data</span><br><input type=\'text\' id=\'buscaColDataMov\' class=\'col-filter\' placeholder=\'Filtrar Data...\' onkeyup=\'filtrarTabela()\'></th>'
html_dm_new = '<th><span>Data_Mov</span><br><input type=\'date\' id=\'buscaColDataMov\' class=\'col-filter\' onchange=\'filtrarTabela()\'></th>'
dax = dax.replace(html_dm_old, html_dm_new)

with open('HTML_Detalhamento_Aprovados.dax', 'w', encoding='utf8') as f:
    f.write(dax)


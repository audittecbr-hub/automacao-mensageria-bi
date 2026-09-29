import re

with open('painel_full.txt', 'r', encoding='utf8') as f:
    text = f.read()

# Edit 1: Add percHonorario to vJsonRows
old_json = '''			            ",nomeUnidade:'" & SUBSTITUTE(SUBSTITUTE(COALESCE([NOME_UNIDADE_VAL], ""), "'", " "), """", " ") & "'" &
			            ",status:'Pendente'" &'''
new_json = '''			            ",nomeUnidade:'" & SUBSTITUTE(SUBSTITUTE(COALESCE([NOME_UNIDADE_VAL], ""), "'", " "), """", " ") & "'" &
			            ",percHonorario:" & SUBSTITUTE(FORMAT(COALESCE([HonorariosPorJob.honorario], 0), "0.00"), ",", ".") &
			            ",status:'Pendente'" &'''
text = text.replace(old_json, new_json)

# Edit 2: Add tds to renderTable
old_tds = '''			        html+='<td class=""num"" style=""color:var(--text-main);font-weight:600"">'+(r.dataPagamento||'-')+'</td>';
			        html+='<td><span class=""unidade-code"">'+(r.unidade||'')+'</span></td>';
			        html+='<td style=""color:var(--text-main);font-size:11px"">'+(r.nomeUnidade||'')+'</td>';
			        html+='<td class=""num""><div class=""status-btn-group"">';'''
new_tds = '''			        html+='<td class=""num"" style=""color:var(--text-main);font-weight:600"">'+(r.dataPagamento||'-')+'</td>';
			        html+='<td><span class=""unidade-code"">'+(r.unidade||'')+'</span></td>';
			        html+='<td style=""color:var(--text-main);font-size:11px"">'+(r.nomeUnidade||'')+'</td>';
			        html+='<td class=""num"" style=""color:var(--text-main)"">'+(pU ? String(pU).replace('.', ',')+'%' : '-')+'</td>';
			        html+='<td class=""num"" style=""color:var(--text-main);font-weight:600;"">'+(pH ? String(pH).replace('.', ',')+'%' : '0,00%')+'</td>';
			        html+='<td class=""num"" style=""color:var(--text-main)"">'+(r.valorUnit ? fmtBRL(r.valorUnit) : '-')+'</td>';
			        html+='<td class=""num""><div class=""status-btn-group"">';'''
text = text.replace(old_tds, new_tds)

with open('painel_full.txt', 'w', encoding='utf8') as f:
    f.write(text)

import re

with open('Painel_Repasses_Codigo.txt', 'r', encoding='utf8') as f:
    text = f.read()

# Update 1: Add sumUnit in loop
old_loop = '''			        var pH = r.percHonorario;
			        sumVal+=r.valor;'''
new_loop = '''			        var pH = r.percHonorario;
			        sumVal+=r.valor;
			        if(r.valorUnit) sumUnit+=r.valorUnit;'''
text = text.replace(old_loop, new_loop)

# Update 2: Fix tfoot
old_foot = '''			    var foot='<tr>';
			    foot+='<td colspan=""5"">TOTAL</td>';
			    foot+='<td class=""valor num"">'+fmtBRL(sumVal)+'</td>';
			    foot+='<td colspan=""4""></td>';
			    foot+='</tr>';'''
new_foot = '''			    var foot='<tr>';
			    foot+='<td colspan=""5"">TOTAL</td>';
			    foot+='<td class=""valor num"">'+fmtBRL(sumVal)+'</td>';
			    foot+='<td colspan=""5""></td>';
			    foot+='<td class=""valor num"">'+fmtBRL(sumUnit)+'</td>';
			    foot+='<td></td>';
			    foot+='</tr>';'''
text = text.replace(old_foot, new_foot)

with open('Painel_Repasses_Codigo.txt', 'w', encoding='utf8') as f:
    f.write(text)

with open(r'C:\Users\cristhofer.maciel.GRUPOSTUDIO\.gemini\antigravity-ide\brain\295cbf89-2513-4d5c-86a1-fc95a552fa3c\Painel_Repasses_Codigo.md', 'w', encoding='utf8') as f:
    f.write('`dax\n' + text + '\n`')

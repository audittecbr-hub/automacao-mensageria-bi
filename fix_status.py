import re

with open('Painel_Repasses_Codigo.txt', 'r', encoding='utf8') as f:
    text = f.read()

# Fix 1: Use filter instead of find to update ALL rows with that ID
old_set_status = '''			    var item = rawData.find(function(r){return r.id===id;});
			    if(item) {
			        item.status = newStatus;
			        hasUnsaved = true;'''
new_set_status = '''			    var items = rawData.filter(function(r){return r.id===id;});
			    if(items.length > 0) {
			        items.forEach(function(item) { item.status = newStatus; });
			        hasUnsaved = true;'''
text = text.replace(old_set_status, new_set_status)

# Fix 2: Since we update all rows with the ID, gravarAPI will save Aprovado for that ID
# Also, to be absolutely safe, let's make the ID a unique composite key again if the user allows it.
# But wait, the user SAID "valida de novo o cmapo de chave unica p usar é o codigo_lancamento_omie".
# If they specifically asked to use codigo_lancamento_omie as the unique key, it implies they WANT all rows with the same codigo_lancamento_omie to share the same status!
# So changing ind to ilter and updating all of them is exactly the right behavior!

with open('Painel_Repasses_Codigo.txt', 'w', encoding='utf8') as f:
    f.write(text)

with open(r'C:\Users\cristhofer.maciel.GRUPOSTUDIO\.gemini\antigravity-ide\brain\295cbf89-2513-4d5c-86a1-fc95a552fa3c\Painel_Repasses_Codigo.md', 'w', encoding='utf8') as f:
    f.write('`dax\n' + text + '\n`')

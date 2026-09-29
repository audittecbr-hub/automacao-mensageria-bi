import re
with open('Painel_Repasses_Codigo.txt', 'r', encoding='utf8') as f:
    text = f.read()

with open(r'C:\Users\cristhofer.maciel.GRUPOSTUDIO\.gemini\antigravity-ide\brain\295cbf89-2513-4d5c-86a1-fc95a552fa3c\Painel_Repasses_Codigo.md', 'w', encoding='utf8') as f:
    f.write('`dax\n' + text + '\n`')

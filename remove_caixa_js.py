import re

filepath = r"C:\Users\cristhofer.maciel.GRUPOSTUDIO\Downloads\honorarios_regionais (2).SemanticModel\definition\tables\medidas_html.tmdl"

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Lines to remove
lines_to_remove = [
    "\"document.getElementById('cx-sul').innerText = formatarMoeda(sCx['Regional Sul']);\" &",
    "\"document.getElementById('cx-sp').innerText = formatarMoeda(sCx['Regional Sudeste']);\" &",
    "\"document.getElementById('cx-sd').innerText = formatarMoeda(sCx['Regional Sudeste 2']);\" &",
    "\"document.getElementById('cx-nn').innerText = formatarMoeda(sCx['Regional NNCO']);\" &",
    "\"document.getElementById('cx-total').innerText = formatarMoeda(sCx['Total']);\" &",
    "\"document.getElementById('card-caixa').innerText = formatarMilhoes(sCx['Total']);\" &"
]

for line in lines_to_remove:
    content = content.replace(line + "\n", "")
    content = content.replace(line + "\r\n", "")
    content = content.replace(line, "")

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print("Removed JS lines for Caixa")

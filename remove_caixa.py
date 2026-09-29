import re

filepath = r"C:\Users\cristhofer.maciel.GRUPOSTUDIO\Downloads\honorarios_regionais (2).SemanticModel\definition\tables\medidas_html.tmdl"

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Remove _linha4 from the table
content = content.replace(
    "_linha_nao_aprovados & _linha3 & _linha3_nao_aprovados & _linha4 & _linha5 &",
    "_linha_nao_aprovados & _linha3 & _linha3_nao_aprovados & _linha5 &"
)

# Remove the card for Caixa
kpi_caixa_regex = r"\s*\"<div class='card' style='border-color:var\(--accent\); background:rgba\(226,179,90,0\.05\);'>\" &\s*\"<div class='card-title' style='color:var\(--accent\);'>&#128176; Honorários Recebidos \(Caixa\)</div>\" &\s*\"<div class='card-value' id='card-caixa' style='color:var\(--accent\);'>R\$ 0,00</div>\" &\s*\"<div><span class='card-indicator ind-up'>&#8593; 15%</span> <span style='font-size:11px;color:var\(--text-muted\);'>vs mês ant\.</span></div>\" &\s*\"</div>\" &"
content = re.sub(kpi_caixa_regex, "", content)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print("Removed Caixa row and KPI")

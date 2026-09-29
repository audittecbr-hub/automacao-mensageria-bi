import re

filepath = r"C:\Users\cristhofer.maciel.GRUPOSTUDIO\Downloads\honorarios_regionais (2).SemanticModel\definition\tables\medidas_html.tmdl"

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Add toggle button to HTML header (in _html)
header_button = "\"<label class='dropdown-btn' style='cursor:pointer; user-select:none; width:auto; border-color:var(--orange); color:var(--orange); margin-right: 12px;'><input type='checkbox' id='chkRegraRt' onchange='filtrarTudo();' style='margin-right:8px;' checked> REGRA RT 12/06</label>\" &"
content = content.replace(
    "\"<div class='dropdown-container'>\" &\n\t\t\t                    \"<button class='dropdown-btn' onclick='toggleProdDropdown()'><span id='prodBtnText'>TODOS PRODUTOS</span>",
    header_button + "\n\t\t\t                " + "\"<div class='dropdown-container'>\" &\n\t\t\t                    \"<button class='dropdown-btn' onclick='toggleProdDropdown()'><span id='prodBtnText'>TODOS PRODUTOS</span>"
)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print("Injected HTML button correctly")

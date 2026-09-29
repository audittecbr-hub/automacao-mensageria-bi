import re

filepath = r"C:\Users\cristhofer.maciel.GRUPOSTUDIO\Downloads\honorarios_regionais (2).SemanticModel\definition\tables\medidas_html.tmdl"

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update Header CSS
content = content.replace(
    ".title { font-size: 40px; font-weight: 300; color: var(--text-main); letter-spacing: 2px; text-transform: uppercase; display: flex; align-items: center; gap: 16px; }",
    ".title { font-size: 28px; font-weight: 300; color: var(--text-main); letter-spacing: 1px; text-transform: uppercase; display: flex; align-items: center; gap: 12px; white-space: nowrap; }"
)
content = content.replace(
    ".subtitle { font-size: 20px; color: var(--text-sec); letter-spacing: 1px; font-weight: 500; text-transform: uppercase; margin-left: 20px; }",
    ".subtitle { font-size: 16px; color: var(--text-sec); letter-spacing: 1px; font-weight: 500; text-transform: uppercase; margin-left: 16px; }"
)
content = content.replace(
    ".header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 150px; position: relative; z-index: 99999; }",
    ".header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 60px; position: relative; z-index: 99999; gap: 20px; padding-bottom: 10px; }"
)


# 2. Replace the HTML for the Regra RT toggle with a Dropdown
old_html_btn = "\"<label class='dropdown-btn' style='cursor:pointer; user-select:none; width:auto; border-color:var(--orange); color:var(--orange); margin-right: 12px;'><input type='checkbox' id='chkRegraRt' onchange='filtrarTudo();' style='margin-right:8px;' checked> REGRA RT 12/06</label>\" &"

new_html_btn = """			                "<div class='dropdown-container' style='margin-right: 12px;'>" &
			                    "<button class='dropdown-btn' onclick='toggleRtDropdown()' style='border-color:var(--orange); color:var(--orange); width:230px;'><span id='rtBtnText'>REGRA RT: HABILITADA</span> <span style='font-size:16px; margin-left:auto;'>&#9660;</span></button>" &
			                    "<div class='dropdown-menu' id='rtMenu' style='width:230px;'>" &
			                        "<div class='dropdown-list'>" &
			                            "<div class='dropdown-item selected' onclick=""selecionarRt(this, true)"">REGRA RT: HABILITADA</div>" &
			                            "<div class='dropdown-item' onclick=""selecionarRt(this, false)"">REGRA RT: DESABILITADA</div>" &
			                        "</div>" &
			                    "</div>" &
			                    "<input type='checkbox' id='chkRegraRt' style='display:none;' checked onchange='filtrarTudo();'>" &
			                "</div>" &"""

content = content.replace(old_html_btn, new_html_btn)


# 3. Add Javascript for the new dropdown
js_to_add = """			    "function toggleRtDropdown() { document.getElementById('rtMenu').classList.toggle('show'); }" &
			    "function selecionarRt(el, habilitada) {" &
			        "var cb = document.getElementById('chkRegraRt');" &
			        "cb.checked = habilitada;" &
			        "document.getElementById('rtBtnText').innerText = habilitada ? 'REGRA RT: HABILITADA' : 'REGRA RT: DESABILITADA';" &
			        "var items = el.parentNode.querySelectorAll('.dropdown-item');" &
			        "for(var i=0; i<items.length; i++) { items[i].classList.remove('selected'); }" &
			        "el.classList.add('selected');" &
			        "document.getElementById('rtMenu').classList.remove('show');" &
			        "filtrarTudo();" &
			    "}" &"""

content = content.replace(
    "\"function toggleProdDropdown() { document.getElementById('prodMenu').classList.toggle('show'); }\" &",
    js_to_add + "\n\t\t\t    " + "\"function toggleProdDropdown() { document.getElementById('prodMenu').classList.toggle('show'); }\" &"
)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated CSS and Regra RT Layout")

import re

filepath = r"C:\Users\cristhofer.maciel.GRUPOSTUDIO\Downloads\honorarios_regionais (2).SemanticModel\definition\tables\medidas_html.tmdl"

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update Header margin-bottom
content = content.replace(
    ".header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 60px; position: relative; z-index: 99999; gap: 20px; padding-bottom: 10px; }",
    ".header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 150px; position: relative; z-index: 99999; gap: 20px; padding-bottom: 10px; }"
)


# 2. Replace the Dropdown HTML with Toggle Switch
old_html_btn = """			                			                "<div class='dropdown-container' style='margin-right: 12px;'>" &
			                    "<button class='dropdown-btn' onclick='toggleRtDropdown()' style='border-color:var(--orange); color:var(--orange); width:230px;'><span id='rtBtnText'>REGRA RT: HABILITADA</span> <span style='font-size:16px; margin-left:auto;'>&#9660;</span></button>" &
			                    "<div class='dropdown-menu' id='rtMenu' style='width:230px;'>" &
			                        "<div class='dropdown-list'>" &
			                            "<div class='dropdown-item selected' onclick=\\"selecionarRt(this, true)\\">REGRA RT: HABILITADA</div>" &
			                            "<div class='dropdown-item' onclick=\\"selecionarRt(this, false)\\">REGRA RT: DESABILITADA</div>" &
			                        "</div>" &
			                    "</div>" &
			                    "<input type='checkbox' id='chkRegraRt' style='display:none;' checked onchange='filtrarTudo();'>" &
			                "</div>" &"""

new_html_btn = """			                "<label class='switch-rt' style='display:flex; align-items:center; gap:10px; cursor:pointer; color:var(--orange); font-weight:700; font-size:14px; user-select:none; margin-right: 12px; letter-spacing:0.5px;'>REGRA RT 12/06" &
			                    "<div style='position:relative; width:44px; height:24px; border-radius:24px; border:2px solid var(--orange); display:flex; align-items:center;'>" &
			                        "<input type='checkbox' id='chkRegraRt' onchange='toggleSlider(this); filtrarTudo();' style='opacity:0; width:0; height:0; position:absolute;' checked>" &
			                        "<span id='sliderThumb' style='position:absolute; width:16px; height:16px; left:2px; background-color:#fff; border-radius:50%; transition:transform 0.3s, background-color 0.3s; transform:translateX(20px); box-shadow: 0 0 5px rgba(255,165,0,0.5);'></span>" &
			                    "</div>" &
			                "</label>" &"""

content = content.replace(old_html_btn, new_html_btn)


# 3. Replace the Dropdown JS with Toggle JS
old_js = """			    "function toggleRtDropdown() { document.getElementById('rtMenu').classList.toggle('show'); }" &
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

new_js = """			    "function toggleSlider(cb) {" &
			        "var thumb = document.getElementById('sliderThumb');" &
			        "if(cb.checked) { thumb.style.transform = 'translateX(20px)'; thumb.style.backgroundColor = '#fff'; }" &
			        "else { thumb.style.transform = 'translateX(0px)'; thumb.style.backgroundColor = 'var(--orange)'; }" &
			    "}" &"""

content = content.replace(old_js, new_js)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated CSS margin and added Toggle Switch layout")

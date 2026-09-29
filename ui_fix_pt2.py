import re

filepath = r"C:\Users\cristhofer.maciel.GRUPOSTUDIO\Downloads\honorarios_regionais (2).SemanticModel\definition\tables\medidas_html.tmdl"

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update Header margin-bottom
content = content.replace(
    ".header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 60px; position: relative; z-index: 99999; gap: 20px; padding-bottom: 10px; }",
    ".header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 150px; position: relative; z-index: 99999; gap: 20px; padding-bottom: 10px; }"
)

# 2. Add KPI Button CSS
kpi_btn_css = """			.btn-kpi-detalhar { position: absolute; bottom: 12px; right: 12px; background: transparent; border: 1px solid var(--border); color: var(--text-sec); font-size: 10px; font-weight: 600; padding: 4px 8px; border-radius: 4px; cursor: pointer; text-transform: uppercase; transition: 0.2s; font-family: var(--font); }
			.btn-kpi-detalhar:hover { background: var(--accent); color: #000; border-color: var(--accent); }\n"""

if ".btn-kpi-detalhar" not in content:
    content = content.replace(
        ".card-indicator { font-size: 15px; font-weight: 600; padding: 4px 8px; border-radius: 6px; display: inline-flex; align-items: center; gap: 4px; }\n",
        ".card-indicator { font-size: 15px; font-weight: 600; padding: 4px 8px; border-radius: 6px; display: inline-flex; align-items: center; gap: 4px; }\n" + kpi_btn_css
    )

# 3. Add KPI buttons to all 5 cards in HTML_Principal (the string looks like: "<div><span class='card-indicator ind-down'>&#8595; 0%</span> <span style='font-size:11px;color:var(--text-muted);'>vs mês ant.</span></div>" & )
def add_detalhar_btn(match):
    return match.group(1) + "\n\t\t\t                \"<button class='btn-kpi-detalhar'>DETALHAR</button>\" &\n\t\t\t            \"</div>\" &"

content = re.sub(
    r"(\"<div><span class='card-indicator[^>]*>[^<]*</span> <span[^>]*>[^<]*</span></div>\" &)\n\s*\"</div>\" &",
    add_detalhar_btn,
    content
)


# 4. Replace the Dropdown HTML with Toggle Switch
old_html_btn = re.compile(
    r"\"<div class='dropdown-container' style='margin-right: 12px;'>\" &\n"
    r"\s*\"<button class='dropdown-btn' onclick='toggleRtDropdown\(\)' style='border-color:var\(--orange\); color:var\(--orange\); width:230px;'><span id='rtBtnText'>REGRA RT: HABILITADA</span> <span style='font-size:16px; margin-left:auto;'>&#9660;</span></button>\" &\n"
    r"\s*\"<div class='dropdown-menu' id='rtMenu' style='width:230px;'>\" &\n"
    r"\s*\"<div class='dropdown-list'>\" &\n"
    r"\s*\"<div class='dropdown-item selected' onclick=\"\"selecionarRt\(this, true\)\"\">REGRA RT: HABILITADA</div>\" &\n"
    r"\s*\"<div class='dropdown-item' onclick=\"\"selecionarRt\(this, false\)\"\">REGRA RT: DESABILITADA</div>\" &\n"
    r"\s*\"</div>\" &\n"
    r"\s*\"</div>\" &\n"
    r"\s*\"<input type='checkbox' id='chkRegraRt' style='display:none;' checked onchange='filtrarTudo\(\);'>\" &\n"
    r"\s*\"</div>\" &"
)

new_html_btn = """\"<label class='switch-rt' style='display:flex; align-items:center; gap:10px; cursor:pointer; color:var(--orange); font-weight:700; font-size:14px; user-select:none; margin-right: 12px; letter-spacing:0.5px;'>REGRA RT 12/06\" &
			                    \"<div style='position:relative; width:44px; height:24px; border-radius:24px; border:2px solid var(--orange); display:flex; align-items:center;'>\" &
			                        \"<input type='checkbox' id='chkRegraRt' onchange='toggleSlider(this); filtrarTudo();' style='opacity:0; width:0; height:0; position:absolute;' checked>\" &
			                        \"<span id='sliderBg' style='position:absolute; top:0; left:0; right:0; bottom:0; border-radius:24px; background-color:var(--orange); transition:0.3s;'></span>\" &
			                        \"<span id='sliderThumb' style='position:absolute; width:16px; height:16px; left:2px; background-color:#fff; border-radius:50%; transition:transform 0.3s, background-color 0.3s; transform:translateX(20px); box-shadow: 0 0 5px rgba(255,165,0,0.5);'></span>\" &
			                    \"</div>\" &
			                \"</label>\" &"""

content = old_html_btn.sub(new_html_btn, content)


# 5. Replace the Dropdown JS with Toggle JS
old_js = re.compile(
    r"\"function toggleRtDropdown\(\) \{ document\.getElementById\('rtMenu'\)\.classList\.toggle\('show'\); \}\" &\n"
    r"\s*\"function selecionarRt\(el, habilitada\) \{\" &\n"
    r"\s*\"var cb = document\.getElementById\('chkRegraRt'\);\" &\n"
    r"\s*\"cb\.checked = habilitada;\" &\n"
    r"\s*\"document\.getElementById\('rtBtnText'\)\.innerText = habilitada \? 'REGRA RT: HABILITADA' : 'REGRA RT: DESABILITADA';\" &\n"
    r"\s*\"var items = el\.parentNode\.querySelectorAll\('\.dropdown-item'\);\" &\n"
    r"\s*\"for\(var i=0; i<items\.length; i\+\+\) \{ items\[i\]\.classList\.remove\('selected'\); \}\" &\n"
    r"\s*\"el\.classList\.add\('selected'\);\" &\n"
    r"\s*\"document\.getElementById\('rtMenu'\)\.classList\.remove\('show'\);\" &\n"
    r"\s*\"filtrarTudo\(\);\" &\n"
    r"\s*\"\}\" &"
)

new_js = """\"function toggleSlider(cb) {\" &
			        \"var thumb = document.getElementById('sliderThumb');\" &
			        \"var bg = document.getElementById('sliderBg');\" &
			        \"if(cb.checked) { thumb.style.transform = 'translateX(20px)'; thumb.style.backgroundColor = '#fff'; bg.style.backgroundColor = 'var(--orange)'; }\" &
			        \"else { thumb.style.transform = 'translateX(0px)'; thumb.style.backgroundColor = 'var(--orange)'; bg.style.backgroundColor = 'transparent'; }\" &
			    \"}\" &"""

content = old_js.sub(new_js, content)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated successfully")

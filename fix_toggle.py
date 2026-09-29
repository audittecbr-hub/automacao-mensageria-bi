import re

filepath = r"C:\Users\cristhofer.maciel.GRUPOSTUDIO\Downloads\honorarios_regionais (2).SemanticModel\definition\tables\medidas_html.tmdl"

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Replace the HTML for the Toggle
old_html = """\"<label class='switch-rt' style='display:flex; align-items:center; gap:10px; cursor:pointer; color:var(--orange); font-weight:700; font-size:14px; user-select:none; margin-right: 12px; letter-spacing:0.5px;'>REGRA RT 12/06\" &
			                    \"<div style='position:relative; width:44px; height:24px; border-radius:24px; border:2px solid var(--orange); display:flex; align-items:center;'>\" &
			                        \"<input type='checkbox' id='chkRegraRt' onchange='toggleSlider(this); filtrarTudo();' style='opacity:0; width:0; height:0; position:absolute;' checked>\" &
			                        \"<span id='sliderBg' style='position:absolute; top:0; left:0; right:0; bottom:0; border-radius:24px; background-color:var(--orange); transition:0.3s;'></span>\" &
			                        \"<span id='sliderThumb' style='position:absolute; width:16px; height:16px; left:2px; background-color:#fff; border-radius:50%; transition:transform 0.3s, background-color 0.3s; transform:translateX(20px); box-shadow: 0 0 5px rgba(255,165,0,0.5);'></span>\" &
			                    \"</div>\" &
			                \"</label>\" &"""

new_html = """\"<div class='switch-rt' onclick='clickToggleRT()' style='display:flex; align-items:center; gap:10px; cursor:pointer; color:var(--orange); font-weight:700; font-size:14px; user-select:none; margin-right: 12px; letter-spacing:0.5px;'>REGRA RT 12/06\" &
			                    \"<div style='position:relative; width:44px; height:24px; border-radius:24px; border:2px solid var(--orange); display:flex; align-items:center; pointer-events:none;'>\" &
			                        \"<span id='sliderBg' style='position:absolute; top:0; left:0; right:0; bottom:0; border-radius:24px; background-color:var(--orange); transition:0.3s;'></span>\" &
			                        \"<span id='sliderThumb' style='position:absolute; width:16px; height:16px; left:2px; background-color:#fff; border-radius:50%; transition:transform 0.3s, background-color 0.3s; transform:translateX(20px); box-shadow: 0 0 5px rgba(255,165,0,0.5);'></span>\" &
			                    \"</div>\" &
			                \"</div>\" &"""

content = content.replace(old_html, new_html)

# 2. Replace the JS function
old_js = """\"function toggleSlider(cb) {\" &
			        \"var thumb = document.getElementById('sliderThumb');\" &
			        \"var bg = document.getElementById('sliderBg');\" &
			        \"if(cb.checked) { thumb.style.transform = 'translateX(20px)'; thumb.style.backgroundColor = '#fff'; bg.style.backgroundColor = 'var(--orange)'; }\" &
			        \"else { thumb.style.transform = 'translateX(0px)'; thumb.style.backgroundColor = 'var(--orange)'; bg.style.backgroundColor = 'transparent'; }\" &
			    \"}\" &"""

new_js = """\"window.rtRuleActive = true;\" &
			    \"function clickToggleRT() {\" &
			        \"window.rtRuleActive = !window.rtRuleActive;\" &
			        \"var thumb = document.getElementById('sliderThumb');\" &
			        \"var bg = document.getElementById('sliderBg');\" &
			        \"if(window.rtRuleActive) { thumb.style.transform = 'translateX(20px)'; thumb.style.backgroundColor = '#fff'; bg.style.backgroundColor = 'var(--orange)'; }\" &
			        \"else { thumb.style.transform = 'translateX(0px)'; thumb.style.backgroundColor = 'var(--orange)'; bg.style.backgroundColor = 'transparent'; }\" &
			        \"filtrarTudo();\" &
			    \"}\" &"""

content = content.replace(old_js, new_js)


# 3. Update calcularSoma to read window.rtRuleActive
old_calcular_soma = """			          "var chkRT = document.getElementById('chkRegraRt');" &
			          "var regraAtiva = chkRT ? chkRT.checked : true;" &"""

new_calcular_soma = """			          "var regraAtiva = typeof window.rtRuleActive !== 'undefined' ? window.rtRuleActive : true;" &"""

content = content.replace(old_calcular_soma, new_calcular_soma)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print("Applied bulletproof toggle JS and HTML")

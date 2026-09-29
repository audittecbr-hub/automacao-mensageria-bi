import re

filepath = r"C:\Users\cristhofer.maciel.GRUPOSTUDIO\Downloads\honorarios_regionais (2).SemanticModel\definition\tables\medidas_html.tmdl"

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# I will inject the clickToggleRT JS function right before function toggleProdDropdown
js_to_inject = """			      "window.rtRuleActive = true;" &
			      "function clickToggleRT() {" &
			          "window.rtRuleActive = !window.rtRuleActive;" &
			          "var thumb = document.getElementById('sliderThumb');" &
			          "var bg = document.getElementById('sliderBg');" &
			          "if(window.rtRuleActive) { thumb.style.transform = 'translateX(20px)'; thumb.style.backgroundColor = '#fff'; bg.style.backgroundColor = 'var(--orange)'; }" &
			          "else { thumb.style.transform = 'translateX(0px)'; thumb.style.backgroundColor = 'var(--orange)'; bg.style.backgroundColor = 'transparent'; }" &
			          "filtrarTudo();" &
			      "}" &
"""

if "function clickToggleRT" not in content:
    content = content.replace(
        "			      \"function toggleProdDropdown() {\" &",
        js_to_inject + "			      \"function toggleProdDropdown() {\" &"
    )

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print("Injected clickToggleRT successfully.")

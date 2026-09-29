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

content = content.replace(
    ".card-indicator { font-size: 15px; font-weight: 600; padding: 4px 8px; border-radius: 6px; display: inline-flex; align-items: center; gap: 4px; }\n",
    ".card-indicator { font-size: 15px; font-weight: 600; padding: 4px 8px; border-radius: 6px; display: inline-flex; align-items: center; gap: 4px; }\n" + kpi_btn_css
)

# 3. Add KPI buttons to all 7 cards in HTML_Principal
content = re.sub(
    r"(\"<div><span class='card-indicator[^>]*>[^<]*</span> <span[^>]*>[^<]*</span></div>\" & \n\s*\"</div>\" &)",
    r"\"<div><span class='card-indicator ind-down'>&#8595; 0%</span> <span style='font-size:11px;color:var(--text-muted);'>vs mês ant.</span></div>\" &\n\t\t\t                \"<button class='btn-kpi-detalhar'>DETALHAR</button>\" &\n\t\t\t            \"</div>\" &",
    content
)
# Fix the regex substitution because my replacement hardcoded 'ind-down' and '0%'. That's wrong!
# I need to capture the existing line.

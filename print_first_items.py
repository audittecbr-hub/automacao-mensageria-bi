with open('dump_encontrados_fixed.html', 'r', encoding='utf-8') as f:
    html = f.read()

raw_start = html.find("<div id='raw-data' style='display:none;'>") + len("<div id='raw-data' style='display:none;'>")
raw_end = html.find("</div>", raw_start)
raw = html[raw_start:raw_end]
items = raw.split('~')

for i, it in enumerate(items[:25]):
    print(f"Row {i}: {it}")

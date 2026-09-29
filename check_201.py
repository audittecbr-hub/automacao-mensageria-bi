with open('dump_encontrados_fixed.html', 'r', encoding='utf-8') as f:
    html = f.read()

raw_start = html.find("<div id='raw-data' style='display:none;'>") + len("<div id='raw-data' style='display:none;'>")
raw_end = html.find("</div>", raw_start)
raw = html[raw_start:raw_end]
items = raw.split('~')

print("Total items:", len(items))

sum_val = 0
for i in range(201):
    cols = items[i].split('|')
    val = float(cols[7].replace(',', '.'))
    sum_val += val

print("Sum of first 201 items:", sum_val)

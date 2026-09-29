with open('dump_negociacao_fixed.html', 'r', encoding='utf-8') as f:
    html = f.read()

raw_start = html.find("<div id='raw-data' style='display:none;'>") + len("<div id='raw-data' style='display:none;'>")
raw_end = html.find("</div>", raw_start)
raw = html[raw_start:raw_end]
items = raw.split('~')

print("Total items in negociacao:", len(items))

total_sum = 0
valid_count = 0
for it in items:
    cols = it.split('|')
    if len(cols) >= 8:
        val = float(cols[7].replace(',', '.'))
        total_sum += val
        valid_count += 1

print(f"Valid count: {valid_count}")
print(f"Calculated Total: {total_sum:,.2f}")

import json

with open("measure_names.json", "r", encoding="utf-8") as f:
    names = json.load(f)

for n in names:
    if "repasse" in n.lower() or "tax" in n.lower() or "receita" in n.lower():
        print(n)

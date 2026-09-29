import json

with open("all_clean_payloads.json", "r", encoding="utf-8") as f:
    payloads = json.load(f)

print(f"Total payloads: {len(payloads)}")
for p in payloads:
    name = p['name']
    expr = p['expression']
    print(f"{name}: len={len(expr)}, backslashes={expr.count('\\')}")

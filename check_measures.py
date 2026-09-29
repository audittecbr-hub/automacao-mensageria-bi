import json

with open('updated_html_measures.json', 'r', encoding='utf-8') as f:
    measures = json.load(f)

# Let's inspect the first one
print(f"Total measures to update: {len(measures)}")
for m in measures:
    print(f"- {m['name']} (Length: {len(m['expression'])})")

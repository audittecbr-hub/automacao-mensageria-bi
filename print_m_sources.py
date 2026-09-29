import json

with open(r'C:\Users\cristhofer.maciel.GRUPOSTUDIO\.gemini\antigravity-ide\brain\86a55459-41f9-4a50-8a31-1a8a8f9a51d5\.system_generated\steps\2020\output.txt', 'r', encoding='utf-8') as f:
    data = json.load(f)

for r in data['results']:
    t = r['data'].get('tableName')
    p = r['data'].get('name')
    mode = r['data'].get('mode')
    src = r['data'].get('source', '')
    print(f"=== Table: {t} | Partition: {p} ===")
    print("Source expression:")
    print(src)
    print()

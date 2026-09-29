import json

with open(r'C:\Users\cristhofer.maciel.GRUPOSTUDIO\.gemini\antigravity-ide\brain\86a55459-41f9-4a50-8a31-1a8a8f9a51d5\.system_generated\steps\1678\output.txt', 'r', encoding='utf-8') as f:
    data = json.load(f)

measure_names = [m['name'] for m in data['data']]
print(f"Total measures: {len(measure_names)}")
with open("measure_names.json", "w", encoding="utf-8") as out:
    json.dump(measure_names, out, ensure_ascii=False)

import json

with open(r'C:\Users\cristhofer.maciel.GRUPOSTUDIO\.gemini\antigravity-ide\brain\86a55459-41f9-4a50-8a31-1a8a8f9a51d5\.system_generated\steps\2008\output.txt', 'r', encoding='utf-8') as f:
    data = json.load(f)

for p in data['data']:
    t = p.get('tableName')
    name = p.get('name')
    mode = p.get('mode')
    sourceType = p.get('sourceType')
    print(f"Table: {t} | Partition: {name} | Mode: {mode} | SourceType: {sourceType}")
    # Let's inspect source if available
    src = p.get('source', '')
    if src:
        print(f"  Source preview: {repr(src[:200])}")

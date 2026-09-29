import json
with open('compact_sync_payload.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for item in data:
    if item['name'] == 'HTML_Detalhamento_Encontrados':
        with open('enc_compact_dax.txt', 'w', encoding='utf-8') as out:
            out.write(item['expression'])
        print("Wrote enc_compact_dax.txt")
        break

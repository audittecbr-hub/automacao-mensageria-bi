import urllib.request
import json
import re

with open('painel_script.js', 'r', encoding='utf-8') as f:
    text = f.read()

sb_url_m = re.search(r'var SB_URL\s*=\s*[\'"]([^\'"]+)[\'"]', text)
sb_key_m = re.search(r'var SB_KEY\s*=\s*[\'"]([^\'"]+)[\'"]', text)
doc_id_m = re.search(r'var DOC_ID\s*=\s*[\'"]([^\'"]+)[\'"]', text)

sb_url = sb_url_m.group(1) if sb_url_m else ''
sb_key = sb_key_m.group(1) if sb_key_m else ''
doc_id = doc_id_m.group(1) if doc_id_m else ''

print('SB_URL:', sb_url)
print('SB_KEY:', sb_key[:20] + '...')
print('DOC_ID:', doc_id)

url = sb_url + '?id=eq.' + doc_id + '&select=*'
req = urllib.request.Request(url, headers={'apikey': sb_key, 'Authorization': 'Bearer ' + sb_key})
try:
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode())
        print('Supabase status code: 200')
        print('Records returned:', len(data))
        if data:
            row = data[0]
            print('Title:', row.get('title'))
            print('Category:', row.get('category'))
            print('Updated at / Created at:', row.get('updated_at'), row.get('created_at'))
            desc = row.get('description', '')
            print('Description length:', len(desc))
            if desc:
                saved_map = json.loads(desc)
                print(f'Total saved items in Supabase: {len(saved_map)}')
                for k, v in list(saved_map.items())[:15]:
                    print(f'   ID {k}: {v}')
except Exception as e:
    print('Error querying Supabase:', e)

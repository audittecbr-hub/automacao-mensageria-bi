with open('detalhes_expressions.txt', 'r', encoding='utf-8') as f:
    text = f.read()

p = text.split('=== HTML_Detalhamento_Aprovados ===')[1].split('===')[0]
for l in p.split('\n'):
    if any(k in l.lower() for k in ['tfoot', 'total', 'count', 'rodape', 'sum']):
        print(l.strip())

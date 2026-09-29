with open('detalhes_expressions.txt', 'r', encoding='utf-8') as f:
    text = f.read()

parts = text.split('=== HTML_Detalhamento_')
for p in parts[1:]:
    lines = p.split('\n')
    m_name = lines[0].replace(' ===', '').strip()
    print(f"\n==================== {m_name} ====================")
    for l in lines:
        if any(k in l for k in ['VAR _linhas', 'FILTER(', 'CONCATENATEX(', 'VAR _Total', 'data-mes', 'data-rt', 'data-mov', 'DATA_RT', 'DATA_MOV_ANTERIOR', 'data_mov_anterior', 'tfoot', 'sumTotal']):
            print("  ", l.strip()[:140])

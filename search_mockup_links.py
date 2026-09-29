with open('Mockup_Honorarios_Matriz_Current.dax', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'detalhar' in l.lower() or 'html_detalhamento' in l.lower() or 'onclick' in l.lower():
        print(f"L{i+1}: {l.strip()}")

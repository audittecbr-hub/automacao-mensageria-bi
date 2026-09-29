with open('Mockup_Honorarios_Matriz.dax', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'encontrad' in l.lower() or 'hono_encontrados' in l.lower() or 'total_encontrado' in l.lower():
        print(f"L{i+1}: {l.strip()}")

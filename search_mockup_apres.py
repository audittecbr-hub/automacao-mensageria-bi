with open('Mockup_Honorarios_Matriz.dax', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if '_dadosapresentados' in l.lower() or 'hono_apresentados' in l.lower() or 'apres-' in l.lower():
        print(f"L{i+1}: {l.strip()}")

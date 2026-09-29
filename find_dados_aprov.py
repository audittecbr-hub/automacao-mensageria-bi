with open('Mockup_Honorarios_Matriz.dax', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if '_dadosaprovados =' in l.lower() or '_dadosiniciais =' in l.lower():
        print(f"L{i+1}: {l.strip()}")

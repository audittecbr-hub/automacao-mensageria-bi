with open('Mockup_Honorarios_Matriz.dax', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if any(k in l.lower() for k in ['pontua', 'ranking', 'pts', 'peso', 'legendadepontuacao', 'scomp', 'sretif', 'sajuiz', 'sap']):
        print(f"L{i+1}: {l.strip()}")

with open('Mockup_Honorarios_Matriz.dax', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if any(k in l.lower() for k in ['_dadosaprov', 'dado-ap', 'dado-comp', 'dado-retif', 'dado-ajuiz', 'dado-ini', 'hi-', 'hc-', 'hr-', 'ha-']):
        print(f"L{i+1}: {l.strip()}")

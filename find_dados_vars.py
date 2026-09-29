with open('Mockup_Honorarios_Matriz_Current.dax', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if "VAR _dados" in l:
        print(f"L{i+1}: {l.strip()}")

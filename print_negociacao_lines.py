with open('Mockup_Honorarios_Matriz_Current.dax', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(309, 412):
    if i < len(lines):
        print(f"L{i+1}: {lines[i]}", end='')

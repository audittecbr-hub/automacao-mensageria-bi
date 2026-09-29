with open('Mockup_Honorarios_Matriz.dax', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(899, 955):
    if i < len(lines):
        print(f"L{i+1}: {lines[i]}", end='')

with open('Mockup_Honorarios_Matriz_Current.dax', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(69, 110):
    print(f"L{i+1}: {lines[i]}", end="")

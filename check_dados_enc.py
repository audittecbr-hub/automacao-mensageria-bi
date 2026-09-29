with open('Mockup_Honorarios_Matriz_Current.dax', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print("--- _dadosEncontrados in Mockup DAX ---")
for i in range(140, 185):
    if i < len(lines):
        print(f"L{i+1}: {lines[i]}", end="")

print("\n--- _dadosApresentados in Mockup DAX ---")
for i in range(200, 240):
    if i < len(lines):
        print(f"L{i+1}: {lines[i]}", end="")

with open('Mockup_Honorarios_Matriz_Current.dax', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print("--- _dadosEncontrados (L144-177) ---")
for i in range(143, 178):
    print(f"L{i+1}: {lines[i]}", end="")

print("\n--- _dadosApresentados (L205-238) ---")
for i in range(204, 239):
    print(f"L{i+1}: {lines[i]}", end="")

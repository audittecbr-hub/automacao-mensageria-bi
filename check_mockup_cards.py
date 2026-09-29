with open('Mockup_Honorarios_Matriz_Current.dax', 'r', encoding='utf-8') as f:
    code = f.read()

# Let's search for card IDs and calculations in JS and DAX
import re

print("--- CARDS IN HTML ---")
for m in re.finditer(r"id=['\"]card-[^'\"]+['\"]", code):
    print(m.group(0))

print("\n--- CALCULATIONS FOR CARDS IN JS ---")
# search for document.getElementById('card-
for line in code.split('\n'):
    if "document.getElementById('card-" in line or "document.getElementById(\"card-" in line:
        print(line.strip())

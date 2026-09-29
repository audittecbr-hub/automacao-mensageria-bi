with open('matriz_with_apneg.dax', 'r', encoding='utf-8') as f:
    dax = f.read()

# Fix missing quote on line 946
dax = dax.replace("    <div style='display:none;' id='dados-aprov-total-container'>", "    \"<div style='display:none;' id='dados-aprov-total-container'>")

with open('matriz_with_apneg.dax', 'w', encoding='utf-8') as f:
    f.write(dax)

print("Fixed line 946 quote successfully!")

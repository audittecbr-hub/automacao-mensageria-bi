with open('matriz_perfect.dax', 'r', encoding='utf-8-sig') as f:
    dax = f.read()

dax = dax.replace('    "    "<div style=\'display:none;\' id=\'dados-apneg-total-container\'>', '    "<div style=\'display:none;\' id=\'dados-apneg-total-container\'>')

with open('matriz_perfect.dax', 'w', encoding='utf-8-sig') as f:
    f.write(dax)

print("Fixed double quote on line 947 successfully!")

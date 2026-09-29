import json

with open('Painel_Repasses_dax.txt', 'r', encoding='utf-8') as f:
    dax_code = f.read()

# Let's inspect if any double quotes or anything need attention in DAX
print("DAX file loaded. First 100 chars:")
print(dax_code[:100])

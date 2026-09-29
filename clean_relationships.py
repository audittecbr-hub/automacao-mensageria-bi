import re

rel_path = r'C:\Users\cristhofer.maciel.GRUPOSTUDIO\Downloads\Ranking_Metas_V2.SemanticModel\definition\relationships.tmdl'
with open(rel_path, 'r', encoding='utf-8') as f:
    text = f.read()

# Split by relationship blocks
blocks = re.split(r'(?=relationship\s+[0-9a-f\-]+)', text)
clean_blocks = []
for b in blocks:
    if 'public metas_bruto' not in b and 'LocalDateTable_caf78040' not in b and 'LocalDateTable_9192e880' not in b and 'LocalDateTable_1eda6a16' not in b:
        if b.strip():
            clean_blocks.append(b.strip())

new_text = '\n\n'.join(clean_blocks) + '\n'

with open(rel_path, 'w', encoding='utf-8') as f:
    f.write(new_text)

print("relationships.tmdl cleaned successfully!")

import re

with open(r"C:\Users\cristhofer.maciel.GRUPOSTUDIO\.gemini\antigravity-ide\brain\72165768-232a-406d-96b3-99d4a9874520\.system_generated\steps\501\output.txt", "r", encoding="utf-8") as f:
    text = f.read()

matches = re.findall(r"\{id:'11797685925'.*?\}", text)
for m in matches:
    print("Contract 380 row in JSON:", m)

matches_all_contab = re.findall(r"\{id:'\d+',cnpj:'[^']+',nome:'[^']+',bandeira:'[^']+',categoria:'Receita de Contabilidade Recorrente'.*?\}", text)
print(f"\nFound {len(matches_all_contab)} Contabilidade rows. First 3:")
for m in matches_all_contab[:3]:
    print(" -", m)

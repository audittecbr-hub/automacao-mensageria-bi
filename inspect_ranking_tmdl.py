import os, re

tmdl_dir = r"c:\Users\cristhofer.maciel.GRUPOSTUDIO\Downloads\Ranking_Metas_V2.SemanticModel\definition\tables"

for fname in ["Medidas_Repasse.tmdl", "Medidas.tmdl", "Medidas_HTML.tmdl"]:
    fpath = os.path.join(tmdl_dir, fname)
    if os.path.exists(fpath):
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
        print(f"\n==========================================")
        print(f"ARQUIVO: {fname} (Tamanho: {len(content)})")
        measures = re.findall(r"measure\s+([^\s=]+)\s*=", content)
        print("Medidas encontradas:", measures)

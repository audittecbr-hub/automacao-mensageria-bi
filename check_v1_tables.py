import os

v1_dir = r'C:\Users\cristhofer.maciel.GRUPOSTUDIO\Downloads\Ranking_Metas.SemanticModel\definition\tables'
if os.path.exists(v1_dir):
    print("V1 tables found:")
    for f in os.listdir(v1_dir):
        print("  -", f)
        if 'repasse' in f.lower() or 'tax' in f.lower() or 'honorario' in f.lower():
            fp = os.path.join(v1_dir, f)
            with open(fp, 'r', encoding='utf-8', errors='ignore') as fl:
                print(f"--- CONTENT OF {f} (first 500 chars) ---")
                print(fl.read()[:500])
else:
    print("V1 dir does not exist.")

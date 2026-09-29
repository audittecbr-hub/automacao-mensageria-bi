import os

tmdl_dir = r"C:\Users\cristhofer.maciel.GRUPOSTUDIO\Downloads\Ranking_Metas.SemanticModel\definition\tables"
for f in os.listdir(tmdl_dir):
    if f.endswith('.tmdl'):
        path = os.path.join(tmdl_dir, f)
        with open(path, 'r', encoding='utf-8') as file:
            content = file.read()
            if 'PostgreSQL.Database' in content:
                print(f"File: {f}")
                for line in content.split('\n'):
                    if 'PostgreSQL.Database' in line or 'Fonte' in line:
                        print(f"  {line}")

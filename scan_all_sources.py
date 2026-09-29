import os

root_dir = r"C:\Users\cristhofer.maciel.GRUPOSTUDIO\Downloads\Ranking_Metas.SemanticModel\definition"
for root, dirs, files in os.walk(root_dir):
    for f in files:
        if f.endswith('.tmdl'):
            path = os.path.join(root, f)
            with open(path, 'r', encoding='utf-8') as file:
                content = file.read()
                if 'Fonte' in content or 'Database' in content:
                    print(f"File: {os.path.relpath(path, root_dir)}")
                    for line in content.split('\n'):
                        if any(k in line for k in ['Fonte', 'Database', 'PostgreSQL', 'Sql', 'OData', 'Web', 'Json', 'Excel', 'Csv', 'SharePoint']):
                            print(f"  {line.strip()}")

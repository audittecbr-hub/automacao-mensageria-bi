import os

tmdl_dir = r"C:\Users\cristhofer.maciel.GRUPOSTUDIO\OneDrive\repasse.SemanticModel\definition\tables"
for f in os.listdir(tmdl_dir):
    if f.endswith('.tmdl') and not f.startswith('LocalDate') and not f.startswith('DateTable'):
        path = os.path.join(tmdl_dir, f)
        print(f"=== {f} ===")
        with open(path, 'r', encoding='utf-8') as file:
            print(file.read())
        print("="*60)

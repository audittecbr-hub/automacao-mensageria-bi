import os

model_dir = r"C:\Users\cristhofer.maciel.GRUPOSTUDIO\OneDrive\repasse.SemanticModel\definition"
for root, dirs, files in os.walk(model_dir):
    for f in files:
        if f.endswith('.tmdl'):
            path = os.path.join(root, f)
            with open(path, 'r', encoding='utf-8') as file:
                content = file.read()
                if 'Func_JOB_CALCULAR_HONORARIO' in content or 'HonorariosPorJob' in content or 'metas_bruto' in content:
                    print(f"=== {os.path.relpath(path, model_dir)} ===")
                    print(content)
                    print("="*60)

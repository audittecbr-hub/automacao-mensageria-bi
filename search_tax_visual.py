import os
import json

report_dir = r'C:\Users\cristhofer.maciel.GRUPOSTUDIO\Downloads\Ranking_Metas_V2.Report\definition\pages'
for root, dirs, files in os.walk(report_dir):
    for f in files:
        if f.endswith('.json'):
            fp = os.path.join(root, f)
            with open(fp, 'r', encoding='utf-8') as fl:
                content = fl.read()
                if 'valor_Tax_Repasse' in content or '3213330' in content or '3.213.330' in content:
                    print("Found in:", fp)
                    # print snippet
                    for line in content.splitlines():
                        if 'valor_Tax_Repasse' in line or 'Repasse' in line:
                            print("   ", line[:100])

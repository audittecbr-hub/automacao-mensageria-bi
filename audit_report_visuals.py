import os

report_dir = r'C:\Users\cristhofer.maciel.GRUPOSTUDIO\Downloads\Ranking_Metas_V2.Report'
terms = ['metas_bruto', 'unidadesporcnpj', 'departamentos', 'honorariosporjob', 'vw_powerbi_job_repasse']
matches = {t: [] for t in terms}

for root, dirs, files in os.walk(report_dir):
    for f in files:
        fp = os.path.join(root, f)
        try:
            with open(fp, 'r', encoding='utf-8', errors='ignore') as fl:
                content = fl.read().lower()
                for t in terms:
                    if t in content:
                        matches[t].append(fp)
        except:
            pass

print("=== REPORT VISUALS AUDIT ===")
for t, m in matches.items():
    print(f"Term '{t}': found in {len(m)} files")
    for item in m:
        print("   ->", item)

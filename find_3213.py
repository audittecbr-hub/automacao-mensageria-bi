import os

search_dir = r'C:\Users\cristhofer.maciel.GRUPOSTUDIO\.gemini\antigravity\scratch\automacao-mensageria-bi'
for root, dirs, files in os.walk(search_dir):
    for f in files:
        if f.endswith(('.py', '.dax', '.txt', '.json', '.ps1', '.sql')):
            fp = os.path.join(root, f)
            try:
                with open(fp, 'r', encoding='utf-8', errors='ignore') as fl:
                    c = fl.read()
                    if '3213330' in c or '3.213.330' in c or '3213' in c:
                        print("Found in:", f)
            except:
                pass

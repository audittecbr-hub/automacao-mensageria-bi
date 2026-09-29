import os
import json

brain_dir = r"C:\Users\cristhofer.maciel.GRUPOSTUDIO\.gemini\antigravity-ide\brain"
print("Scanning brain_dir...")

found = []
for root, dirs, files in os.walk(brain_dir):
    for f in files:
        if f == "transcript.jsonl":
            p = os.path.join(root, f)
            with open(p, "r", encoding="utf-8", errors="ignore") as fl:
                for idx, line in enumerate(fl):
                    if "vw_powerbi_job_repasse" in line and ("CREATE VIEW" in line or "ALTER VIEW" in line):
                        print(f"Match in {p} at line {idx}")
                        found.append((p, idx, line))

print(f"Total matches: {len(found)}")
if found:
    # examine first match
    p, idx, l = found[0]
    data = json.loads(l)
    print("Keys:", data.keys())
    print("Content snippet:", str(data)[:1000])

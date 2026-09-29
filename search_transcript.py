import re

log_path = r'C:\Users\cristhofer.maciel.GRUPOSTUDIO\.gemini\antigravity-ide\brain\53a8a01a-da38-486b-92ec-ae80b30b913e\.system_generated\logs\transcript.jsonl'
with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
    for line_num, line in enumerate(f):
        if '3213330' in line or '3.213.330' in line or '2113680' in line or '2.113.680' in line or '15.774' in line or '15774174' in line:
            print(f"Line {line_num}:")
            matches = re.findall(r'.{0,50}(?:3213330|3\.213\.330|2113680|2\.113\.680|15774174).{0,50}', line)
            for m in matches[:3]:
                print("   ...", m, "...")

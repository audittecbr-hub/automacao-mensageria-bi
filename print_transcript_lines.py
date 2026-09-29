log_path = r'C:\Users\cristhofer.maciel.GRUPOSTUDIO\.gemini\antigravity-ide\brain\53a8a01a-da38-486b-92ec-ae80b30b913e\.system_generated\logs\transcript.jsonl'
with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
    for i, line in enumerate(f):
        if 1360 <= i <= 1380:
            print(f"--- Line {i} ---")
            print(line[:300])

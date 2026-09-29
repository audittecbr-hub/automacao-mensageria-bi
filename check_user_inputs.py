import json

for conv_id in ["72165768-232a-406d-96b3-99d4a9874520", "53a8a01a-da38-486b-92ec-ae80b30b913e"]:
    p = rf"C:\Users\cristhofer.maciel.GRUPOSTUDIO\.gemini\antigravity-ide\brain\{conv_id}\.system_generated\logs\transcript.jsonl"
    print(f"=== CONVERSATION {conv_id} ===")
    with open(p, "r", encoding="utf-8", errors="ignore") as f:
        for idx, line in enumerate(f):
            data = json.loads(line)
            if data.get("type") == "USER_INPUT":
                text = data.get("content", "")
                if any(k in text.lower() for k in ["view", "repasse", "funcao", "função", "cagada", "job"]):
                    print(f"User at {idx}: {text[:200]}")

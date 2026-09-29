import json

p = r"C:\Users\cristhofer.maciel.GRUPOSTUDIO\.gemini\antigravity-ide\brain\72165768-232a-406d-96b3-99d4a9874520\.system_generated\logs\transcript.jsonl"
lines_to_check = [379, 424, 561, 587, 593, 608, 646]

with open(p, "r", encoding="utf-8", errors="ignore") as f:
    for idx, line in enumerate(f):
        if idx in lines_to_check:
            data = json.loads(line)
            print(f"=== Line {idx} Step {data.get('step_index')} Source {data.get('source')} Type {data.get('type')} ===")
            content = data.get("content", "")
            if content:
                print("Content:", content[:300])
            for tc in data.get("tool_calls", []):
                print("Tool call:", tc.get("name"), tc.get("args"))

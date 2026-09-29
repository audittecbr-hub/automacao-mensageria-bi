import json

p = r"C:\Users\cristhofer.maciel.GRUPOSTUDIO\.gemini\antigravity-ide\brain\53a8a01a-da38-486b-92ec-ae80b30b913e\.system_generated\logs\transcript.jsonl"

with open(p, "r", encoding="utf-8", errors="ignore") as f:
    for idx, line in enumerate(f):
        if 2565 <= idx <= 2600:
            data = json.loads(line)
            print(f"=== Line {idx} Step {data.get('step_index')} Source {data.get('source')} Type {data.get('type')} ===")
            content = data.get("content", "")
            if content:
                print("Content:", content[:400])
            for tc in data.get("tool_calls", []):
                print("Tool call:", tc.get("name"))
                args = tc.get("args", {})
                for k, v in args.items():
                    print(f"  {k}: {str(v)[:300]}")

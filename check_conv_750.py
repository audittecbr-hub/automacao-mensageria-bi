import json
import sys

p = r"C:\Users\cristhofer.maciel.GRUPOSTUDIO\.gemini\antigravity-ide\brain\53a8a01a-da38-486b-92ec-ae80b30b913e\.system_generated\logs\transcript.jsonl"

with open(p, "r", encoding="utf-8", errors="ignore") as f:
    for idx, line in enumerate(f):
        if 750 <= idx <= 776:
            data = json.loads(line)
            sys.stdout.buffer.write(f"=== Line {idx} Step {data.get('step_index')} Source {data.get('source')} Type {data.get('type')} ===\n".encode("utf-8"))
            content = data.get("content", "")
            if content:
                sys.stdout.buffer.write(f"Content: {content[:300]}\n".encode("utf-8", errors="replace"))
            for tc in data.get("tool_calls", []):
                sys.stdout.buffer.write(f"Tool call: {tc.get('name')}\n".encode("utf-8"))
                args = tc.get("args", {})
                for k, v in args.items():
                    sys.stdout.buffer.write(f"  {k}: {str(v)[:300]}\n".encode("utf-8", errors="replace"))

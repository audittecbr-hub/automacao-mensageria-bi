import json
import sys

p = r"C:\Users\cristhofer.maciel.GRUPOSTUDIO\.gemini\antigravity-ide\brain\53a8a01a-da38-486b-92ec-ae80b30b913e\.system_generated\logs\transcript.jsonl"

with open(p, "r", encoding="utf-8", errors="ignore") as f:
    for idx, line in enumerate(f):
        if 2568 <= idx <= 2585:
            data = json.loads(line)
            sys.stdout.buffer.write(f"\n--- LINE {idx} Step {data.get('step_index')} {data.get('source')} {data.get('type')} ---\n".encode("utf-8"))
            content = data.get("content", "")
            if content:
                sys.stdout.buffer.write(f"{content[:500]}\n".encode("utf-8", errors="replace"))

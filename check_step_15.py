import json
import sys

p = r"C:\Users\cristhofer.maciel.GRUPOSTUDIO\.gemini\antigravity-ide\brain\72165768-232a-406d-96b3-99d4a9874520\.system_generated\logs\transcript.jsonl"

with open(p, "r", encoding="utf-8", errors="ignore") as f:
    for idx, line in enumerate(f):
        if idx in [14, 15, 16]:
            data = json.loads(line)
            sys.stdout.buffer.write(f"=== Line {idx} Step {data.get('step_index')} Source {data.get('source')} Type {data.get('type')} ===\n".encode("utf-8"))
            content = data.get("content", "")
            sys.stdout.buffer.write(f"Content:\n{content}\n".encode("utf-8", errors="replace"))

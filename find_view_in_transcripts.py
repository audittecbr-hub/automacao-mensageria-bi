import os
import glob
import json

brain_dir = r"C:\Users\cristhofer.maciel.GRUPOSTUDIO\.gemini\antigravity-ide\brain"

for jsonl in glob.glob(os.path.join(brain_dir, "**", "transcript*.jsonl"), recursive=True):
    try:
        with open(jsonl, "r", encoding="utf-8", errors="ignore") as f:
            for line_no, line in enumerate(f, 1):
                if "vw_powerbi_job_repasse" in line and ("CREATE VIEW" in line or "ALTER VIEW" in line):
                    # print matching snippet
                    try:
                        data = json.loads(line)
                        content = data.get("content", "")
                        tool_calls = data.get("tool_calls", [])
                        print(f"File: {jsonl} Line: {line_no} Type: {data.get('type')}")
                        for tc in tool_calls:
                            args = tc.get("args", {})
                            cmd = args.get("CommandLine") or args.get("CodeContent") or args.get("ReplacementContent") or ""
                            if "CREATE VIEW" in cmd or "ALTER VIEW" in cmd:
                                print(f"--- TOOL CALL {tc.get('name')} in {jsonl} ---")
                                print(cmd[:500])
                        if "CREATE VIEW" in content or "ALTER VIEW" in content:
                            print(f"--- CONTENT in {jsonl} ---")
                            print(content[:500])
                    except Exception as e:
                        pass
    except Exception as e:
        pass

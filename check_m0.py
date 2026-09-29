with open("clean_m_0.json", "r", encoding="utf-8") as f:
    text = f.read()

lines = text.split('\n')
for idx, l in enumerate(lines, 1):
    if '\\' in l:
        print(f"Line {idx}: {l}")

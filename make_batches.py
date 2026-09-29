import json

with open("measure_names.json", "r", encoding="utf-8") as f:
    names = json.load(f)

# Split into batches of 30
batches = [names[i:i+30] for i in range(0, len(names), 30)]
for idx, b in enumerate(batches):
    refs = [{"name": n} for n in b]
    with open(f"batch_get_{idx}.json", "w", encoding="utf-8") as out:
        json.dump(refs, out)

print(f"Created {len(batches)} batches")

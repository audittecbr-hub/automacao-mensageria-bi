import json

# Let's get all measure names from measure_names.json
with open("measure_names.json", "r", encoding="utf-8") as f:
    names = json.load(f)

# We will generate a DAX query that evaluates each measure one by one
print(f"Total measures: {len(names)}")
# Let's create single measure queries to test
for idx, name in enumerate(names):
    # sanitize name
    clean_name = name.replace('"', '""')
    # Save a list of queries
with open("measures_to_test.json", "w", encoding="utf-8") as out:
    json.dump(names, out, ensure_ascii=False)

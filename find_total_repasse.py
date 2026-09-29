import json

with open("measure_names.json", "r", encoding="utf-8") as f:
    names = json.load(f)

# Let's get table names for all measures named total_repasse or repasse
# We can use measure_operations to inspect all tables

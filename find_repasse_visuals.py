import os
import json

report_path = r'C:\Users\cristhofer.maciel.GRUPOSTUDIO\Downloads\Ranking_Metas_V2.Report\report.json'
with open(report_path, 'r', encoding='utf-8') as f:
    text = f.read()

# Search for repasse measures in visuals
import re
measures_found = set(re.findall(r'"Property":\s*"([^"]*Repasse[^"]*)"', text, re.IGNORECASE))
print("Repasse measures in report.json:", measures_found)

import re

with open('HTML_Onboarding_Executivo.dax', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace all \" with ' in the JS string
# For example:
# class=\"badge b-green\" -> class='badge b-green'
# [data-col=\"0\"] -> [data-col='0']
fixed_content = content.replace('\\"', "'")

with open('HTML_Onboarding_Executivo.dax', 'w', encoding='utf-8') as f:
    f.write(fixed_content)

print("HTML_Onboarding_Executivo.dax cleaned successfully.")

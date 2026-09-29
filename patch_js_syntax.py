import re

file_path = r'C:\Users\cristhofer.maciel.GRUPOSTUDIO\Desktop\HTML_Detalhamento_Aprovados_Corrigido.dax'
with open(file_path, 'r', encoding='utf8') as f:
    dax = f.read()

# Let's find the bad block
bad_block_start = '"function toggleDropdown(id) {" &'
if bad_block_start in dax:
    # We want to replace the whole block of concatenated strings that I mistakenly added
    # up to ");" &
    
    # regex to find from the start of the bad block to the end of it
    pattern = r'"function toggleDropdown\(id\) \{" &.*?"\}\);" &'
    match = re.search(pattern, dax, flags=re.DOTALL)
    
    if match:
        bad_code = match.group(0)
        
        # Convert it to plain js by removing '" &' from end of lines and '"' from start
        good_code = bad_code
        good_code = re.sub(r'^"', '', good_code, flags=re.MULTILINE)
        good_code = re.sub(r'" &$', '', good_code, flags=re.MULTILINE)
        
        dax = dax.replace(bad_code, good_code)

with open(file_path, 'w', encoding='utf8') as f:
    f.write(dax)

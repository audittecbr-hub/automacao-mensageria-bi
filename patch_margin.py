import re

file_path = r'C:\Users\cristhofer.maciel.GRUPOSTUDIO\Desktop\Mockup_Honorarios_Matriz_Corrigido.dax'
with open(file_path, 'r', encoding='utf8') as f:
    dax = f.read()

# Replace margin-bottom: 30px in .header with margin-bottom: 90px
old_header = '.header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px; position: relative; z-index: 99999; }'
new_header = '.header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 80px; position: relative; z-index: 99999; }'

if old_header in dax:
    dax = dax.replace(old_header, new_header)
else:
    # Use regex
    dax = re.sub(
        r'\.header\s*\{\s*display:\s*flex;\s*justify-content:\s*space-between;\s*align-items:\s*center;\s*margin-bottom:\s*30px;\s*position:\s*relative;\s*z-index:\s*99999;\s*\}',
        new_header,
        dax
    )
    
# Let's check if there are other margins we should increase
# Like z-index of .dropdown-menu is 9999
old_dropdown_menu = '.dropdown-menu { display: none; position: absolute; top: calc(100% + 5px); right: 0; width: 280px;'
new_dropdown_menu = '.dropdown-menu { display: none; position: absolute; top: calc(100% + 5px); right: 0; width: 280px;' # Z-index is further down

with open(file_path, 'w', encoding='utf8') as f:
    f.write(dax)

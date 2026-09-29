with open('Painel_Repasses_Codigo.txt', 'r', encoding='utf8') as f:
    text = f.read()

# Let's extract the VAR _html = "..." string
start = text.find('VAR _html = "')
if start != -1:
    html_part = text[start + 13 : text.rfind('"')]
    # In DAX, double quotes inside the string must be doubled
    i = 0
    errors = 0
    while i < len(html_part):
        if html_part[i] == '"':
            if i + 1 < len(html_part) and html_part[i+1] == '"':
                i += 2  # Valid escaped quote
            else:
                print(f"UNESCAPED QUOTE FOUND AT INDEX {i}: {html_part[i-20:i+20]}")
                errors += 1
                i += 1
        else:
            i += 1
    if errors == 0:
        print("NO UNESCAPED QUOTES FOUND")
